# Template: IOTivity Constrained C server


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
        - naming convention g_<resource>_<propertyname>
        
    - functions:
        - get_<resource> 
            - function to convert the  member variables to the response document
            - note: always returns the same document, regardless of the interface
                - this works for testcase CT1.2.2
            - handles: boolean, number, integer, string
        - post_<resource>(
            - function to convert the input request document to the member variables
            - checks if input is correct :
                - no write to readOnly properties
                - properties of the correct type (using type in the struct)
                - properties in MIN/MAX range given in by schema (not by property range)
               returns error if this is not satisfied.
               global variable(s) is not assigned
            - handles boolean, number, integer and string
-PICS.json
    - PICT file that list the implemented resources in the generated code
      to be used with CTT
      
            
# what is missing/incorrect:
- creation/deletion of resources (PUT/DELETE functions)
- handling in get/post of
    - arrays/json structures in payload

    
# Building instructions
## code repo
https://github.com/iotivity/iotivity-constrained  e.g. IOTivity-Lite

## windows:
- easiest way to build and run is to rename the generated file to the simpleserver_windows.c file in the apps folder 
- use the existing visual studio project in folder port/windows
- note that there are 3 project, 1 for the library, client and server.

- other instructions
    - place the server_introspection.dat file in the folder port/windows
    
# CTT instructions
- When CTT pops up: "reset to on-boarding state" means one needs to:
  - stop the device
  - delete all files in port/windows/simpleserver_creds  
  - start the server.
    



