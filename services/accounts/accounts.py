import os
import sys
sys.path.append(os.path.abspath("../../common"))

import time
from hashlib import md5
from datetime import datetime, timezone, timedelta

import pymongo
from pymongo import ReturnDocument

import tools
logger = tools.get_logger()
db = tools.get_mongo()
db.accounts.create_index("login", unique=True)
db.sessions.create_index([
    ("login", pymongo.ASCENDING),
    ("active", pymongo.ASCENDING),
    ("ip_address", pymongo.ASCENDING),
    ("created_at", pymongo.DESCENDING)
])

#logger.debug(f"ROUTER_ADDRESS: {os.environ.get('ROUTER_ADDRESS')}")
#logger.debug(f"LISTEN: {os.environ.get('LISTEN')}")

import grpc
import accounts_pb2, accounts_pb2_grpc
import georesolver_pb2, georesolver_pb2_grpc
import services_pb2, services_pb2_grpc

channel = grpc.insecure_channel(os.environ.get("ROUTER_ADDRESS"))
GeoResolver = georesolver_pb2_grpc.GeoResolverStub(channel)
Services = services_pb2_grpc.ServicesStub(channel)

import threading
tlocal = threading.local()
def create_mysql_pool():
    tlocal.my = tools.get_mysql()


class Accounts(accounts_pb2_grpc.AccountsServicer):
    def GetAccounts(self, GetAccountsReq, context):
        fields = {field: 1 for field in GetAccountsReq.fields.split(',')} \
            if GetAccountsReq.fields else None

        cursor = db.accounts.find({}, fields)
        total = cursor.count()

        cursor = cursor.sort("login")
        cursor = cursor.skip(GetAccountsReq.skip)
        cursor = cursor.limit(GetAccountsReq.limit)

        accounts = []
        for account in list(cursor):
            account["_id"] = str(account.pop("_id"))
            accounts.append(account)

        return accounts_pb2.GetAccountsRep(
            accounts=accounts,
            offset=GetAccountsReq.skip,
            count=len(accounts),
            total=total
        )

    def GetAccount(self, Account, context):
        account = self._load_account(Account.login)
        account or context.abort(grpc.StatusCode.NOT_FOUND, "")
        account["_id"] = str(account.pop("_id"))
        return tools.from_dict(account, accounts_pb2.Account)

    def updateAccount(self, Account, context):
        account = tools.to_dict(Account)
        login = account.pop("login")
        password = account.get("password")
        if password:
            logger.debug(f"updateAccount: Password for login {login} has been updated")
            db.sessions.remove({ "login": login })
            logger.debug(f"updateAccount: Old sessions for login {login} has been removed")
        account.pop("_id", None)
        db.accounts.update_one({ "login": login }, { "$set": account })
        return accounts_pb2.Account()

    def SessionCreate (self, SessionCreateReq, context):

        account = self._load_account(SessionCreateReq.login)
        # Check if account exists and it is enabled and password matches
        account or context.abort(grpc.StatusCode.NOT_FOUND, "")
        account["enabled"] or context.abort(grpc.StatusCode.FAILED_PRECONDITION, "")
        if md5(SessionCreateReq.password.encode()).hexdigest() != account["password"]:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "")

        account_login = SessionCreateReq.login

        # Create new session
        session = {
            "login": account_login,
            "user_agent": SessionCreateReq.user_agent,
            "ip_address": SessionCreateReq.ip_address,
            "created_at": datetime.now(timezone.utc),
            "location": None,
            "active": True
        }

        # Get user/account location
        try:
            reply = GeoResolver.GetLocation(
                georesolver_pb2.GetLocationReq(
                    ip_address=SessionCreateReq.ip_address
                )
            )
            logger.debug(f"[Account {account_login}] Location: {reply}")
            session["location"] = tools.to_dict(reply)
        except:
            logger.warning(f"[Account {account_login}] Location unknown")

        db.accounts.update_one(
            {"login": account_login},
            {"$set": {
                "ip_address": session["ip_address"],
                "location": session["location"]
            }}
        )

        result = db.sessions.insert_one(session)
        session["_id"] = str(result.inserted_id)
        session["created_at"] = str(session["created_at"])
        logger.info(f"[Account {account_login}] New session created: {session}")

        max_addresses = account["max_addresses"]
        max_streams = account["max_streams"]

        # Find all account's active IP(s)
        result = db.sessions.aggregate([
            { "$match": { "login": account_login, "active": True } },
            { "$group": { "_id": "$ip_address", "oid": {"$max": "$_id" } } },
            { "$sort": { "oid": pymongo.DESCENDING } }
        ])
        active_ips = [ doc["_id"] for doc in result ]
        logger.debug(f"[Account {account_login}] Active IPs: {active_ips}")

        # Get account's IP(s) exceeding max_addresses range
        forget_ips = active_ips[max_addresses:]
        logger.debug(f"[Account {account_login}] Forget IPs: {forget_ips}")

        # Get allowed account's IP(s) within max_addresses range
        allowed_ips = active_ips[:max_addresses]
        logger.debug(f"[Account {account_login}] Allowed IPs: {allowed_ips}")

