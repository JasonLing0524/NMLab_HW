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

    def get(self, request):
    
        #ask server
        host = "localhost:8080"
        print(host)
        with grpc.insecure_channel(host) as channel:
            stub = fib_pb2_grpc.LogStub(channel)

            request = fib_pb2.LogRequest()
            request.n = 1;

            response = stub.Show(request)
            result = response.log
            history = []
            if result:
                history = result.split(' ')
                history = list(map(int, history))
        return Response(data={ 'history': history }, status=200)

