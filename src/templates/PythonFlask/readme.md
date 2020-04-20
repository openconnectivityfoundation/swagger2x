# template: PythonFlask

generates an http/json server based on python Flask

used as demonstration that the code generation from swagger2.0 files works with python.
This is not a OCF server, it has some functions implemented simular as OCF.
for exampe:
- oic.wk.res : list of implemented resources, but without end point information
- oic.wk.intropspection: introspection file, implemented with HTTP and JSON as payload

Flask:
see http://flask.pocoo.org/
All endpoints per method have an seperate function.
the Flask route annotation make sure that this function is called when the server is being used.
Each end point has it own set of callbacks.
note that resources without post section in OAS2.0 will not have an POST function implemented.
e.g. they will be by definition read only.

This example shows:
- global variables (per resource) for each parameter in the payload
- Get method callback
    each callback function has
    - input body (if applicable)
    - query parameters (if applicable)
    - generate the output according the parameters in the resource definition
        - uses the value of the global parameter value
- Post method callback
    each method per endpoint has is own callback
    each callback function has
    - input body (if applicable)
    - query parameters (if applicable)
    - update the global variable according the input
    - generate the output according the parameters in the resource definition
        - uses the value of the global parameter value
        
File: python-server.py
the main file that is the generated Flask server
to run the server:
python3 python-server.py <option>

File requirements.txt
file with python packages to install.

File: readme.txt
this file


File: install_packages.py
python script to install packages if not installed in the python3 environment
currently installs Flask.