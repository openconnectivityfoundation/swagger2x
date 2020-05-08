# swagger2x

swagger2x is a python tool that generate implementations based on templates from json files.
It uses the [jinja2](https://jinja.palletsprojects.com/en/2.11.x/) templates engine.


## Installation
This tool is python3 based.

run ```src\install.py``` to install the dependencies.


Installation of the tool is creating a clone of the repository and
use the tool relative of where the repository is located on your system.


## Usage
swagger2x is an command line tool.
To run the tool enter this on the (bash) command line:

```python3 swagger2x.py <options>```

use -h to see all the options.


__note: see/use [DeviceBuilder](https://openconnectivityfoundation.github.io/DeviceBuilder/) for usage of this tool in the development chain.__


To run the tooling on windows, install [git-bash](https://gitforwindows.org/).


# Templates

The code generator is using jinja2 templates.
Using templates decouples the generated code from looping over the JSON hierarchy.

For code generation the input JSON file is a [swagger2.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md) file.
The hierarchy traversed is the swagger2.0 file constructs in JSON 
e.g. the end points, methods, query param and payload information is available in the jinja2 template.

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
- [more details](/src/templates/IOTivity-lite)
- [folder](https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/IOTivity-lite)


### C++IotivityServer
- generates an C++ server for the v1.3.1 IoTivity stack.
- [more details](https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/C%2B%2BIotivityServer)


### PythonFlask
- generates an python Flask server.
    - this is an HTTP server
- __NO OCF implemenation__
- [more details](/src/templates/PythonFlask)
- [folder](https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/PythonFlask) 
    

### one-data-model
- generates schemas files for One Data Model in Simple Data Format (SDF) language.  
- __NO OCF implemenation__
- [more details](https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/one-data-model)    
- more details on [One Data Model SDF Format](https://github.com/one-data-model/language)


### SDF2OAS
- generates Open API Specification (2.0) files from SDF language (One Data Model).  
- __NO OCF implemenation__
- [more details](https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/SDF2OAS)   
- more details on [One Data Model SDF Format](https://github.com/one-data-model/language)  


## jinja2 template information
The template contents is an mix of the target syntax and jinja2 commands.

Information on implemented commands can be found [here.](https://github.com/openconnectivityfoundation/swagger2x/blob/master/constructs.txt)

Information about jinja2 commands can be found at:

- [docs-dev](http://jinja.pocoo.org/docs/dev/)
- [docs-templates](http://jinja.pocoo.org/docs/dev/templates/)
- [python primer](https://realpython.com/blog/python/primer-on-jinja-templating/)




