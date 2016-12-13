template: PythonFlask

generates an http/json server based on python Flask

Flask:
see http://flask.pocoo.org/
All endpoints per method have an seperate function.
the Flask route make sure that this function is called when the server is being used.


File: python-server.py
the main file that is the generated Flask server
to run the server:
python3 python-server.py <option>

File: readme.txt
this file


File: install_packages.py
python script to install packages if not installed in the python3 environment
currently installs Flask.