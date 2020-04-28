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
- IPV4 (not checked on IPV6)
- using the standard addresses & ports (not OCF addresses & ports)

# Generic concept
The template generates for each vertical resource a resource class.
The resource class will have an GET function and possibly a POST function if the resource is updatable.


# Security
This implementation is __NOT__ secure

# What is missing:
- Creation/deletion of resources (PUT/DELETE functions)
- Handling in get/post of:
    - recursively object, arrays of arrays, arrays of objects, object within objects





