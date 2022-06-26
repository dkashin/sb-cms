import os
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
import movies_pb2, movies_pb2_grpc


class Movies(movies_pb2_grpc.MoviesServicer):
    def getFileInfo(self, MovieFile, context):
        timeout = 2
        started = time.time()
        while not tlocal.my.is_connected():
            time.sleep(0.1)
            if time.time() - started > timeout:
                logger.warning(f"Waited for connection more than {timeout} seconds")
                break

        condition = f"id={MovieFile.file_id}" if MovieFile.file_id else f"vod_film_id={MovieFile.movie_id}"
        try:
            cursor = tlocal.my.cursor(dictionary=True, buffered=True)
            cursor.execute(f"""
                SELECT
                    id AS file_id,
                    vod_film_id AS movie_id,
                    filename,
                    70 AS service_id
                FROM external_ServicesFiles
                WHERE {condition}
            """)

            file = cursor.fetchone()
            logger.debug(f"Fetched file: {file}")
            file or context.abort(grpc.StatusCode.NOT_FOUND, "")
        except mysql.connector.Error as e:
            logger.error(e)
            if cursor:
                logger.debug(f"Sql executed: {cursor.statement}")
        finally:
            cursor.close()

        return movies_pb2.MovieFile(**file)


if __name__ == "__main__":
    from concurrent import futures
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=int(os.environ.get("WORKERS")),
        initializer=create_mysql_pool
    ))
    movies_pb2_grpc.add_MoviesServicer_to_server(Movies(), server)
    server.add_insecure_port("[::]:%s" % os.environ.get("LISTEN", 11421))
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        exit(0)
