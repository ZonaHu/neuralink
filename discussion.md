
Discussion
-----------

- This is an interesting project to work on, I learned gRPC from scratch by studying the tutorials on [gRPC quick start guide
](https://grpc.io/docs/languages/python/quickstart/), which gave a lot of useful examples.
- gRPC uses HTTP/2, which multiplexes multiple calls on a single TCP connection.
- According to my research, due to the tight packing of the Protocol Buffers and the use of HTTP/2 by gRPC, gRPC is about 7 times faster than REST when receiving data, and approximately 10 times faster than REST when sending data for this specific payload.
- There are some limitations or known issues with my solution, 
- If I'm given more time and resources, I think we can use thread pooling, a software design pattern for achieving concurrency of execution, to improve efficiency. It should maintain multiple threads witing for tasks to be allocated for concurrent execution.
- Currently, I only made sure that the solution supports valid png and jpeg images as the prompt asked, but I would recommend supporting more types of images so for future development. 
