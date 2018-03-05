Template: IOtivity node server

generates an IOTivity node server based on:
https://github.com/otcshare/iotivity-node
documentation available at:
https://github.com/01org/iot-js-api/tree/master/api/ocf


what is working:
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


what is missing:
- creation/deletion of resources (PUT/DELETE functions)
- no code generation of URL arguments
- no code generation of error codes.
- translation for interfaces
  now uses an fixed constant from the API

what is possibly wrong with node.js
- rt and if values are single strings: API should be an array
    (not sure what the impact is though)




