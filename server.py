import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
from concurrent import futures
import fib_pb2
import fib_pb2_grpc

class LogServicer(fib_pb2_grpc.LogServicer):

    def __init__(self):
        pass
        
    def Show(self, request, context):
        response = fib_pb2.LogResponse()
        f = open("log.txt", 'r')
        response.log = f.read()
        if response.log:
            response.log = response.log[:-1]
        f.close()
        return response


class FibCalculatorServicer(fib_pb2_grpc.FibCalculatorServicer):

    def __init__(self):
        pass

    def Compute(self, request, context):
        n = request.order
        value = self._fibonacci(n)

        response = fib_pb2.FibResponse()
        response.value = value

        return response

    def _fibonacci(self, n):
        a = 0
        b = 1
        if n < 0:
            return 0
        elif n == 0:
            return 0
        elif n == 1:
            return b
        else:
            for i in range(1, n):
                c = a + b
                a = b
                b = c
            return b


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", type=str)
    parser.add_argument("--port", default=8080, type=int)
    args = vars(parser.parse_args())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer1 = FibCalculatorServicer()
    servicer2 = LogServicer()
    fib_pb2_grpc.add_FibCalculatorServicer_to_server(servicer1, server)
    fib_pb2_grpc.add_LogServicer_to_server(servicer2, server)

    try:
        server.add_insecure_port(f"{args['ip']}:{args['port']}")
        server.start()
        print(f"Run gRPC Server at {args['ip']}:{args['port']}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass
