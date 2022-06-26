import os
import sys
import operator
sys.path.append(os.path.abspath("../../common"))

from hashlib import md5
from base64 import b64encode
from urllib.parse import urlparse, parse_qs
from random import choice

import requests
from requests.exceptions import RequestException

import time
from datetime import datetime, timezone, timedelta

import pymongo
from bson.objectid import ObjectId

import streamers
import machines
import tools

logger = tools.get_logger()

db = tools.get_mongo()

db.accounts.create_index("login", unique=True)

db.requests.create_index("nid")
db.requests.create_index([
    ("login", pymongo.ASCENDING),
    ("requested_at", pymongo.DESCENDING)
])

db.sessions.create_index([
    ("login", pymongo.ASCENDING),
    ("active", pymongo.ASCENDING),
    ("ip_address", pymongo.ASCENDING)
])

from redis import Redis, StrictRedis
from rq import Queue
r = StrictRedis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
rq = Queue('requests', connection=Redis.from_url(os.environ.get("RQ_REDIS_URL")))

import grpc
import accounts_pb2, accounts_pb2_grpc
import channels_pb2, channels_pb2_grpc
import dispenser_pb2, dispenser_pb2_grpc
import georesolver_pb2, georesolver_pb2_grpc
import movies_pb2, movies_pb2_grpc
import services_pb2, services_pb2_grpc
import nimble_pb2
import accessresolver

channel = grpc.insecure_channel(os.environ.get("ROUTER_ADDRESS"))
Accounts = accounts_pb2_grpc.AccountsStub(channel)
Channels = channels_pb2_grpc.ChannelsStub(channel)
GeoResolver = georesolver_pb2_grpc.GeoResolverStub(channel)
Movies = movies_pb2_grpc.MoviesStub(channel)
Services = services_pb2_grpc.ServicesStub(channel)

from cachetools import TTLCache
cache = TTLCache(maxsize=800, ttl=20)


class Dispenser(dispenser_pb2_grpc.DispenserServicer):


    def SessionAuthCheck(self, StreamUrlReq, context, account):
        req_login = StreamUrlReq.login
        req_ip = StreamUrlReq.ip_address
        session_id = StreamUrlReq.session_id
        platform = StreamUrlReq.platform
        user_agent = StreamUrlReq.user_agent
        logger.debug(f"[SessionAuthCheck]: user_agent: {user_agent}, session_id: {session_id}, login: {req_login}")
#        if (req_login in range(268123, 276408)) or (req_login in [ 125, 215638 ]):
        if req_login in [ 109910, 215638 ]:
            geo_data = GeoResolver.GetLocation(
                georesolver_pb2.GetLocationReq(
                    ip_address=req_ip
                )
            )
            if geo_data:
                if geo_data.gray:
                    logger.warning(f"[SessionAuthCheck]: Request location is in gray zone ({geo_data.city}, {geo_data.country}) for the account {req_login}")
                    if not account.trusted:
                        logger.warning(f"[SessionAuthCheck]: Request location is not trusted ({geo_data.city}, {geo_data.country}) for the account {req_login}")
                        context.abort(grpc.StatusCode.FAILED_PRECONDITION, "The service is not available in this area")
            else:
                logger.warning(f"[SessionAuthCheck]: Request location is not available for the account {req_login}")

            # Disable SessionID check for platforms that are not providing required ObjectId/BSON format

            bad_platforms = [ "smarty", "oftmw" ]
#            bad_uas = [ "SmartTV", "SMART-TV", "SmartHub", "java 1.4" ]
            bad_uas = [ "Smart", "SMART", "java 1.4" ]
            if any(bp in platform for bp in bad_platforms) or any(ua in user_agent for ua in bad_uas):
#                s_count = db.sessions.count_documents({
#                    "login": req_login,
#                    "active": True
#                       "ip_address": req_ip,
#                       "created_at": { "$gt": (datetime.now(timezone.utc) - timedelta(days = 30)) }
#                })
                s_count = 1
            else:
                s_count = db.sessions.count_documents({
                    "_id": ObjectId(session_id),
                    "login": req_login,
                    "active": True
#                       "ip_address": req_ip,
#                       "created_at": { "$gt": (datetime.now(timezone.utc) - timedelta(days = 30)) }
                })
        else:
            s_count = 1
        if s_count:
            logger.debug(f"[SessionAuthCheck]: Found {s_count} active session(s) for account {req_login}, IP {req_ip}")
        else:
            logger.debug(f"[SessionAuthCheck]: No active session(s) found for account {req_login}, IP {req_ip}")
            context.abort(grpc.StatusCode.UNIMPLEMENTED, "Сеанс завершен. Пожалуйста, авторизуйтесь повторно.".encode('utf-8'))
