# test_grpc.py
import grpc
import hyrch_serving_pb2
import hyrch_serving_pb2_grpc

channel = grpc.insecure_channel('localhost:50050')
stub = hyrch_serving_pb2_grpc.YoloServiceStub(channel)
print("Connection successful")