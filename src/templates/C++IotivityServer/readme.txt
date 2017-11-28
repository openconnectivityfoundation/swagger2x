Template: IOTivity C++ server

The generated code acts as an simulator:
- it creates values at start update
- handles incomming requests, 
    - stores the values on POST
    - respond on GET by giving out the stored values

what is generated:
- server.h header file 
    - list all resources
        - create functions for: get, put, observe, entity handler
        - list all names of the properties in the resources
        - create member variable of properties in the resources
        
- server.cpp implementation code
    - get_XXX_Representation() : function to convert the  member variables to the response document
    - put_XXX_Representation() : function to convert the input request document to the member variables
    - XXXEntityHandler() : function to handle the incomming request 
    - xxx_observeloopFunc() : function to update the observed clients

    
- straigh copies:
    observer.h/cpp
    - this is code to update the list of observers, thanks to Intel.

what is missing/incorrect:
- handling query params
- creation/deletion of resources (PUT/DELETE functions)
- no correct makefile/scons file, so we do not yet know how to insert this in the IOTivity tree and then compile

Notes:
- based on low level api.




