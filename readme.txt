how to run the docker file:

change AMAZON and World ip port: in docker-deploy/myUPS/clent.py 

change world:
43 row: ip_port = ('vcm-25303.vm.duke.edu', 12345) #change this

change amazon:
59 row: server_port = ('0.0.0.0', 55555) #change this

command:
sudo docker-compose build
sudo docker-compose up

step: 
1. open the world
2.open UPS
3. open amazon

#UPS webpage :http://127.0.0.1:8000/
you can input tracknum to test

how to test:
see the output in terminal, we print all the instructions.


-------------------------google protobuf-----------------------------------------


how to use protobuf:

command to install:
pip install protobuf
sudo apt-install protobuf-compiler

how to write protocol:
https://developers.google.com/protocol-buffers/docs/pythontutorial

command to generate Your Protocol Buffers:
protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/[name_of_the_proto_file].proto


Protocol Buffers - Google's data interchange format
Copyright 2008 Google Inc.
https://developers.google.com/protocol-buffers/

This package contains a precompiled binary version of the protocol buffer
compiler (protoc). This binary is intended for users who want to use Protocol
Buffers in languages other than C++ but do not want to compile protoc
themselves. To install, simply place this binary somewhere in your PATH.

If you intend to use the included well known types then don't forget to
copy the contents of the 'include' directory somewhere as well, for example
into '/usr/local/include/'.

Please refer to our official github site for more installation instructions:
  https://github.com/protocolbuffers/protobuf
