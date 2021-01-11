# Template: IoTivity  OCF server

## Introduction

The template generates application level code for the IoTivity stack.
The generated code acts as a OCF Server acting as a simulator.
e.g. the server does not have code to interact with the sensors/actuators.
However the generated code stores the send information and returns the data on request.
The generated code is a good start to hook up all the hardware that that the product will contain.

## Table of Contents

- [Template: IoTivity  OCF server](#template-iotivity-ocf-server)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Generic concept](#generic-concept)
  - [What is generated](#what-is-generated)
  - [IoTivity](#iotivity)
    - [Introspection Device Data (IDD)](#introspection-device-data-idd)
  - [Onboarding on the secure domain](#onboarding-on-the-secure-domain)
  - [What is missing](#what-is-missing)
  - [Build instructions](#build-instructions)
    - [code repo](#code-repo)
    - [Windows](#windows)
  - [CTT instructions](#ctt-instructions)

## Generic concept

The code that can be generated takes into account the following layering.

![LiteStack](https://openconnectivityfoundation.github.io/swagger2x/data/lite-stack.png)

The generated code is using global variable to store the induced changes by a Client.
The functions and global variable have a naming convention that allows that multiple resources of the same resource type can co-exist.

- The Server creates initial values at start up:
  - using the default/examples from the resource definition, and stores these initial values in global variables.
  - if default/example values are not available, then a fixed value is generated in the code.
- The Server handles incoming requests from a Client:
  - RETRIEVE (GET)
    - creates the response by using the global variables intialized at start up.
  - UPDATE (POST)
    - checks if the incoming request is valid 
    - updates the global variables by using the values of the incoming request
    - creates the response by using the global variables

## What is generated

- simpleserver.c implementation code (maybe renamed)
  function list:
  - main
    - Starts the platform
    - Register the device and platform, e.g. initializes oic/d and oic/p
    - Create all application specific resources
    - Message pump
      - A loop that handles the incoming messages, e.g. handles the GET and POST requests
      – Calls the installed callbacks for each resource.
      - This loop makes sure that all access to the functions/global variables are not concurrent.
  - app_init
    - Function to create the OCF device.
      This function configures IoTivity stack with device information:
      - Device type
      - Device name
      - Data model versions
       and with platform information:
        - manufactorer (mnmn)
  - register_resources
    - Function  to register for each generated resource.
      It will register:
      - Resource Type (rt)
      - Interface (if), including the default interface
      - Indicates if the resource is discoverable (e.g. listed in oic/res)
      - Indicates if the resource is observable.
      - Sets the call backs to the resource handling functions
  - Resource handling functions:
    - get_&lt;resource path&gt;
      - Function to convert the global variables to the response document.
        - Note: always returns the same document, regardless of the  interface.
        - This works for testcase CT1.2.2.
        - Handles JSON property types as part of the resource type specification:
          - boolean
          - integer
          - number
          - string
          - object containing:
            - boolean
            - integer
            - number
            - string
            - array of strings
            - array of booleans
            - array of integers
            - array of numbers
            - array of strings
            - array of object
              - see object what an object can contain.
          - handles query parameters:
            - always as type of string.
            - Ff there is an enum, the input value is checked against the enum.
            - NOTE the code needs to be changed to add the behaviour of what the enum should do.
      - post_&lt;resource path&gt;
        - Function to convert the input request document to the member variables.
        - Checks if input is correct :
          - No write to readOnly properties of the common and resource properties.
          - No write to readOnly properties resource dependend.
          - Properties of the correct type (using type in the struct).
          - Properties in MIN/MAX range given in by schema.
            - e.g. __no check by property range__
          - Strings are not too long for the allocated size.
          - Array (bool, int, double, string) size equal or less than the allocated array size.
          - Note that not all possible checks are implemented.
               returns error if this is not satisfied.
          - Note that if error occurs, the global variable(s) are not assigned.
        - Handles property types:
          - boolean
          - integer
          - number
          - string
          - array of booleans
          - array of integers
          - array of numbers
          - array of strings
          - Returns the same information as "GET"
          - Handles query parameters
            - As strings
            - If there is an enum, the input value is checked against the enum
            - NOTE the code needs to be changed to add the behaviour of what the enum should do
  - Global variables.
    For each resource a set of global variables are created.
    Global variables exist for:
    - name of the property
    - value of the property
    - resource URL
    - resource type (rt)
      - array of strings.
      - including the # of strings in the array

## IoTivity

IoTivity already has a set of build-in resources.
These resources are not generated by the code, the generated code are configuring the build-in resources.
The build-in resources are:

- oic/res
- oic/p
- oic/d
- Security resources
- Introspection

### Introspection Device Data (IDD)

The IDD is generated, and can be imported in the code via:

- an header file.
- reading a file from disk
  
The default setup is reading the IDD file from disk.
The reading of the file (by means of std c library) is done from the generated code.

The header file option is available.
The header file is at &lt;installation folder&gt;/include/server_introspection.dat.h

## Onboarding on the secure domain

The following mechanisms are supported:

- Just Works
- Random Pin (can be compiled out)
  - with compile flage: OC_SECURITY_PIN
- PKI (can be compiled out)
  - with compile flag: OC_PKI
Note that the code stores the credential information under ./devicebuilderserver_creds

## What is missing

The following constructs/mechanisms are not supported:

- Creation/deletion of resources (PUT/DELETE functions)
- Handling in get/post of:
  - recursively arrays of arrays, arrays of objects, object within objects

## Build instructions

### code repo

The code repo of IoTivity is available [here](https://github.com/iotivity/iotivity-lite)

See also the folder iotivity-lite/port/&lt;port&gt; for more build instructions.

### Windows

- The generated file is renamed to the simpleserver_windows.c file in the apps folder.
  - The current file is kept (renamed).
- Use the existing visual studio project in folder &lt;installation folder&gt;/port/windows
- Note that there are multiple projects:
  - project for the library
  - project for the server
  - project for the server that is enabled for cloud

Note: to reduce the amount of debug information, remove OC_DEBUG from the compile flags in the property menu.
      please do this for the __library__.

## CTT instructions

- When CTT pops up: "reset to on-boarding state" means one needs to:
  - Stop the device
  - Delete all files in &lt;..&gt;/port/windows/devicebuilderserver_creds  
  - Start the server.
