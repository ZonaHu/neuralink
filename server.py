#!/usr/bin/python3
from concurrent import futures
import grpc
import argparse
import logging
import cv2
import numpy as np
import image_pb2_grpc
import image_pb2

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class NLImageService(image_pb2_grpc.NLImageServiceServicer):
    def __init__(self):
        self.CV_ROTATE_ENUMS = {
            image_pb2.NLImageRotateRequest.Rotation.NINETY_DEG: cv2.ROTATE_90_COUNTERCLOCKWISE,
            image_pb2.NLImageRotateRequest.Rotation.ONE_EIGHTY_DEG: cv2.ROTATE_180,
            image_pb2.NLImageRotateRequest.Rotation.TWO_SEVENTY_DEG: cv2.ROTATE_90_CLOCKWISE,
        }

    def RotateImage(self, request, context):
        if request.rotation == image_pb2.NLImageRotateRequest.Rotation.NONE:
            return request.image
        image = self.parseImage(request.image)
        rotate_deg = self.CV_ROTATE_ENUMS[request.rotation]
        rotated_image = cv2.rotate(
            image, self.CV_ROTATE_ENUMS[request.rotation])
        result = cv2.imencode(".PNG", rotated_image)[1]
        resultBytes = result.tobytes()

        new_width = request.image.width
        new_height = request.image.height
        if rotate_deg != cv2.ROTATE_180:
            new_width = request.image.height
            new_height = request.image.width

        return image_pb2.NLImage(
            color=request.image.color,
            data=resultBytes,
            width=new_width,
            height=new_height
        )

    def MeanFilter(self, request, context):
        K = 15

        image = self.parseImage(request)
        mean_image = cv2.blur(image, (K, K))
        result = cv2.imencode(".PNG", mean_image)[1]
        resultBytes = result.tobytes()
        response = request
        response.data = resultBytes

        return response

    def parseImage(self, request):
        image_bytes = np.frombuffer(request.data, np.uint8)
        color = None
        if request.color is True:
            color = cv2.IMREAD_COLOR
        else:
            color = cv2.IMREAD_GRAYSCALE
        return cv2.imdecode(image_bytes, color)


def serve(host, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_pb2_grpc.add_NLImageServiceServicer_to_server(
        NLImageService(), server)
    server.add_insecure_port("{0}:{1}".format(host, port))
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Argument parsing")
    parser.add_argument("--host", type=str, required=True)
    parser.add_argument("--port", type=int, required=True)

    args = parser.parse_args()
    serve(args.host, args.port)
