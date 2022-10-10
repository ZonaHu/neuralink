from __future__ import print_function
import argparse
import grp
import io

import logging

import grpc
import image_pb2
import image_pb2_grpc

from PIL import Image


class Client:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.channel = grpc.insecure_channel('{0}:{1}'.format(host, port))
        self.stub = image_pb2_grpc.NLImageServiceStub(self.channel)

    def rotateImage(self, image_path, rotatation):
        target_image = Image.open(image_path)
        image_bytes = io.BytesIO()
        target_image.save(image_bytes, format=target_image.format)

        # Parse Rotation
        rotate = {
            "NONE": image_pb2.NLImageRotateRequest.Rotation.NONE,
            "NINETY_DEG": image_pb2.NLImageRotateRequest.Rotation.NINETY_DEG,
            "ONE_EIGHTY_DEG": image_pb2.NLImageRotateRequest.Rotation.ONE_EIGHTY_DEG,
            "TWO_SEVENTY_DEG": image_pb2.NLImageRotateRequest.Rotation.TWO_SEVENTY_DEG,
        }

        request = image_pb2.NLImageRotateRequest(
            rotation=rotate[rotatation],
            image=image_pb2.NLImage(
                color=(target_image.mode == "RGB"),
                data=image_bytes.getvalue(),
                width=target_image.width,
                height=target_image.height
            )
        )
        response = self.stub.RotateImage(request)
        return response

    def meanImage(self, image_path):
        target_image = Image.open(image_path)
        image_bytes = io.BytesIO()
        target_image.save(image_bytes, format=target_image.format)

        request = image_pb2.NLImage(
            color=(target_image.mode == "RGB"),
            data=image_bytes.getvalue(),
            width=target_image.width,
            height=target_image.height
        )

        response = self.stub.MeanFilter(request)
        return response

    def saveImage(self, response, path):
        image = Image.open(io.BytesIO(response.data))
        image.save(path)


if __name__ == '__main__':
    logging.basicConfig()
    parser = argparse.ArgumentParser(description='Argument parsing')
    parser.add_argument('--port', type=str, required=True)
    parser.add_argument('--host', type=str, required=True)
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)
    parser.add_argument('--rotate', type=str)
    parser.add_argument('--mean', action='store_true')
    args = parser.parse_args()
    c = Client(args.host, args.port)
    if args.mean:
        res = c.meanImage(args.input)
        c.saveImage(res, args.output)
    if args.rotate:
        if args.mean:
            res1 = c.rotateImage(args.output, args.rotate)
            c.saveImage(res1, args.output)
        else:
            res1 = c.rotateImage(args.input, args.rotate)
            c.saveImage(res1, args.output)