#            context.abort(grpc.StatusCode.PERMISSION_DENIED, "No active session(s) found")
        return


    def getChannelStreamUrl(self, StreamUrlReq, context):

        try:
            account = Accounts.GetAccount(
                accounts_pb2.Account(login=StreamUrlReq.login)
            )
        except grpc.RpcError as e:
            logger.error(e.details())
            context.abort(e.code(), e.details())

#        account.last_access = datetime.now(timezone.utc)
#        Accounts.updateAccount(account)

        self.SessionAuthCheck(StreamUrlReq, context, account)

        if StreamUrlReq.time_start:
            logger.warning(f"[getChannelStreamUrl] Live URL requested, but time_start = {StreamUrlReq.time_start} is detected. Forwarding request to getProgramStreamUrl (login {StreamUrlReq.login})")
            return self.getProgramStreamUrl(StreamUrlReq, context, auth_passed = True)
        request_id = str(ObjectId())
        channel_id = StreamUrlReq.content_id
        logger.debug(f"Got channel ID: {channel_id}")
        try:
            colos = cache[f"{channel_id}streams"]
            #logger.debug(f"cached colos: {colos}")
        except KeyError:
            colos = {}
            for stream in Channels.getAvailableStreams(
                channels_pb2.Channel(channel_id=channel_id)):
                if stream.service.colo_name not in colos:
                    colos[stream.service.colo_name] = []
                colos[stream.service.colo_name].append(stream)
            logger.debug(f"Fetched colos: {colos}")
            cache[f"{channel_id}streams"] = colos

        try:
            stream = choice(colos[account.live_colo.name])
        except KeyError:
            try:
                stream = choice(choice(list(colos.values())))
                logger.warning(f"Channel {channel_id} not served from {account.live_colo.name} colo")
            except IndexError:
                logger.error(f"Channel {channel_id} not served at all")
                context.abort(grpc.StatusCode.FAILED_PRECONDITION, f"Channel {channel_id} not served at all")

        streamer = streamers.BaseStreamer.factory(stream.service)
        stream_url = streamer.create_live_url(request_id, StreamUrlReq.ip_address, stream.name, account.login)
        db.requests.insert_one({
            "_id": request_id,
            "login": account.login,
            "requested_at": datetime.now(timezone.utc),
            "channel_id": channel_id,
            "content_type": "channel",
            "platform": StreamUrlReq.platform,
            "session_id": StreamUrlReq.session_id,
            "request": {
                "ip_address": StreamUrlReq.ip_address,
                "user_agent": StreamUrlReq.user_agent,
                "stream_name": stream.name
            },
            "stream_url": stream_url,
            "colo_name": stream.service.colo_name
        })
        session_ids_key = f"login:{account.login}:sid"
        session_id_key = f"{session_ids_key}:{StreamUrlReq.session_id}"
        r.execute_command('ZADD', session_ids_key, 'NX', time.time(), StreamUrlReq.session_id)
        r.zremrangebyrank(session_ids_key, 0, -(account.max_streams + 1))
        r.set(session_id_key, str(request_id))
        r.expire(session_id_key, 86400)
        #logger.debug(f"session_id_key {session_id_key}")
        #logger.debug(f"request_id {request_id}")
        #logger.debug("session_id_key expire is 86400 sec")
        logger.debug(f"Generated url for login {StreamUrlReq.login} on {StreamUrlReq.platform}: {stream_url}")
        return dispenser_pb2.GetStreamUrlRep(stream_url=stream_url)


    def getMovieUrl(self, StreamUrlReq, context):
        MovieFileReq = movies_pb2.MovieFile(movie_id=StreamUrlReq.content_id)
        return self._create_movie_url(StreamUrlReq, MovieFileReq, context)


    def getMovieFileUrl(self, StreamUrlReq, context):
        MovieFileReq = movies_pb2.MovieFile(file_id=StreamUrlReq.content_id)
        return self._create_movie_url(StreamUrlReq, MovieFileReq, context)


    def _create_movie_url(self, StreamUrlReq, MovieFileReq, context):

        try:
            account = Accounts.GetAccount(
                accounts_pb2.Account(login=StreamUrlReq.login)
            )
        except grpc.RpcError as e:
            logger.error(e.details())
            context.abort(e.code(), e.details())

