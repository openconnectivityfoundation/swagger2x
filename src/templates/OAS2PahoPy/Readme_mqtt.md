
# Template: PAHO MQTT OCF server

## Introduction

The template generates application level code for the OCF over MQTT using paho mqtt python.
The generated code acts as a OCF Server acting as a simulator.
e.g. the server does not have code to interact with the sensors/actuators.
However the generated code stores the send information and returns the data on request.
The generated code is a good start to hook up all the hardware that that the product will contain.

## Table of Contents

- [Template: PAHO MQTT OCF server](#template-paho-mqtt-ocf-server)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Generic concept](#generic-concept)
  - [What is generated](#what-is-generated)
    - [Introspection Device Data (IDD)](#introspection-device-data-idd)
  - [DeviceBuilder](#DeviceBuilder)
  - [Config file](#config-file)
  - [security](#security)

## Generic concept

The generated code is using global variable to store the induced changes by a Client.
The functions and global variable have a naming convention that allows that multiple resources of the same resource type can co-exist.

- The Server creates initial values at start up:
  - using the default/examples from the resource definition, and stores these initial values in global variables.
  - if default/example values are not available, then a fixed value is generated in the code.
- The Server handles incoming requests from a Client:
  - RETRIEVE (GET)
    - creates the response by using a python class containing member variables intialized at start up.
  - UPDATE (POST)
    - checks if the incoming request is valid
    - updates the class member variables by using the values of the incoming request
    - creates the response by using the member variables

- The UDN of the server generated at each start up.
- The UDN of the server is used for the MQTT clientid, e.g. making it unique.

## What is generated

- ocfmqtt_server.py implementation code (maybe renamed)
  function list:
  - main
    - Starts the platform
    - Register the device and platform resources
      - oic/d
      - oic/p
      - oic/res
      - introspection
    - Create all application specific resources in a class
    - creates an mqtt client
      - subscribes to OCF/[UDN]/#
      - subscribes to OCF/*/#
    - wait for incoming connections
  - Resource handling class (path dependend):
    - create_return_json
      - Function to convert the class member variables to the response document.
      - uses "if" to generate the appropriate set of return values
      - Handles JSON property types as part of the resource type specification:
        - boolean
        - integer
        - number
        - string
    - render_GET
      - uses create_return_json for returning data
    - render_POST
      - Function to convert the input request document to the member variables.
      - Checks if input is correct :
        - TODO No write to readOnly properties of the common and resource properties.
        - TODO No write to readOnly properties resource dependend.
        - TODO Properties of the correct type (using type in the struct).
        - TODO Properties in MIN/MAX range given in by schema.
          - e.g. __no check by property range__
        - TODO Strings are not too long for the allocated size.
        - TODO Array (bool, int, double, string) size equal or less than the allocated array size.
        - Note that not all possible checks are implemented.
               returns error if this is not satisfied.
        - Note that if error occurs, the global variable(s) are not assigned.
      - Handles property types:
        - boolean
        - integer
        - number
        - string
        - TODO array of booleans
        - TODO array of integers
        - TODO array of numbers
        - TODO array of strings
        - Returns the same information as "GET"
        - Handles query parameters - TODO
          - As strings
          - If there is an enum, the input value is checked against the enum
          - NOTE the code needs to be changed to add the behaviour of what the enum should do

### Introspection Device Data (IDD)

The IDD is generated, and can be imported in the code via:

- reading a file from disk in JSON format with name out_introspection_merged.swagger.json
- can be located in the same folder as the python file
- can be located 1 folder up in the hierarchy
  
The default setup is reading the IDD file from disk.

## DeviceBuilder

The device builder tool chain can be adapted to generate the python code.
The gen.sh contains information to enable the code generation for a server.
e.g. comment out the indicated line.

## Config file

The default config file is "mqtt.config". A specific config file can be loaded with option -rc.

Config file will read the configuration data for:
MQTT:

- Host the host name or ip address of the MQTT server
- port, server port to be used
- client_id, the client id, not set then a random uuid will be generated
- keepalive, the keep alive for the TCP/TLS connection

Security:

- cacerts, the file name of the certificate file.

The config file is read from the same location as the python script.

## security

commandline arguments are available to set the tls configuration if the mqtt server is secure.
