from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../build/service/")
sys.path.insert(0, BUILD_DIR)

import grpc
import fib_pb2
import fib_pb2_grpc

import psutil
import paho.mqtt.client as mqtt



# Create your views here.
class EchoView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        order = int(request.data['order'])
        
        # ask solver
        host = "localhost:8080"
        print(host)
        with grpc.insecure_channel(host) as channel:
            stub = fib_pb2_grpc.FibCalculatorStub(channel)

            request = fib_pb2.FibRequest()
            request.order = order

            response = stub.Compute(request)
            result = response.value
        
        # log
        client = mqtt.Client()
        client.connect(host='localhost', port=1883)
        #client.loop_start()
        
        client.publish(topic='history', payload=str(order))
        
        return Response(data={ 'result': result }, status=200)