#        account.last_access = datetime.now(timezone.utc)
#        Accounts.updateAccount(account)

        self.SessionAuthCheck(StreamUrlReq, context, account)

        try:
            file = Movies.getFileInfo(MovieFileReq)
        except grpc.RpcError as e:
            logger.error(e.details())
            context.abort(e.code(), e.details())
        if not "services" in cache:
            cache["services"] = {s.service_id: s for s in
                Services.getServices(services_pb2.Nothing()).items
            }
        services = cache["services"]
        try:
            service = services[file.service_id]
        except KeyError:
            msg = f"No service {file.service_id} found for file {file.file_id}"
            logger.error(msg)
            context.abort(2, msg)
        request_id = str(ObjectId())
        streamer = streamers.BaseStreamer.factory(service)
        stream_url = streamer.create_movie_url(request_id, StreamUrlReq.ip_address, file.filename, account.login)
        db.requests.insert_one({
            "_id": request_id,
            "login": account.login,
            "requested_at": datetime.now(timezone.utc),
            "movie_id": file.movie_id,
            "content_type": "movie",
            "platform": StreamUrlReq.platform,
            "session_id": StreamUrlReq.session_id,
            "request": {
                "ip_address": StreamUrlReq.ip_address,
                "user_agent": StreamUrlReq.user_agent,
                "stream_name": file.filename
            },
            "stream_url": stream_url,
            "colo_name": service.colo_name
        })
        session_ids_key = f"login:{account.login}:sid"
        session_id_key = f"{session_ids_key}:{StreamUrlReq.session_id}"
        r.execute_command('ZADD', session_ids_key, 'NX', time.time(), StreamUrlReq.session_id)
        r.zremrangebyrank(session_ids_key, 0, -(account.max_streams + 1))
        r.set(session_id_key, str(request_id))
        r.expire(session_id_key, 86400)
        logger.debug(f"Generated url for login {StreamUrlReq.login} on {StreamUrlReq.platform}: {stream_url}")
        return dispenser_pb2.GetStreamUrlRep(stream_url=stream_url)


    def getProgramStreamUrl(self, StreamUrlReq, context, auth_passed = False):

        try:
            account = Accounts.GetAccount(
                accounts_pb2.Account(login=StreamUrlReq.login)
            )
        except grpc.RpcError as e:
            logger.error(e.details())
            context.abort(e.code(), e.details())

