# Template: IOTivity Lite C server


The generated code acts as a simulator:
- the server creates (initial) values at start up (from default/examples)
- handles incomming requests (GET/POST)
    - stores the values on POST
    - respond on GET by handing out the stored values

## what is generated:
- simpleserver.c implementation code
    - app_init
        - function to create the device
        - sets the type and which OCF spec is being used (default to OCF1.3)
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
                - array of booleans,
                - array of integers,
                - array of numbers,
                - array of strings
        - post_&lt;resource&gt;
            - function to convert the input request document to the member variables
            - checks if input is correct :
                - no write to readOnly properties
                - properties of the correct type (using type in the struct)
                - properties in MIN/MAX range given in by schema 
                    - e.g. __no check by property range__
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
                
                
-PICS.json
    - PICT file that list the implemented resources in the generated code
      to be used with CTT
      
         
# Introspection IDD
The introspection IDD is handled via an header file.

The header file is at &lt;installation folder&gt;/include/server_introspection.dat.h

# what is missing:
- creation/deletion of resources (PUT/DELETE functions)
- handling in get/post of:
    - arrays of arrays, arrays of objects
    - handing of json objects

    
# Building instructions
## code repo
https://github.com/iotivity/iotivity-constrained  e.g. IOTivity-lite

## windows:
- rename the generated file to the simpleserver_windows.c file in the apps folder 
- use the existing visual studio project in folder &lt;installation folder&gt;/port/windows
- note that there are 3 project, 1 for the library, 1 for the client and 1 for server.

Note: to reduce the amount of debug information, remove OC_DEBUG from the compile flags in the property menu.
    
# CTT instructions
- When CTT pops up: "reset to on-boarding state" means one needs to:
  - stop the device
  - delete all files in port/windows/simpleserver_creds  
  - start the server.
    



