template: PythonFlask

generates an http/json server based on python Flask

Flask:
see http://flask.pocoo.org/
All endpoints per method have an seperate function.
the Flask route annotation make sure that this function is called when the server is being used.

This example shows:
- function generation per end point
    each method per endpoint has is own callback
    each call back has
    - input body (if applicable)
    - query parameters (if applicable)
    - list of return codes
    - example used as return payload


File: python-server.py
the main file that is the generated Flask server
to run the server:
python3 python-server.py <option>

File: readme.txt
this file


File: install_packages.py
python script to install packages if not installed in the python3 environment
currently installs Flask.