#        account.last_access = datetime.now(timezone.utc)
#        Accounts.updateAccount(account)

        if not auth_passed:
            self.SessionAuthCheck(StreamUrlReq, context, account)

        try:
            if StreamUrlReq.time_start:
                program = Channels.findProgram(
                    channels_pb2.Program(
                        channel_id=StreamUrlReq.content_id,
                        starts_at=StreamUrlReq.time_start
                    )
                )
                time_start = StreamUrlReq.time_start
            else:
                program = Channels.getProgram(
                    channels_pb2.Program(
                        program_id=StreamUrlReq.content_id
                    )
                )
                time_start = program.starts_at
        except grpc.RpcError as e:
            logger.error(e.details())
            context.abort(e.code(), e.details())

        logger.debug(f"Got program: {program}")

        # Get services list
        if not "services" in cache:
            cache["services"] = {
                s.service_id: s for s in Services.getServices(services_pb2.Nothing()).items
            }
        services = cache["services"]
        logger.debug(f"getProgramStreamUrl: DVR collocation name: \'{account.dvr_colo.name}\'")

        # Find DVR service from collocation
        dvr_services = [
            services[s] for s in services if services[s].colo_name == account.dvr_colo.name and services[s].enabled
        ]
        dvr_services.sort(key = lambda x: x.priority, reverse = True)
        logger.debug(f"getProgramStreamUrl: DVR collocation services: {dvr_services}")

        # Map channel data (alias)

        channels_map_premuim_ssd = {
            852: 665, # Матч! Премьер HD+
            813: 517, # Домашний Premium+
            853: 479, # Eurosport 1 HD+
            854: 480, # Eurosport 2 HD+
            379: 433  # Vox+
        }

        channels_map_premuim_sas = {
            805: 481, # Первый Premium+
            800: 659, # Первый HD Premium+
            806: 504, # Первый международный Premium+
            807: 506, # Россия 1 Premium+
            797: 660, # Россия 1 HD Premium+
            808: 507, # РТР Планета Premium+
            809: 509, # НТВ Premium+
            798: 110, # НТВ HD Premium+
            811: 513, # СТС Premium+
            812: 515, # ТНТ Premium+
            819: 736, # ТНТ HD Premium+
            813: 517, # Домашний Premium+
            519: 445, # ТВ Центр Premium+
            814: 521, # ТВ 3 Premium+
            523: 815, # Рен ТВ Premium+
            527: 816, # Матч! ТВ Premium+
            394: 236, # Матч! ТВ HD Premium+
            625: 804, # Матч! Игра HD Premium+
            540: 803, # Матч! Арена HD Premium+
            616: 801, # МАТЧ! Футбол 1 FHD+
            617: 802, # МАТЧ! Футбол 2 FHD+
            618: 799, # МАТЧ! Футбол 3 FHD+
            852: 665, # Матч! Премьер HD+
            670: 581, # МАТЧ! Боец Premium+
            853: 479, # Eurosport 1 HD+
            854: 480, # Eurosport 2 HD+
            452: 641, # Cartoon Network+
            402: 632, # Nickelodeon+
            233: 639, # Disney Channel+
            423: 615, # TV1000+
            621: 633, # TV1000 Русское кино+
            857: 565, # TV1000 Action+
            454: 538, # Русский Роман Premium+
            249: 536, # Русский детектив Premium+
            567: 823, # ZDF HD+
            566: 824, # Das Erste HD+
            376: 825, # RTL HD+
            379: 433  # Vox+
        }

        channels_map_hq = {
            740: 504, # Первый международный HQ
            741: 507, # РТР Планета HQ
            109: 535, # Россия 24 HQ
            735: 511, # Россия К HQ
            748: 333, # 5 канал HQ
            746: 517, # Домашний HQ
            744: 445, # ТВ Центр HQ
            127: 646, # Телеканал 78 HQ
            745: 521, # ТВ 3 HQ
            738: 815, # Рен ТВ HQ
            737: 525, # Че HQ
            189: 683, # РБК HQ
            137: 684, # BBC World News HQ
            467: 749, # Euronews HQ
            145: 671, # Русский Экстрим HQ
            100: 705, # Футбол HQ
            102: 596, # Матч! Страна HQ
            121: 644, # Карусель HQ
            106: 641, # Cartoon Network HQ
            161: 650, # JimJam HQ
            103: 639, # Disney Channel HQ
            129: 674, # Пятница HQ
            131: 669, # Ю ТВ HQ
            140: 734, # Телеканал 2x2 HQ
            155: 704, # Ностальгия HQ
            182: 642, # Сарафан ТВ HQ
            144: 675, # ТНТ-Music HQ
            171: 686, # Шансон ТВ HQ
            160: 676, # Музыка первого HQ
            95: 677, # Europa Plus TV HQ
            190: 292, # BRIDGE TV Русский Хит HQ
            192: 691, # Bridge TV HQ
            148: 693, # Ля-Минор HQ
            147: 706, # Русская ночь HQ
            154: 645, # Дом кино HQ
            184: 703, # КИНОСЕРИЯ HQ
            98: 702, # Индия ТВ HQ
            425: 538, # Русский Роман HQ
            183: 687, # НСТ(Настоящее Страшное Телевидение) HQ
            167: 716, # Russian Travel Guide HQ
            143: 640, # Звезда HQ
            158: 718, # Время HQ
            146: 708, # Авто Плюс HQ
            194: 690, # 365 Дней HQ
            150: 707, # Кухня ТВ HQ
            151: 709  # Телекафе HQ
        }

        channels_map_test = {
            974: 758, # ТНТ4
            975: 110, # НТВ HD
            976: 919, # НТВ Хит
            977: 481, # Первый
            978: 747  # СТС HD
        }

        cid = channels_map_premuim_ssd.get(program.channel_id, program.channel_id)
        cid = channels_map_hq.get(program.channel_id, cid)
        cid = channels_map_test.get(program.channel_id, cid)

        stream_url = None
        user_agent = StreamUrlReq.user_agent

        if any(map(user_agent.__contains__, [ "Web0S", "Tizen" ])):
            device_class = 'SmartTV'
        else:
            device_class = 'Generic'

        legacy_ua = [ "Dune", "v2.8", "java 1.4", "Maple2012", "Maple2013", "Maple2014", "MAG", "Windows client", "NetCast.TV-2013", "NetCast.TV-2012", "NovoeTV Mobile", "Chrome/3", "Chrome/4", "Large Screen WebAppManager" ]

        for dvr_service in dvr_services:

            duration = program.ends_at - program.starts_at

            logger.debug(f"getProgramStreamUrl: Channel ID: {cid}")
            logger.debug(f"getProgramStreamUrl: DVR service type: \'{dvr_service.handler}\'")
            dvr_app = 'abr_ssd'
            if any(ds in dvr_service.handler for ds in [ 'nimble', 'cdn' ]):
                # Patches for missing Nimble DVR parts (UTC format)
