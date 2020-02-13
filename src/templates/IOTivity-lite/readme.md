# Template: IOTivity Lite OCF server

The generated code acts as a OCF server acting as a simulator.
- The server creates initial values at start up 
  - using the default/examples from the resource definition, and stores these initial values in global variables.
- It handles incoming requests:
    - RETIEVE (GET)
        - creates the response by using the global variables intialized at start up.
    - UPDATE (POST)
        - checks if the incoming request is valid 
        - updates the global variables by using the values of the incoming request
        - creates the response by using the global variables
        
## What is generated:
- simpleserver.c implementation code
    - app_init
        - function to create the device
        - sets the type and which OCF spec is being used (default to OCF2.0)
    - global variables, for each property per resources
        - type 
        - naming convention g_&lt;resource&gt;_&lt;propertyname&gt;
        
    - functions:
        - get_&lt;resource&gt; 
            - function to convert the  member variables to the response document
            - note: always returns the same document, regardless of the interface
                - this works for testcase CT1.2.2
            - handles property types: 
                - boolean, 
                - integer,
                - number, 
                - string
                - object
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
                    - see object
            - handles query parameters
                - as strings
                - if there is an enum, the input value is checked against the enum
                - NOTE the code needs to be changed to add the behaviour of what the enum should do
        - post_&lt;resource&gt;
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
                
                
-PICS.json
    - PICT file that list the implemented resources in the generated code
      to be used with CTT
      
         
# Introspection IDD
The introspection IDD is handled via an header file.

The header file is at &lt;installation folder&gt;/include/server_introspection.dat.h

# Security
The following mechanisms are supported:
- just works
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
    



