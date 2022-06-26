import os
import sys
sys.path.append(os.path.abspath("../../common"))
sys.path.append(os.path.abspath("common"))

from datetime import timedelta

from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo import UpdateOne, InsertOne

from redis import StrictRedis
r = StrictRedis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)

import tools
logger = tools.get_logger()
db = tools.get_mongo()


def handle_nimble_report(NimbleReportReq, reported_at):
    queries = []
    reports = {}
    unique_streams = set()

    for vhost in NimbleReportReq.PayPerViewInfo.VHost:
        for application in vhost.Application:
            for instance in application.Instance:
                for stream in instance.Stream:
                    for player in stream.Player:
                        report = {
                            "vhost": NimbleReportReq.vhost,
                            "report": {
                                "ip_address": player.ip,
                                "user_agent": (player.user_agents or [None])[0],
                                "stream_path": stream.name
                            }
                        }
                        if not ObjectId.is_valid(player.id):
                            if vhost.name == player.ip:
                                # Skip local Flussonic requests
                                continue

                            # Getting rid of whitelisted sessions by Nimble.
                            report.update(
                                given_id=(player.id or None),
                                started_at=reported_at,
                                state="crooked",
                                reason="Invalid stream ID"
                            )
                            queries.append(UpdateOne(
                                {"nid": f"{vhost.name}-{player.ip}-{stream.name}"},
                                {
                                    "$set": {"updated_at": reported_at},
                                    "$setOnInsert": report
                                },
                                upsert=True
                            ))
                            continue
                        reports[ObjectId(player.id)] = report

    requests = db.requests.find({"_id": {"$in": list(reports)}})
    requests = {url.pop("_id"): url for url in requests}

    reject_key = f"nimble:{NimbleReportReq.vhost}:reject"

    for request_id, request in reports.items():
        if request_id in requests:
            request.update(**requests[request_id])

        if request.get("state") == "rejected":
            # r.sadd(reject_key, request_id)
            # continue
            pass

        request.setdefault("started_at", reported_at)
        request.update({"updated_at": reported_at})

        if "request" not in request:
            request.update(state="crooked", reason="Falsified stream ID")
        else:
            session_ids_key = f"login:{request['login']}:sid"
            session_id_key = f"{session_ids_key}:{request['session_id']}"

            if request_id in unique_streams:
                r.sadd(reject_key, str(request_id))
                request.update(state="rejected", reason="multiple usage")
            elif request["report"]["stream_path"] not in request["request"]["stream_name"]:
                r.sadd(reject_key, str(request_id))
                request.update(state="rejected", reason="stream mismatch")
            elif request["report"]["ip_address"] != request["request"]["ip_address"]:
                r.sadd(reject_key, str(request_id))
                request.update(state="rejected", reason="ip mismatch")
            elif request["session_id"] not in r.zrange(session_ids_key, 0, -1):
                logger.debug(f"({type(request['session_id'])}) {request['session_id']}")
                logger.debug(f"SID KEY {session_ids_key}: {r.zrange(session_ids_key, 0, -1)}")
                r.sadd(reject_key, str(request_id))
                request.update(state="rejected", reason="no active account session")
            elif str(request_id) != r.get(session_id_key):
                r.sadd(reject_key, str(request_id))
                request.update(state="rejected", reason="no active stream request")
            else:
                unique_streams.add(request_id)
                r.expire(session_id_key, 86400)
                request.update(state="reported")

        queries.append(UpdateOne(
            {"_id": request_id},
            {"$set": request},
            upsert=True
        ))

    if queries:
        db.requests.bulk_write(queries)


def handle_flussonic_report(FlussonicReportReq, reported_at):
    report = {
        "vhost": FlussonicReportReq.vhost,
        "report": {
            "ip_address": FlussonicReportReq.ip,
            "user_agent": FlussonicReportReq.user_agent,
            "stream_path": FlussonicReportReq.name
        }
    }

    if FlussonicReportReq.media_request == "hls_live-hls_track_segment":
        report.update(content_type="channel", stream_type="hls")
    elif FlussonicReportReq.media_request in ["hls_dvr-segment", "hls_dvr-track_segment"]:
        report.update(content_type="program", stream_type="hls")
    elif FlussonicReportReq.media_request == "mpegts_handler-request":
        report.update(content_type="channel", stream_type="mpegts")
    elif FlussonicReportReq.media_request.startswith("dvr_stream_handler"):
        report.update(content_type="program", stream_type="mpegts")
    else:
        return

    if not ObjectId.is_valid(FlussonicReportReq.token):
        report.update(
            given_id=(FlussonicReportReq.token or None),
            started_at=reported_at,
            state="crooked",
            reason="Invalid stream ID"
        )
        db.requests.update_one(
            {"nid": f"{FlussonicReportReq.vhost}-{FlussonicReportReq.ip}-{FlussonicReportReq.session_id}"},
            {
                "$set": {"updated_at": reported_at},
                "$setOnInsert": report
            },
            upsert=True
        )
        return

    request_id = ObjectId(FlussonicReportReq.token)
    streamurl = db.requests.find_one(request_id)
    if streamurl:
        report.update(**streamurl)

    duration = timedelta(seconds=FlussonicReportReq.duration)
    report.setdefault("started_at", (reported_at - duration))
    report.update({"updated_at": reported_at})

    if "request" not in report:
        report.update(state="crooked", reason="Falsified stream ID")
    else:
        report.update(state="reported")

    db.requests.update_one(
        {"_id": request_id},
        {"$set": report},
        upsert=True
    )
