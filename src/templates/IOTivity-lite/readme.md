# Template: IOTivity Lite OCF server

## Introduction
The generated code acts as a OCF Server acting as a simulator.
e.g. the server does not have code to interact with the sensors/actuators.
However the generated code stores the send information and returns the data on request.
The generated code is a good start to hook up all the hardware that that the product will contain.

# Generic concept
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
        
## What is generated:
- simpleserver.c implementation code
  function list:
    - main
      - starts the platform
      - Register the device and platform, e.g. initializes oic/d and oic/p
      - Create all application specific resources
      - Message pump
        - A loop that handles the incoming messages, e.g. handles the GET and POST requests
          – Calls the installed callbacks for each resource.
        - This loop makes sure that all access to the functions/global variables are not
concurrent.

    - app_init
        - function to create the OCF device
        this function configures IoTivity-Lite with device information:
          - Device type
          - Device name
          - Data model versions
       and with platform information:
          - manufactorer (mnmn)
          
    - register_resources 
      - function  to register for each generated resource
      it will register:
        - Resource Type (rt)
        - Interface (if), including the default interface
        - indicates if the resource is discoverable (e.g. listed in oic/res)
        - indicates if the resource is observable.
        - sets the call backs to the resource handling functions
        
    - Resource handling functions:
        - get_&lt;resource path&gt; 
            - function to convert the global variables to the response document.
            - note: always returns the same document, regardless of the interface
                - this works for testcase CT1.2.2
            - handles JSON property types as part of the resource type specification: 
                - boolean, 
                - integer,
                - number, 
                - string
                - object containing:
                    - boolean
                    - integer
                    - number
                    - string
                    - array of strings
                - array of booleans,
                - array of integers,
                - array of numbers,
                - array of strings
                - array of object
                    - see object what an object can contain.
            - handles query parameters
                - as type of strings
                - if there is an enum, the input value is checked against the enum
                - NOTE the code needs to be changed to add the behaviour of what the enum should do
        - post_&lt;resource path&gt;
            - function to convert the input request document to the member variables
            - checks if input is correct :
                - no write to readOnly properties of the common and resource properties.
                - no write to readOnly properties resource dependend
                - properties of the correct type (using type in the struct)
                - properties in MIN/MAX range given in by schema 
                    - e.g. __no check by property range__
                - strings are not too long for the allocated size
                - array (bool, int, double, string) size equal or less than the allocated array size
                - note that not all possible checks are implemented.
               returns error if this is not satisfied.
                    - note that if error occurs, the global variable(s) are not assigned.
            - handles property types: 
                - boolean, 
                - integer,
                - number, 
                - string,
                - array of booleans,
                - array of integers,
                - array of numbers,
                - array of strings
            - returns the same information as "GET"
            - handles query parameters
                - as strings
                - if there is an enum, the input value is checked against the enum
                - NOTE the code needs to be changed to add the behaviour of what the enum should do
                
                       
    - global variables, for each property per resources
        for each resource a set of global variables are created.
        global variables exist for:
        - name of the property
        - value of the property
        - resource URL
        - resource type (rt)
          - array of strings.
          - including the # of strings in the array
        - supported interfaces (if)
          - array of strings
          - including the # of strings in the array
        naming convention g_&lt;resource path&gt;_RESOURCE_PROPERTY_NAME_&lt;propertyname&gt;
        
-PICS.json

    PICT file that list the implemented resources in the generated code
      to be used with CTT. Note: generated file not up to date.
      
## IoTivity_lite
IoTivity Lite already has a set of build-in resources.
These resources are not generated by the code, the generated code are configuring the build-in resources.
The build-in resources are:
- oic/res
- oic/p
- oic/d
- Security resources
- Introspection


### Introspection IDD
The introspection IDD is handled via an header file.

The header file is at &lt;installation folder&gt;/include/server_introspection.dat.h



# Security
The following mechanisms are supported:
- just works (can be compiled out)
- random pin (can be compiled out)
- pki (can be compiled out)
note that the code stores the credential information under ./devicebuilderserver_creds

# What is missing:
- Creation/deletion of resources (PUT/DELETE functions)
- Handling in get/post of:
    - recursively arrays of arrays, arrays of objects, object within objects

    
# Building instructions
## code repo
The code repo of IOTivity lite is available at:

https://github.com/iotivity/iotivity-lite 

see iotivity-constrained/port/&lt;port&gt; for more instructions.

## Windows:
- the generated file is renamed to the simpleserver_windows.c file in the apps folder.
    - current file is kept.
- use the existing visual studio project in folder &lt;installation folder&gt;/port/windows
- note that there are multiple projects: 
    - project for the library,
    - project for the server 

Note: to reduce the amount of debug information, remove OC_DEBUG from the compile flags in the property menu.
      please do this for the __library__.
    
# CTT instructions
- When CTT pops up: "reset to on-boarding state" means one needs to:
  - stop the device
  - delete all files in port/windows/devicebuilderserver_creds  
  - start the server.
    



