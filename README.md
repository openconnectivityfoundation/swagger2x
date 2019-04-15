# swagger2x

python tool
generate implementations based on templates from json swagger2.0 file.
templates engine: jinga2

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
    

    
    
## jinja2 template information
The template contents is an mix of the target syntax and jinja2 commands.
information about jinja2 commands can be found at:

http://jinja.pocoo.org/docs/dev/

http://jinja.pocoo.org/docs/dev/templates/

https://realpython.com/blog/python/primer-on-jinja-templating/


### jinja2 test functions

#### has_body (method_name)
method name of an swagger path name

### jinja2 custom (global) functions

#### replace_chars (string, array of chars to be replaced by "")
any input string.
function: santize strings to be part of the target language.
typical value = "+-? ,./"

#### retrieve_path_value
retrieve an specific value from a property
- input: json_object
- input: path leading from that object
- input: property name to retrieve the value from, e.g. will be prefixed with path
- return: value of the property

typical usage:

```
{% for path, path_data in json_data['paths'].items() -%}
 var {{path|variablesyntax}}_resourceTypes = {{retrieve_path_value(path_data, "get/200/x-example", "rt")}};
{% endfor -%}
```


#### query_rt
retrieve an rt value for an path
- input: full swagger file
- input: path
- return: rt value (as part of the x-example)

typical usage:

```
{% for path, path_data in json_data['paths'].items() -%}
{{query_rt(json_data,path)}}
{% endfor -%}
```

#### query_if
retrieve an list of if values for an path
- input: full swagger file
- input: path
- return: if value (as part of the resolved schema)

typical usage:

```
{% for path, path_data in json_data['paths'].items() -%}
{{query_if(json_data, path)}}
{% endfor -%}
```

#### query_property_names
retrieve an list of properties values of an schema belonging to the path
- input: full swagger file
- input: path
- return: if value (as part of the resolved schema)

typical usage:

```
{% for path, path_data in json_data['paths'].items() -%}
{% for propname in query_property_names(json_data, path) -%}
{{propname}}
{% endfor -%}
{% endfor -%}
```


#### query_properties
retrieve an list of properties an schema belonging to the path
- input: full swagger file
- input: path
- return: if value (as part of the resolved schema)

typical usage:

```
{% for path, path_data in json_data['paths'].items() %}
{% for var, var_data in query_properties(json_data, path).items() %}
    {{var_data.type|convert_to_c_type}} m{{path|variablesyntax}}{{var|variablesyntax}}; 
{% endfor %}
{% endfor %}
```

#### query_ref
retrieve an reference 

typical usage:

```
{{query_ref(json_data, parameter_data["$ref"], "enum")}}
```

#### path_names (string, array of chars to be replaced by "")
any input string.
function: santize strings to be part of the target language.

typical value = "+-? ,./"

#### swagger_property_data_schema
    get the value of the property name from the schema that is referenced by the path in get (or put)
    it tries to get first the enum values or the default value.
    if this is not found then it will try to get the value from the example
    param json_data: the swagger file as json struct
    param input_path: the path to which the if should be queried
    return: list of if values


typical usage:
```
{% for path, path_data in json_data['paths'].items() -%}
{% for var, var_data in query_properties(json_data, path).items() -%}
{{swagger_property_data_schema(json_data, path, var) | convert_value_to_c_value}}; 
{% endfor -%}
{% endfor -%}
```

### jinja2 filter functions

#### variablesyntax
replace chars so that the data can be used as an variable.
note that it prefixes the variable with "_" so that names don't get in the
way of language defined names (like "if")

typical usage:
```
{% for path, path_data in json_data['paths'].items() -%}
{{path|variablesyntax}}
{% endfor -%}
```

#### classsyntax
replace chars so that the data can be used for an class name.
note that it capitalizes the first letter of the string.
this also solves issue with keywords like "if" won't occur.

typical usage:
```
{% for path, path_data in json_data['paths'].items() -%}
{{path|classsyntax}}
{% endfor -%}
```

#### variableforbidden
if the variable is "if", "var", "function", "null"
it will be prefixed with "_" 
all other names will be kept intact (e.g. just pass through)

#### convert_to_c_type
convert the json types into C types.
typical usage:
```
{{var|convert_to_c_type}}
```
note string will be mapped to char*
note does not do array type.

#### convert_to_cplus_type
convert the json types into C++ types.
typical usage:
```
{{var|convert_to_cplus_type}}
```
note string will be mapped to std:string
note does not do array type.


#### convert_to_cplus_array_type
convert the json array types into C++ vector types.
typical usage:
```
{% if var_data.type == "array" %}
        {{var_data |convert_to_cplus_array_type}}  m_var_value{{var|variablesyntax}};
{% endif -%}
```


#### convert_array_size
determines the size of the array.
for single strings, 1 is returned.

typical usage:
```
{{var|convert_array_size}}
```

#### code_indent
indents the descriptions with an prefix per line.

typical usage:
```
{{ method_data["description"] | code_indent(" * ")}}
```

#### convert_value_to_c_value
    used in combination with swagger_property_data_schema
    the filter is then unwrapping the array and gives out the variable in c style
    e.g. boolean True False are corrected to true and false
    string needs to be with quotes in the jinga2 template.

typical usage:
```
{% for path, path_data in json_data['paths'].items() -%}
{% for var, var_data in query_properties(json_data, path).items() -%}
{{swagger_property_data_schema(json_data, path, var) | convert_value_to_c_value}}; 
{% endfor -%}
{% endfor -%}
```










