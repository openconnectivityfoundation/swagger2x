# Template: CoAPthon3 server (not secure)

## Introduction
The generated code acts as a none OCF Server acting as a simulator.
e.g. the server does not have code to interact with the sensors/actuators.
However the generated code stores the send information and returns the data on request.
The generated code is a good start to hook up all the hardware that that the product will contain.

The generated code is a CoAP server based on the CoAPthon3 python library.
Note that a modified version of CoAPthon3 will be needed:

https://github.com/WAvdBeek/CoAPthon3

This version works on:
- IPV6 (default)
- using the standard addresses & ports (not OCF addresses & ports)

# Generic concept
The template generates for each vertical resource a resource class.
The resource class will have an GET function and possibly a POST function if the resource is updatable.


# python client

CoAPthon3 also includes a generic client
run from the command line (bash) in the CoAPthon3 folder:

python3 coapclient.py -o GET -p  coap://[ ipv6 address]:port/oic/d -c 10000

The address of the server to use is printed on the console


# Security
This implementation is __NOT__ secure

# What is missing:
- Creation/deletion of resources (PUT/DELETE functions)
- Handling in get/post of:
    - recursively object, arrays of arrays, arrays of objects, object within objects





