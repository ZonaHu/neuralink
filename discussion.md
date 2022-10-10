
Discussion
-----------

- This is an interesting project to work on, I learned gRPC from scratch by studying the tutorials on [gRPC quick start guide
](https://grpc.io/docs/languages/python/quickstart/), which has provided a lot of useful examples.
- gRPC uses HTTP/2, which multiplexes multiple calls on a single TCP connection.
- According to my research, due to the tight packing of the Protocol Buffers and the use of HTTP/2 by gRPC, gRPC is about 7 times faster than REST when receiving data, and approximately 10 times faster than REST when sending data for this specific payload.
- There are some limitations or known issues with my solution.
  - Based on `image.proto`, a color can be grayscale or colored; if it is colored, the data is 3 channel rgb with the rgb triplets stored row-wise. Thus, in my solution, we checked if `target_image.mode == "RGB"`, which is comparing the image mode with the string `RGB`. However, there is also a four-channel format containing data for Red, Green, Blue, and an Alpha value, which is called "RGBA". We can change the code `target_image.mode == "RGB"` to checking if `(”RGB” in target_image.mode)`, so that it could also process `RGBA` pictures. Even though the prompt did not ask for supporting RGBA pictures, this change would allow it to support processing more pictures properly. 
  - If I'm given more time and resources, I think we can use thread pooling, a software design pattern for achieving concurrency of execution, to improve efficiency. It should maintain multiple threads witing for tasks to be allocated for concurrent execution. There is a [tutorial](https://www.tutorialspoint.com/concurrency_in_python/concurrency_in_python_pool_of_threads.htm) on this.
  - Currently, I only made sure that the solution supports valid png and jpeg images as the prompt asked, but I would recommend supporting more types of images so for future development. 
