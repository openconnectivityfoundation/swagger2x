# swagger2x

python tool
generate implementations based on templates from json swagger2.0 file.
templates engine: jinga2

## instalation
This tool is python3 based.

run ```src\install.py``` to install the dependencies.


Installation of the tool is making a clone of the repository.
use the tool relative of where the respository is located on your system.

see the test directory as examples of how to use the tool.
Note that the test directory is set up for bash.
These examples can be used on windows with git-bash.


## usage
swagger2x is an command line tool.
To run the tool enter this on the command line:

```python3 swagger2x.py <options>```

use -h to see all the options.

# templates

The code generator is using jinja2 templates.
Using templates decouples the generated code from looping over the hierarchy.
The hierarchy traversed is the swagger2.0 file constructs in json
e.g. the end points, methods, query param and payload information are all available in jinja2.

code that will be generated will be generated towards:

       -------------------
       |     library      |  <-- functions/class/methods that are allowed to be
       |                  |      used by the template
       --------------------
       | operating system |  <-- os constructs that are allowed to be
       |                  |      used by the template
       --------------------
       |    language      | <-- language constructs/syntax that must be used
       |                  |     by the template
       -------------------

The template is an mix of the library calls, the supported operating system in the used language mixed with the jinaj2 template language to generate the code.
jinja2 takes the json swagger information and make it iteratable by looping over the end points, methods etc. and uses then the info from json to fill in the library/os calls.


## template directory structure
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

### PythonFlask
- generates an python Flask server
- normal http server
- no OCF implemenation
- used as demonstration that the code generation from swagger2.0 files works:
   - call back generation per endpoint-method
   - code to obtain the body of an PUT/POST
   - code to obtain the query parameters
   - code to create the return payload (from the supplied example)


### NodeIotivityServer
- generates an node.js server for the IOTivity stack
- OCF specific based  on:
https://github.com/otcshare/iotivity-node
- work in progress

## jinja2 templates information
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

#### query_rt
retrieve an rt value for an path
input: full swagger file
input: path
return: rt value (as part of the x-example)
typical usage:

{% for path, path_data in json_data['paths'].items() -%}
{{query_rt(json_data,path)}}
{% endfor -%}


#### query_if
retrieve an list of if values for an path
input: full swagger file
input: path
return: if value (as part of the resolved schema)
typical usage:

{% for path, path_data in json_data['paths'].items() -%}
{{query_if(json_data, path)}}
{% endfor -%}


#### query_property_names
retrieve an list of properties values of an schema belonging to the path
input: full swagger file
input: path
return: if value (as part of the resolved schema)
typical usage:

{% for path, path_data in json_data['paths'].items() -%}
{% for propname in query_property_names(json_data, path) -%}
{{propname}}
{% endfor -%}
{% endfor -%}



#### query_properties
retrieve an list of properties an schema belonging to the path
input: full swagger file
input: path
return: if value (as part of the resolved schema)
typical usage:

{% for path, path_data in json_data['paths'].items() %}
{% for var, var_data in query_properties(json_data, path).items() %}
    {{var_data.type|convert_to_c_type}} m{{path|variablesyntax}}{{var|variablesyntax}}; 
{% endfor %}
{% endfor %}


#### query_ref
retrieve an reference 
typical usage:

{{query_ref(json_data, parameter_data["$ref"], "enum")}}


#### path_names (string, array of chars to be replaced by "")
any input string.
function: santize strings to be part of the target language.
typical value = "+-? ,./"

### jinja2 filter functions

#### variablesyntax
replace chars so that the data can be used as an variable.
note that it prefixes the variable with "_" so that names don't get in the
way of language defined names (like "if")

typical usage:

{% for path, path_data in json_data['paths'].items() -%}
{{path|variablesyntax}}
{% endfor -%}

#### variableforbidden
if the varialbe is "if", "var", "function", "null"
it will be prefixed with "_" 
all other names will be kept intact (e.g. just pass through)

#### convert_to_c_type
convert the json types into c types.
typical usage:

{{var|convert_to_c_type}}

note does not do array type.

## TODO list

- template for client code for IOTivity node
- template for client code for IOTivity c++
- template for client code for IOTivity c++
- wheel instalation of the tool
- rename option for generated files

## Fixes

<list fixes here>






### hints


{% for path, path_data in json_data['paths'].items() -%}
{% for definition, def_data in json_data['definitions'].items() -%}
{% for decl, decl_data in def_data.items() -%}
{% if decl == "properties" -%} 
{% for var, var_data in decl_data.items() -%}
    // readonly: {{var_data.readOnly}} type: {{var_data.type}} description: {{var_data.description}}
    {{var_data.type|convert_to_c_type}} m{{path|variablesyntax}}{{var_data.name|variablesyntax}}; 
{% endfor -%}
{% endif -%}
{% endfor -%}
{% endfor %}
{% endfor -%}
