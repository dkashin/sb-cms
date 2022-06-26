# import os
import sys
sys.path.append(os.path.abspath("../../common"))

import time
import mysql.connector

import tools
logger = tools.get_logger()

import threading
tlocal = threading.local()
def create_mysql_pool():
    tlocal.my = tools.get_mysql()

import grpc
import channels_pb2, channels_pb2_grpc
import services_pb2, services_pb2_grpc

channel = grpc.insecure_channel(os.environ.get("ROUTER_ADDRESS"))
Services = services_pb2_grpc.ServicesStub(channel)

from cachetools import TTLCache
cache = TTLCache(maxsize=400, ttl=20)

class Channels(channels_pb2_grpc.ChannelsServicer):
    def getAvailableStreams(self, Channel, context):
        if not "colos" in cache:
            cache["colos"] = {colo.name: colo for colo in
                Services.getColos(services_pb2.Nothing()).items
            }
        colos = cache["colos"]

        if not "services" in cache:
            cache["services"] = {s.service_id: s for s in
                Services.getServices(services_pb2.Nothing()).items
            }
        services = cache["services"]

        timeout = 2
        started = time.time()
        while not tlocal.my.is_connected():
            time.sleep(0.1)
            if time.time() - started > timeout:
                logger.warning(f"Waited for connection more than {timeout} seconds")
                break

        cursor = tlocal.my.cursor(dictionary=True, buffered=True)
        cursor.execute("""
            SELECT id, stream_address, external_service_id
            FROM btv_Channel_to_StreamSrc
            WHERE btv_channel_id=%s
        """, (Channel.channel_id,))

        for row in cursor:
            try:
                service = services[row["external_service_id"]]
                assert service.enabled
                assert colos[service.colo_name].enabled
            except (KeyError, AssertionError) as e:
                continue

            yield channels_pb2.Stream(
                stream_id=row["id"],
                name=row["stream_address"],
                enabled=True,  # Add `enabled` property to stream after migrating streams to mongo
                service=service
            )
        cursor.close()

    def getProgram(self, Program, context):
        timeout = 2
        started = time.time()
        while not tlocal.my.is_connected():
            time.sleep(0.1)
            if time.time() - started > timeout:
                logger.warning(f"Waited for connection more than {timeout} seconds")
                break

        try:
            cursor = tlocal.my.cursor(dictionary=True, buffered=True)
            cursor.execute(f"""
                SELECT
                    p.id AS program_id,
                    p.channel_id,
                    pl.name,
                    pl.description,
                    UNIX_TIMESTAMP(p.date_start) AS starts_at,
                    UNIX_TIMESTAMP(p.date_end) AS ends_at
                FROM btv_Programs AS p
                LEFT JOIN btv_ProgramLng AS pl ON pl.btv_program_id=p.id
                WHERE p.id={Program.program_id}
            """)

            program = cursor.fetchone()
            logger.debug(f"Fetched program: {program}")
            program or context.abort(grpc.StatusCode.NOT_FOUND, "")
        except mysql.connector.Error as e:
            logger.error(e)
            logger.debug(f"Sql executed: {cursor.statement}")
        finally:
            cursor.close()

        return channels_pb2.Program(**program)

    def findProgram(self, Program, context):
        timeout = 2
        started = time.time()
        while not tlocal.my.is_connected():
            time.sleep(0.1)
            if time.time() - started > timeout:
                logger.warning(f"Waited for connection more than {timeout} seconds")
                break

        try:
            cursor = tlocal.my.cursor(dictionary=True, buffered=True)
            cursor.execute(f"""
                SELECT
                    id AS program_id,
                    channel_id,
                    UNIX_TIMESTAMP(date_start) AS starts_at,
                    UNIX_TIMESTAMP(date_end) AS ends_at
                FROM btv_Programs
                WHERE channel_id={Program.channel_id}
                    AND FROM_UNIXTIME({Program.starts_at}) >= date_start
                    AND FROM_UNIXTIME({Program.starts_at}) < date_end
            """)

            program = cursor.fetchone()
            logger.debug(f"Fetched program: {program}")
            program or context.abort(grpc.StatusCode.NOT_FOUND, "")
        except mysql.connector.Error as e:
            logger.error(e)
            logger.debug(f"Sql executed: {cursor.statement}")
        finally:
            cursor.close()

        return channels_pb2.Program(**program)


if __name__ == "__main__":
    from concurrent import futures
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=int(os.environ.get("WORKERS")),
        initializer=create_mysql_pool
    ))
    channels_pb2_grpc.add_ChannelsServicer_to_server(Channels(), server)
    server.add_insecure_port("[::]:%s" % os.environ.get("LISTEN", 11421))
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        exit(0)
