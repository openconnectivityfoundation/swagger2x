# swagger2x

python tool
generate implementations based on templates from json swagger2.0 file.
templates engine: jinja2

## Installation
This tool is python3 based.

run ```src\install.py``` to install the dependencies.


Installation of the tool is making a clone of the repository.
use the tool relative of where the repository is located on your system.

see the test directory as examples of how to use the tool.
Note that the test directory is set up for bash.
These examples can be used on windows with git-bash.


## Usage
swagger2x is an command line tool.
To run the tool enter this on the command line:

```python3 swagger2x.py <options>```

use -h to see all the options.


__note: see/use https://github.com/openconnectivityfoundation/DeviceBuilder for usage in the development chain.__


# Templates

The code generator is using jinja2 templates.
Using templates decouples the generated code from looping over the hierarchy.
The hierarchy traversed is the swagger2.0 file constructs in json
e.g. the end points, methods, query param and payload information are all available in jinja2.

code that will be generated will be generated towards:

       --------------------
       |     library      |  <-- functions/class/methods (from libraries) that are allowed to be
       |                  |      used by the template
       --------------------
       | operating system |  <-- os constructs (in the used language) that are allowed to be
       |                  |      used by the template
       --------------------
       |    language      | <-- language constructs/syntax that must be used
       |                  |     by the template
       --------------------

The template is an mix of the library calls, the supported operating system in the used language mixed with the jinja2 template language to generate the code.
jinja2 takes the json swagger information and make it iteratable by looping over the end points, methods etc. and uses then the info from json to fill in the library/os calls.


## Template directory structure
The templates can be found at /src/templates
the following structure is defined:

       -src
          |
          |- templates
                 |
                 |- <template name>
                            |
                            |--- <template file>.jinja2
                            |--- other files (will be copied to output)

## Available Templates


### Iotivity Lite Server
- generates an C server for the IoTivity Lite stack.
- more details: https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/IOTivity-lite


### C++IotivityServer
- generates an C++ server for the v1.3.1 IoTivity stack.
- more details: https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/C%2B%2BIotivityServer


### NodeIotivityServer
- generates an node.js server for the IOTivity stack.
- OCF specific based on:
https://github.com/otcshare/iotivity-node
- Requires iotivity-node v1.3.1 or later
- more details: https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/NodeIotivityServer


### PythonFlask
- generates an python Flask server.
    - this is an HTTP server
- __NO OCF implemenation__
- more details: https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/PythonFlask     
    

### one-data-model
- generates schemas files for One Data Model in Simple Data Format (SDF) language.  
- __NO OCF implemenation__
- more details: https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/one-data-model    
- One Data Model SDF Format, more details: https://github.com/one-data-model/language  


## jinja2 template information
The template contents is an mix of the target syntax and jinja2 commands.
information about jinja2 commands can be found at:

http://jinja.pocoo.org/docs/dev/

http://jinja.pocoo.org/docs/dev/templates/

https://realpython.com/blog/python/primer-on-jinja-templating/




