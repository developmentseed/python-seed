

from concurrent import futures
import os
import logging
import grpc
import datahub_pb2 as dh
import datahub_pb2_grpc as dh_rpc
from isharp.datahub.core import Matrix
from isharp.datahub.core import RevisionInfo
import pandas as pd
import time
import datetime

from isharp.datahub.broker_client.remote_proxy import BrokerConnectionPool


def addAndCommitChange(pricePoint:dh.PricePoint,seriesDate: datetime, url:str,matrix:Matrix):
    pass





class PatchApplier(dh_rpc.ApplyPatchServicer):



    def __init__(self) -> None:
        self.hub_host = os.getenv('isharp_hub_host', 'daphne174:5672')
        self.databroker = BrokerConnectionPool()


    def ApplyPatch(self, request:dh.PatchRequest, context):
        print(  "{}/{}".format(request.url,request.patch.pp.price)  )
        found = self.databroker.peek(request.url)

        if found:
            pricePoint = request.patch.pp
            seriesDate = datetime.datetime(year=pricePoint.year,month=pricePoint.month,day=pricePoint.date)

            matrix = self.databroker.checkout(request.url)
            df = matrix.content.append(pd.DataFrame(data=[pricePoint.price],
                                                    index=[seriesDate],
                                                    columns=matrix.content.columns))

            revision_info = RevisionInfo(who="Jeremy Ward", what=request.patch.comment,when=datetime.datetime.now())

            self.databroker.commit(matrix.replace_content(df), revision_info)

        return dh.PatchResponse(success=False)




def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dh_rpc.add_ApplyPatchServicer_to_server(PatchApplier(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
