# swagger2x

python tool
generate implementations based on templates from json swagger2.0 file.
templates engine: jinga2


## instalation
This tool is python3 based.
It should automatically install all the packages that it needs to run.

just do an clone of the repository.
and use the tool relative of where the respository is located on your system.


## usage
python3 swagger2x.py <options>
use -h to see all the options.


# templates
The templates can be found at /src/templates
the following structure is defined:

       -src
          |
          |- templates
                 |
                 |- <template name>
                            |
                            |--- <template file>.jinga2
                            |--- other files (will be copied to output)


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


#### path_names (string, array of chars to be replaced by "")
any input string.
function: santize strings to be part of the target language.
typical value = "+-? ,./"

### jinja2 filter functions

#### variablesyntax
eplace chars so that it can be used as an variable


## TODO

## Fixes