#        if forget_ips:
#            result = db.sessions.update_many({
#                "login": account_login,
#                "ip_address": {"$in": forget_ips}
#            }, {
#                "$set": {"active": False}
#            })
#            logger.info(f"Removed {result.modified_count} old sessions of account {account_login}")

        # Remove account's expired session(s) exceeding max_addresses range
        if forget_ips:
            result = db.sessions.delete_many({
                "login": account_login,
                "ip_address": { "$in": forget_ips }
            })
            logger.info(f"[Account {account_login}] Removed {result.deleted_count} session(s) exceeding max_addresses={max_addresses} limit, IP(s): {forget_ips}")

        if allowed_ips:
            for aip in allowed_ips:
                # Find all expired account's session(s) ID exceeding max_streams limit
                result = db.sessions.aggregate([
                    {
                        "$match": {
                            "login": account_login,
                            "ip_address": aip
                        }
                    },
                    { "$sort": { "created_at": pymongo.DESCENDING } },
                    { "$limit": max_streams },
                    { "$group": { "_id": "$_id" } }
                ])
                # Remove all expired account's session(s) ID exceeding max_streams limit
                if result:
                    active_ids = [ doc["_id"] for doc in result ]
                    result = db.sessions.delete_many({
                        "login": account_login,
                        "ip_address": aip,
                        "_id": { "$not": { "$in": active_ids } }
                    })
                    if result.deleted_count:
                        logger.info(f"[Account {account_login}] Removed {result.deleted_count} session(s) exceeding max_streams={max_streams} limit per IP {aip}")

        return accounts_pb2.AccountSession(**session)


    def _load_account(self, login) -> dict:
        logger.debug(f"Account login: {login}")
        account = db.accounts.find_one({"login": login})
        if account:
            logger.debug(f"Loaded account: {account}")
            return account

        timeout = 2
        started = time.time()
        while not tlocal.my.is_connected():
            time.sleep(0.1)
            if time.time() - started > timeout:
                logger.warning(f"Waited for connection more than {timeout} seconds")
                break

        cursor = tlocal.my.cursor(dictionary=True, buffered=True)
        # dvr_colo_id: 11 (nld), 19 (dec)
        cursor.execute("""
            SELECT u.id AS user_id,
                a.active,
                u.login,
                u.pass AS password,
                u.account_id,
                r.age AS rating,
                u.timezone AS tz_offset,
                u.lastChannel AS channel_id,
                u.volume AS volume_level,
                u.channel_pass AS parent_code,
                u.collocation_id as live_colo_id,
                IF(u.sig_pult="grey", 11, 13) AS dvr_colo_id
            FROM iptv_Users AS u
            LEFT JOIN iptv_Accounts AS a ON a.id=u.account_id
            LEFT JOIN g_Rating AS r ON r.id=u.rating_id
            WHERE u.login=%s
        """, (login,))
        account = cursor.fetchone()
        cursor.close()

        logger.debug(f"Imported account: {account}")
        if not account:
            return

        account.update(
            login=int(account.pop("login")),
            enabled=bool(int(account.pop("active"))),
            max_streams=3,
            max_addresses=1,
            autocolo=True,
            ip_address=None,
            trusted=False,
            live_colo=None,
            dvr_colo=None,
#            last_access=datetime.now(timezone.utc),
            abuses={}
        )

        try:
            reply = Services.GetColo(
                services_pb2.Colo(
                    colo_id=account.pop("live_colo_id")
                )
            )
            account["live_colo"] = tools.to_dict(reply)
        except grpc.RpcError as e:
            logger.error(f"Could not get colocation for account {account['login']}")

        try:
            reply = Services.GetColo(
                services_pb2.Colo(
                    colo_id=account.pop("dvr_colo_id")
                )
            )
            account["dvr_colo"] = tools.to_dict(reply)
        except grpc.RpcError as e:
            logger.error(f"Could not get colocation for account {account['login']}")

        result = db.accounts.insert_one(account)
        account["_id"] = result.inserted_id

        return account


if __name__ == "__main__":
    from concurrent import futures
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=int(os.environ.get("WORKERS")),
        initializer=create_mysql_pool
    ))
    accounts_pb2_grpc.add_AccountsServicer_to_server(Accounts(), server)
    server.add_insecure_port("[::]:%s" % os.environ.get("LISTEN", 11421))
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        exit(0)
