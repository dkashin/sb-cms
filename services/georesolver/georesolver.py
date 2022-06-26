import os
import sys
sys.path.append(os.path.abspath("../../common"))

import tools
logger = tools.get_logger()

import grpc
import georesolver_pb2, georesolver_pb2_grpc

import geoip2.database
from maxminddb import MODE_MEMORY


dir_path = os.path.dirname(os.path.realpath(__file__))
database = os.path.join(dir_path, 'GeoLite2-City.mmdb')
reader = geoip2.database.Reader(database, mode=MODE_MEMORY)


class GeoResolver(georesolver_pb2_grpc.GeoResolverServicer):
    def GetLocation(self, GetLocationReq, context):
        logger.debug("Got location request for %s" % GetLocationReq.ip_address)

        try:
            result = reader.city(GetLocationReq.ip_address)
            return georesolver_pb2.GeoLocation(
                country=result.country.name,
                city=result.city.name,
                gray=(result.country.iso_code in [ 'RU', 'UA', 'LT', 'LV' ])
            )
        except Exception as e:
            logger.error(e)
            return georesolver_pb2.GeoLocation()


if __name__ == "__main__":
    from concurrent import futures
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=int(os.environ.get("WORKERS"))
    ))
    georesolver_pb2_grpc.add_GeoResolverServicer_to_server(GeoResolver(), server)
    server.add_insecure_port("[::]:%s" % os.environ.get("LISTEN", 11421))
    server.start()

    try:
        import time
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        exit(0)
