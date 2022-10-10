
Specification
-----------

This solution supports macOS, to be more specific, it is developed and tested under macOS Version 12.3. 


- Please run the setup script by `chmod +x ./setup.sh` followed by `./setup.sh` to set up the system;
- Run the build script by `chmod +x ./build.sh` followed by `./build` to execute required build steps;
- Then, run the server and client with specified arguments discussed in `prompt.md`.
    - For example, `python3 server.py --host <host> --port <port>`
    - Then, `python3 client.py  --host <host> --port <port> --input <path to the input picture> --output <path to the output picture> [--mean]  [--rotate <NONE/NINETY_DEG/ONE_EIGHTY_DEG/TWO_SEVENTY_DEG>]`
- The processed picture will be generated in `<path to the output picture>`.