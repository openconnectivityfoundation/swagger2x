# swagger2x

## Description

swagger2x is a Python tool that generate implementations based on templates from JSON files.
It uses the [jinja2](https://jinja.palletsprojects.com/en/2.11.x/) templates engine.

## Table of Contents

- [swagger2x](#swagger2x)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Templates](#templates)
      - [Template directory structure](#template-directory-structure)
      - [Available Templates](#available-templates)
        - [IoTivity Server](#iotivity-server)
        - [PythonFlask](#pythonflask)
        - [one-data-model](#one-data-model)
        - [SDF2OAS](#sdf2oas)
    - [Jinja2 template information](#jinja2-template-information)
  
## Installation

This tool is Python3 based.

Installation of the tool is makin a clone of the repository and
use the tool relative of where the repository is located on your system.
To install the dependencies:

run ```pip3 install -U -r requirements.txt``` to install the dependencies.

## Usage

Swagger2x is an command line tool.
To run the tool enter this on the (bash) command line:

```python3 swagger2x.py <options>```

use -h to see all the options.

__note: see/use [DeviceBuilder](https://openconnectivityfoundation.github.io/DeviceBuilder/) for usage of this tool in the development chain.__

To run the tooling on windows, install [git-bash](https://gitforwindows.org/).

### Templates

The code generator is using jinja2 templates.
Using templates decouples the generated code from looping over the JSON hierarchy.

For code generation the input JSON file is a [swagger2.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md) file.
The hierarchy traversed is the swagger2.0 file constructs in JSON 
e.g. the end points, methods, query param and payload information is available in the jinja2 template.

The code that can be generated should take into account:
![GenericStack](https://openconnectivityfoundation.github.io/swagger2x/data/generic-stack.png)

Therefore a template is an mix of the library calls, the supported operating system in the used language mixed with the jinja2 template language to generate the code.
jinja2 takes the JSON swagger information and make it iteratable by looping over the end points, methods etc. and uses then the info to fill in the library/os calls in the used language.

#### Template directory structure

The templates can be found at [/src/templates](https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates)
the following structure is defined:

![DevelopmentProcess](https://openconnectivityfoundation.github.io/swagger2x/data/structure.png)

New templates can be added by:

- adding a new folder
- adding file(s) with the jinja2 extension that contains the template.

#### Available Templates

##### IoTivity Server

- generates an C server for the IoTivity stack.
- [IoTivity](https://iotivity.org/)
- [more details on the template](/swagger2x/src/templates/IOTivity-lite)
- [folder](https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/IOTivity-lite)

##### PythonFlask

- generates a python Flask server.
  - this is an HTTP server based on [FLASK](https://flask.palletsprojects.com/en/1.1.x/)
- __NO OCF implemenation__
- [more details on the template](/swagger2x/src/templates/PythonFlask)
- [folder](https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/PythonFlask) 

##### one-data-model

- generates schemas files for One Data Model in Simple Data Format (SDF) language.  
- __NO OCF implemenation__
- [more details on the template](/swagger2x/src/templates/one-data-model)
- [folder](https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/one-data-model)
- more details on [One Data Model SDF Format](https://github.com/one-data-model/language)

##### SDF2OAS

- generates Open API Specification (2.0) files from SDF language (One Data Model).  
- __NO OCF implemenation__
- [more details on the template](/swagger2x/src/templates/SDF2OAS)
- [folder](https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/SDF2OAS)
- more details on [One Data Model SDF Format](https://github.com/one-data-model/language)  

### Jinja2 template information

The template contents is an mix of the target syntax and jinja2 commands.

Information on implemented commands can be found [here.](https://github.com/openconnectivityfoundation/swagger2x/blob/master/constructs.txt)

Information about jinja2 commands can be found at:

- [docs-dev](http://jinja.pocoo.org/docs/dev/)
- [docs-templates](http://jinja.pocoo.org/docs/dev/templates/)
- [python primer](https://realpython.com/blog/python/primer-on-jinja-templating/)