#                if (time_start in range(1605564000, 1605567600)):
#                    continue
#                if (cid == 343) and (time_start < 1605567600):
#                    continue
                if (time.time() - time_start) < (11 * 24 * 3600) - 60:
                    dvr_app = 'abr_ssd'
                    if (device_class == 'SmartTV') and ((time_start + duration + 60) > time.time()):
                        dvr_app = 'abr_ssd_legacy'
                    if any(ua in user_agent for ua in legacy_ua):
                        dvr_app = 'abr_ssd_legacy'
                else:
                    dvr_app = 'abr_sas'
                    cid = channels_map_premuim_sas.get(program.channel_id, cid)
                    if (device_class == 'SmartTV') and ((time_start + duration + 60) > time.time()):
                        dvr_app = 'abr_sas_legacy'
                    if any(ua in user_agent for ua in legacy_ua):
                        dvr_app = 'abr_sas_legacy'

            stream_name = f"ch-{cid}"
            request_id = str(ObjectId())
            streamer = streamers.BaseStreamer.factory(dvr_service)
            stream_url = streamer.create_dvr_url(request_id, StreamUrlReq.ip_address, stream_name, dvr_app, time_start, duration, StreamUrlReq.force_hls, StreamUrlReq.login, StreamUrlReq.platform, device_class)

            if stream_url:
#                if self.StreamCheckDVR('http://' + stream_url):
#                if self.StreamCheck('http://' + stream_url):
                break

        if stream_url:
            db.requests.insert_one({
                "_id": request_id,
                "login": account.login,
                "requested_at": datetime.now(timezone.utc),
                "program_id": program.program_id,
                "channel_id": program.channel_id,
                "content_type": "program",
                "platform": StreamUrlReq.platform,
                "session_id": StreamUrlReq.session_id,
                "request": {
                    "ip_address": StreamUrlReq.ip_address,
                    "user_agent": StreamUrlReq.user_agent,
                    "stream_path": stream_name
                },
                "stream_url": stream_url,
                "colo_name": account.dvr_colo.name
            })
            logger.debug(f"Generated url for login {StreamUrlReq.login} on {StreamUrlReq.platform}: {stream_url}")
        else:
            context.abort(grpc.StatusCode.INTERNAL, 'DVR service is not available')

        return dispenser_pb2.GetStreamUrlRep(
            stream_url=stream_url
        )

    # Live Stream check
    def StreamCheck(self, url = None, headers = None, auth = None, timeout = 3):
        try:
            r = requests.head(url, headers = headers, auth = auth, timeout = timeout)
            code = r.status_code
            logger.debug(f"StreamCheck: URL: HTTP {code}")
            if code >= 200 and code < 400:
                return True
        except RequestException as e:
            logger.debug(f"StreamCheck: Exception error {e}")
        except:
            logger.debug(f"StreamCheck: Exception error")
        return False

    # DVR Stream check
    def StreamCheckDVR(self, url = None, headers = None, auth = None, timeout = 3):
        try:
            r = requests.get(url, headers = headers, auth = auth, timeout = timeout)
            logger.debug(f"StreamCheckDVR: HTTP {code}")
            logger.debug(f"StreamCheckDVR: HTTP Text {r.text}")
            if code >= 200 and code < 400:
                return True
        except RequestException as e:
            logger.debug(f"StreamCheckDVR: Exception error {e}")
        except:
            logger.debug(f"StreamCheckDVR: Exception error")
        return False


    def storeNimbleReport(self, NimbleReportReq, context):
        deny_list = []
        if os.environ.get("AUTH_FEEDBACK"):
            reject_key = f"nimble:{NimbleReportReq.vhost}:reject"
            deny_list = list(r.smembers(reject_key))
            r.delete(reject_key)

        rq.enqueue(
            accessresolver.handle_nimble_report,
            NimbleReportReq,
            datetime.now(timezone.utc),
            result_ttl=0
        )
        return nimble_pb2.NimbleReportRep(DenyList=dict(ID=deny_list))


    def storeFlussonicReport(self, FlussonicReportReq, context):
        rq.enqueue(
            accessresolver.handle_flussonic_report,
            FlussonicReportReq,
            datetime.now(timezone.utc),
            result_ttl=0
        )
        return dispenser_pb2.FlussonicReportRep()


