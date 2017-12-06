Template: IOTivity Constrained C server

== not complete yet, awaiting answers ==


The generated code acts as an simulator:
- it creates values at start update
- handles incomming requests, 
    - stores the values on POST
    - respond on GET by giving out the stored values

what is generated:
        
- simpleserver.c implementation code
    - variables
        
    - functions:
        - get_XXX() : function to convert the  member variables to the response document
            - TODO: setting output response from global variables
        - post_XXX() : function to convert the input request document to the member variables
            - TODO: setting input to global variables

what is missing/incorrect:
- handling query params
- creation/deletion of resources (PUT/DELETE functions)
- no correct makefile file, so we do not yet know how to insert this in the IOTivity tree and then compile
- security?
- introspection

Notes:




