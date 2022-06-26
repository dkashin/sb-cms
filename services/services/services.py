import os
import sys
sys.path.append(os.path.abspath("../../common"))

import tools
logger = tools.get_logger()
db = tools.get_mongo()

import grpc
import services_pb2, services_pb2_grpc


class Services(services_pb2_grpc.ServicesServicer):
    def getColos(self, Nothing, context):
        colos = []
        for colo in db.colocations.find():
            colo["_id"] = str(colo.pop("_id"))
            colos.append(colo)

        return services_pb2.GetColosRep(items=colos, total=len(colos))

    def GetColo(self, Colo, context):
        colo = db.colocations.find_one(tools.to_dict(Colo))
        colo or context.abort(grpc.StatusCode.NOT_FOUND, "")
        colo["_id"] = str(colo.pop("_id"))
        return services_pb2.Colo(**colo)

    def getServices(self, Nothing, context):
        items = []
        for item in db.services.find():
            item["_id"] = str(item.pop("_id"))
            items.append(item)
        #logger.debug(str(items))
        return services_pb2.GetServicesRep(items=items, total=len(items))


if __name__ == "__main__":
    from concurrent import futures
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=int(os.environ.get("WORKERS"))
    ))
    services_pb2_grpc.add_ServicesServicer_to_server(Services(), server)
    server.add_insecure_port("[::]:%s" % os.environ.get("LISTEN", 11421))
    server.start()

    try:
        import time
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        exit(0)