### Legacy code notice start.
### The code below will be disabled in future releases.

    def reportColoAbuse(self, GetStreamUrlRep, context):

        # Temporary disable colo abuse code
        return dispenser_pb2.ColoAbuseRep()

        logger.debug("reportColoAbuse: Activated")
        logger.debug(f"reportColoAbuse: stream_url {GetStreamUrlRep.stream_url}")
        queryargs = urlparse(GetStreamUrlRep.stream_url).query
        logger.debug(f"reportColoAbuse: queryargs {queryargs}")
        token = parse_qs(queryargs)["token"][0]
        logger.debug(f"reportColoAbuse: Got token {token}")

        request = db.requests.find_one({"_id": str(ObjectId(token))})
        request or context.abort(grpc.StatusCode.NOT_FOUND, "")
        logger.debug(f"reportColoAbuse: Fetched request {request}")

        account = Accounts.GetAccount(
            accounts_pb2.Account(login=request["login"])
        )
        logger.debug(f"reportColoAbuse: Loaded account {account}")
        if not account.autocolo:
            logger.debug("reportColoAbuse: AutoColo is disabled for this account")
            context.abort(grpc.StatusCode.FAILED_PRECONDITION, "")

        field = "dvr_colo" if request["content_type"] == "program" else "live_colo"

        if tools.to_dict(account)[field]["name"] != request["colo_name"]:
            logger.debug(f"reportColoAbuse: {field} abuse created")
            return dispenser_pb2.ColoAbuseRep()

        timestamps = account.abuses[request["colo_name"]].timestamps
        timestamps.append(int(time.time())) # just a reference

        last_15_minutes_abuses = [ts for ts in timestamps if time.time() - ts < 60 * 15]

        if len(last_15_minutes_abuses) < 2:
            Accounts.updateAccount(account)
            logger.debug(f"reportColoAbuse: {field} abuse created")

        timestamps[:] = []
        if field == "dvr_colo":
            machine = machines.DVR(account.dvr_colo.name)
            machine.advance()
            account.dvr_colo.name = machine.state
            logger.debug(f"reportColoAbuse: Switching dvr_colo: {account.dvr_colo.name} -> {machine.state}")
        else:
            reply = GeoResolver.GetLocation(
                georesolver_pb2.GetLocationReq(
                    ip_address=request["request"]["ip_address"]
                )
            )
            if reply.country == "Netherlands":
                nearest = "nld"
            else:
                nearest = "deu"
            machine = machines.Live(account.live_colo.name, nearest)
            machine.advance()
            account.live_colo.name = machine.state
            logger.debug(f"reportColoAbuse: Switching live_colo: {account.live_colo.name} -> {machine.state}")

        Accounts.updateAccount(account)
#        return dispenser_pb2.ColoAbuseRep(do="reload_stream")
        return dispenser_pb2.ColoAbuseRep()

### Legacy code notice end.


if __name__ == "__main__":
    from concurrent import futures
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=int(os.environ.get("WORKERS"))
    ))
    dispenser_pb2_grpc.add_DispenserServicer_to_server(Dispenser(), server)
    server.add_insecure_port("[::]:%s" % os.environ.get("LISTEN", 11421))
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        exit(0)
