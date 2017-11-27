Template: IOtivity C++ server


what is working:
- header file generation  
    - list all resources
        - list all names of the properties in the resources
        - create member variable of properties in the resources
- c++ code
    - not finished


what is missing:
- code for each endpoint and method
- based on low level api.
- handling query params
- set of variables that are part of the examples as globals
- for GET methods
    - fill in the global variables as return values.
    - list the query params
        but no code to handle the query params 
- for POST methods
    - retrieve all posted varialbles and store them in the global variables
    - fill in the global variables as return values.
    - list the query params
        but no code to handle the query params    
- creation/deletion of resources (PUT/DELETE functions)
- no code generation of URL arguments
- no code generation of error codes.
- translation for interfaces
  now uses an fixed constant from the API

what is wrong:
- rt and if values are single strings: API should be an array
    (not sure what the impact is though)




