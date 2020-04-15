#############################
#
#    copyright 2016, 2020 Open Interconnect Consortium, Inc. All rights reserved.
#    Redistribution and use in source and binary forms, with or without modification,
#    are permitted provided that the following conditions are met:
#    1.  Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#    2.  Redistributions in binary form must reproduce the above copyright notice,
#        this list of conditions and the following disclaimer in the documentation and/or other materials provided
#        with the distribution.
#
#    THIS SOFTWARE IS PROVIDED BY THE OPEN INTERCONNECT CONSORTIUM, INC. "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
#    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE OR
#    WARRANTIES OF NON-INFRINGEMENT, ARE DISCLAIMED. IN NO EVENT SHALL THE OPEN INTERCONNECT CONSORTIUM, INC. OR
#    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#    OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
#    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#############################


import time
import os
import json
import random
import sys
import argparse
import traceback
from datetime import datetime
from time import gmtime, strftime
from sys import exit
#import jsonref
import os.path
from os import listdir
from os.path import isfile, join
from shutil import copyfile
from  collections import OrderedDict
import requests
import re
from numbers import Number


if sys.version_info < (3, 5):
    raise Exception("ERROR: Python 3.5 or more is required, you are currently running Python %d.%d!" %
                    (sys.version_info[0], sys.version_info[1]))
#try:
#    from swagger_spec_validator.validator20 import validate_spec
#except:
#    print("missing swagger_parser:")
#    print ("Trying to Install required module: swagger_parser ")
#    os.system('python3 -m pip install swagger_spec_validator.validator20')
#from swagger_spec_validator.validator20 import validate_spec

#try:
#    from swagger_parser import SwaggerParser
#except:
#    print("missing swagger_parser:")
#    print ("Trying to Install required module: swagger_parser ")
#    os.system('python3 -m pip install swagger_parser')
#from swagger_parser import SwaggerParser
#
# jinja2 imports
#
try:
    from jinja2 import Environment, FileSystemLoader
except:
    print("missing jinja2:")
    print ("Trying to Install required module: jinja2")
    os.system('python3 -m pip install jinja2')
from jinja2 import Environment, FileSystemLoader


def load_json_schema(filename, my_dir=None):
    """
    load the JSON schema file
    :param filename: filename (with extension)
    :param my_dir: path to the file
    :return: json_dict
    """
    full_path = filename
    if my_dir is not None:
        full_path = os.path.join(my_dir, filename)
    if os.path.isfile(full_path) is False:
        print ("json file does not exist:", full_path)

    linestring = open(full_path, 'r').read()
    json_dict = json.loads(linestring, object_pairs_hook=OrderedDict)

    return json_dict


def get_dir_list(dir, ext=None):
    """
    get all files (none recursive) in the specified dir
    :param dir: path to the directory
    :param ext: filter on extension
    :return: list of files (only base_name)
    """
    only_files = [f for f in listdir(dir) if isfile(join(dir, f))]
    # remove .bak files
    new_list = [x for x in only_files if not x.endswith(".bak")]
    if ext is not None:
        cur_list = new_list
        new_list = [x for x in cur_list if x.endswith(ext)]
    return new_list

def create_c_struct(nested_json):
    """
        ...
        Args:
            nested_json: A nested json object.
        Returns:
            dict,  [0 = type, 1 = description ]
    """
    try:
        out = {}
        to_flatten = nested_json

        def my_flatten(my_dict, name=''):
            print (" my_flatten :")
            if isinstance(my_dict, dict):
                for my_name, my_sdict in my_dict.items():
                    if my_name not in ["properties", "allOf", "anyOf", "items", "description", "type", "enum"]:
                        # this is a property name
                        print ("  property: ",my_name, " type: ",my_sdict.get("type"))
                        my_type = my_sdict.get("type")
                        description = my_sdict.get("description")
                        if my_type in ["string", "integer", "number", "boolean"]:
                            out[my_name] = [my_type, description]
                        elif my_type in ["array"]:
                            # handle array
                            type_array = my_sdict["items"].get("type")
                            n_description = my_sdict["items"].get("description")
                            if n_description is not None: 
                                # only use this one if it exists
                                description = n_description
                            out[my_name] = [type_array + "[]", description]
                        elif my_type in ["object"]:
                            # handle object
                            print ( " my_flatten : handle object => go recursive")
                            my_flatten(my_sdict)
            elif isinstance(my_dict, list):
                # dead code so far... e.g. need to be clean up
                i = 0
                for a in my_dict:
                    my_flatten(a, name + str(i) + '_')
                    i += 1
            else:
                print (name)
                if name not in ["properties", "allOf", "anyOf", "items", "description", "type"]:
                    out[name] = my_dict
        
        cur_type = nested_json.get("type")
        if cur_type in ["array"]:
            to_flatten = nested_json["items"]["properties"]
        
        my_flatten(to_flatten)
        
    except:
        traceback.print_exc()
    return out


def find_key(rec_dict, target, depth=0):
    """
    find key "target" in recursive dict
    :param rec_dict: dict to search in, json schema dict, so it is combination of dict and arrays
    :param target: target key to search for
    :param depth: depth of the search (recursion)
    :return:
    """
    try:
        if isinstance(rec_dict, dict):
            for key, value in rec_dict.items():
                if key == target:
                    return rec_dict[key]
            for key, value in rec_dict.items():
                r = find_key(value, target, depth+1)
                if r is not None:
                        return r
        #else:
        #    print ("no dict:", rec_dict)
    except:
        traceback.print_exc()


def find_key_link(rec_dict, target, depth=0):
    """
    find the first key recursively
    also traverse lists (arrays, oneOf,..) but only returns the first occurance
    :param rec_dict: dict to search in, json schema dict, so it is combination of dict and arrays
    :param target: target key to search for
    :param depth: depth of the search (recursion)
    :return:
    """
    if isinstance(rec_dict, dict):
        # direct key
        for key, value in rec_dict.items():
            if key == target:
                return rec_dict[key]
        # key is in array
        rvalues = []
        found = False
        for key, value in rec_dict.items():
            if key in ["oneOf", "allOf", "anyOf"]:
                for val in value:
                    if val == target:
                        return val
                    if isinstance(val, dict):
                        r = find_key_link(val, target, depth+1)
                        if r is not None:
                            found = True
                            # TODO: this should return an array, now it only returns the last found item
                            rvalues = r
        if found:
            return rvalues
        # key is an dict
        for key, value in rec_dict.items():
            r = find_key_link(value, target, depth+1)
            if r is not None:
                return r #[list(r.items())]


def get_value_by_path_name( parse_tree, path_name, target):
    """
    retrieve the target key below the path_name
    :param parse_tree: tree to search from
    :param path_name: url name (without the /)
    :param target: key to find
    :return:
    """
    full_path_name = path_name
    json_path_dict = find_key_link(parse_tree, full_path_name)
    value = find_key_link(json_path_dict, target)
    return value


def get_dict_by_path_name( parse_tree, path_name):
    """
    retrieve the target key below the path_name
    :param parse_tree: tree to search from
    :param path_name: url name (without the /)
    :param target: key to find
    :return:
    """
    full_path_name = path_name
    json_path_dict = find_key_link(parse_tree, full_path_name)
    #value = find_key_link(json_path_dict, target)
    return json_path_dict

#
#  jinga2 custom functions: globals
#
def replace_chars(a, chars):
    """
    function that replaces the occurrences of chars in the string
    :param a: input string
    :param chars: chars to be replaced with "" (nothing)
    :return:
    """
    #print ("replace_chars a: ", a)
    #print ("replace_chars chars: ", chars)
    string = a
    for char in chars:
       copy_string =  string.replace(char, '')
       string = copy_string
    return string

def add_justification_smart( depth, input_string, no_dot_split=False):

        """
        add the spaces for an correct indentation of the generated RAML code section
        for descriptions in the RAML definitions
        :param depth: character depth, e.g. an string prefix
        :param input_string: string to be adjusted
        :return:  adjusted string
        """
        ret_string = ""
        all_lines = input_string.splitlines()
        for x_line in all_lines:
            if no_dot_split is False:
                lines = x_line.split(". ")
                for line in lines:
                    string1 = depth + line + "\n"
                    if len(line) > 0:
                        ret_string = ret_string + string1
            else:
                string1 = depth + x_line
                ret_string = ret_string + string1
                if not x_line is all_lines[-1]:
                    ret_string = ret_string + "\n"
        return ret_string
    
    

def retrieve_path_value(parse_tree, path, value):
    """
    retrieves the parameter values of an path instance
    :param parse_tree: the json parse tree of the swagger document
    :param path: path value of the value to find
    :param value: value to find
    :return:
    """
    #print ("retrieve_path_value", parse_tree, path, value)
    keys = path.split("/")
    my_tree = parse_tree
    for key in keys:
        #print ("Tree before:", my_tree)
        #print ("key", key)
        ret_my_tree = get_dict_by_path_name(my_tree, key)
        my_tree = ret_my_tree
        #print ("Tree after:", my_tree)

    ret_value = None
    if my_tree is not None:
        ret_value = my_tree[value]
        #print ("found value:",ret_value)
    return ret_value


def retrieve_path_dict(parse_tree, path):
    """
    retrieves the parameter values of an path instance
    :param parse_tree: the json parse tree of the swagger document
    :param path: path value of the dict to find
    :return:
    """
    #print ("retrieve_path_dict", parse_tree, path)
    keys = path.split("/")
    my_tree = parse_tree
    for key in keys:
        #print ("Tree before:", my_tree)
        #print ("key", key)
        ret_my_tree = get_dict_by_path_name(my_tree, key)
        my_tree = ret_my_tree
        #print ("Tree after:", my_tree)

    return my_tree


def parameter_names(parse_tree, path, value):
    """
    retrieves the parameter values of an path instance
    :param parse_tree: the json parse tree of the swagger document
    :param path: path value of the
    :param value: value to find
    :return:
    """
    #print ("parameter_names", parse_tree, path, value)
    parameters  = get_value_by_path_name(parse_tree, path, "parameters")
    path_names = ""
    # this is an list
    for parameter_data in parameters:
        print ("parameter_names", parameter_data)
        #if parameter_data["in"] == value:
        #    if len(path_names) == 0:
        #        path_names += parameter_data["name"]
        #    else:
        #        path_names += ", " + parameter_data["name"]
    return path_names


def path_names(parse_tree, path):
    return parameter_names(parse_tree, path, "path")


def query_names(parse_tree, path):
    return parameter_names(parse_tree, path, "query")


def query_ref(parse_tree, parameter_ref, value):
    """
    find the reference of the query value
    :param parse_tree: full json parse tree of the swagger file
    :param parameter_ref: reference value to be found
    :param value: key in the reference to be found
    :return:
    """
    keys = parameter_ref.split("/")
    index = len(keys)
    #print ("query_ref: reference:",keys[index-1])
    parameter_block = get_value_by_path_name(parse_tree, "parameters", keys[index-1])
    try:
        return parameter_block[value]
    except:
        return ""


def swagger_rt(json_data):
    """
    get the rt value from the example
    :param json_data: the swagger file as json struct
    :return: array of arrays of found values e.g. [ [a,b],[a,b] ]
    """
    rt_values = []
    for path, item in json_data["paths"].items():
        try:
            x_example = item["get"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
            for rt_value in rt:
                rt_values.append([ path, rt_value])
        except:
            try:
                rt = item["post"]["responses"]["200"]["x-example"]["rt"]
                for rt_value in rt:
                    rt_values.append([path, rt_value])
            except:
                pass
    return rt_values


def swagger_if(json_data, input_path):
    """
    get the if value from the schema that is referenced by the path in get (or put)
    :param json_data: the swagger file as json struct
    :param input_path: the path to which the if should be queried
    :return: list of if values
    """
    return swagger_property_data_schema(json_data, input_path, "if")


def swagger_if_exist(json_data, input_path, if_value):
    data = swagger_property_data_schema(json_data, input_path, "if")
    #print ("swagger_if_exist", data)
    if if_value in data:
        return True
    return False
    

def swagger_property_data_schema(json_data, input_path, name):
    """swagger_property_data_schema
    get the value of the property name from the schema that is referenced by the path in get (or put)
    it tries to get first the enum values or the default value.
    if this is not found then it will try to get the value from the example
    :param json_data: the swagger file as json struct
    :param input_path: the path to which the if should be queried
    :return: list of if values
    """
    data_values = []
    schema = None
    example = None
    print("swagger_property_data_schema: path/name:", input_path, name)
    for path, path_item in json_data["paths"].items():
        if input_path == path:
            # get the schema
            try:
                schema = path_item["get"]["responses"]["200"]["schema"]
            except:
                try:
                    schema = path_item["post"]["responses"]["200"]["schema"]
                except:
                    print ("swagger_property_data_schema: could not find schema")
                    pass
            # get the example
            try:
                example = path_item["get"]["responses"]["200"]["x-example"]
            except:
                try:
                    example = path_item["post"]["responses"]["200"]["x-example"]
                except:
                    print ("swagger_property_data_schema: could not find x-example")
                    pass


            value_found = False        
            if schema is not None:
                #print("swagger_property_data_schema: schema", schema)
                def_data = json_data["definitions"]
                for def_name, def_item in def_data.items():
                    full_def_name = "#/definitions/" + def_name
                    if full_def_name == schema["$ref"]:
                        #print("swagger_property_data_schema: found", full_def_name)
                        name_block = find_key_link(def_item, name)
                        #print("swagger_property_data_schema: found name", name, name_block)
                        if name_block is not None:
                            # get it from the schema::enum
                            try:
                                enum_values = name_block["items"]["enum"]
                                for enum_value in enum_values:
                                    data_values.append(enum_value)
                                    value_found = True
                            except:
                                # get it from the schema::default
                                try:
                                    default_values = name_block["default"]
                                    for default_value in default_values:
                                        data_values.append(default_value)
                                        value_found = True

                                except:
                                    # get it from the example
                                    value_found = False
                        else:
                            print (def_item)
                            
            else:
                print("swagger_property_data: schema not found:", input_path)

            if value_found is False:
                if example is not None:
                    #print("swagger_property_data_schema: name,example:", name, example)
                    if isinstance(example, dict):
                        value = example.get(name)
                        if value is not None:
                            value = example[name]
                            print("swagger_property_data_schema: getting name, value:", name, value)
                            if isinstance(value, list):
                                for val in value:
                                    data_values.append(val)
                            else:
                                data_values.append(value)
                    else:
                        print("swagger_property_data_schema: example could not find:", name)
                        pass   
                else:
                     print("swagger_property_data_schema: example is none")
    return data_values


def swagger_property_names(json_data, input_path):
    """
    get the properties  from the schema that is referenced by the path in get (or put)
    :param json_data: the swagger file as json struct
    :param input_path: the path to which the if should be queried
    :return: list of if values
    """
    prop_values = []
    schema = None
    #print("swagger_property_names: path:", input_path)
    for path, path_item in json_data["paths"].items():
        if input_path == path:
            try:
                schema = path_item["get"]["responses"]["200"]["schema"]
            except:
                try:
                    schema = path_item["post"]["responses"]["200"]["schema"]
                except:
                    pass
            if schema is not None:
                #print("swagger_property_names: schema", schema)
                def_data = json_data["definitions"]
                for def_name, def_item in def_data.items():
                    full_def_name = "#/definitions/" + def_name
                    if full_def_name == schema["$ref"]:
                        #print("swagger_property_names: found", def_item)
                        prop_block = find_key_link(def_item, "properties")
                        #print("swagger_property_names: found", prop_block)
                        if prop_block is not None:
                            for prop_name, prop in prop_block.items():
                                prop_values.append(prop_name)
            else:
                print("swagger_property_names: schema not found:", input_path)
    return prop_values

def swagger_properties(json_data, input_path):
    """
    get the properties  from the schema that is referenced by the path in get (or post)
    :param json_data: the swagger file as json struct
    :param input_path: the path to which the if should be queried
    :return: list of if values
    """
    prop_block = []
    #print("swagger_properties: path:", input_path)
    schema = None
    for path, path_item in json_data["paths"].items():
        if input_path == path:
            try:
                schema = path_item["get"]["responses"]["200"]["schema"]
            except:
                try:
                    schema = path_item["post"]["responses"]["200"]["schema"]
                except:
                    pass
            if schema is not None:
                schema_ref = schema["$ref"]
                #print("swagger_properties: schema", schema, schema_ref)
                def_data = json_data["definitions"]
                for def_name, def_item in def_data.items():
                    full_def_name = "#/definitions/" + def_name
                    if full_def_name in [schema_ref]:
                        #print("swagger_properties: found", def_item)
                        prop_block = find_key_link(def_item, "properties")
                        #for var, var_data in prop_block.items():
                        #    print ("  swagger_properties var:", var)
                        return prop_block
            else:
                print("swagger_properties: schema not found:", input_path)
    return prop_block
    
    
def swagger_properties_post(json_data, input_path):
    """
    get the properties  from the schema that is referenced by the path in post (or get)
    :param json_data: the swagger file as json struct
    :param input_path: the path to which the if should be queried
    :return: list of if values
    """
    prop_block = []
    #print("swagger_properties_post: path:", input_path)
    schema = None
    for path, path_item in json_data["paths"].items():
        if input_path == path:
            try:
                #schema = path_item["post"]["responses"]["200"]["schema"]
                schema_param = path_item["post"]["parameters"]
                for item in schema_param:
                    schema_found = item.get("schema")
                    if schema_found is not None:
                      schema = schema_found
            except:
                try:
                    schema = path_item["get"]["responses"]["200"]["schema"]
                except:
                    pass
            if schema is not None:
                schema_ref = schema["$ref"]
                #print("swagger_properties_post: schema", schema, schema_ref)
                def_data = json_data["definitions"]
                for def_name, def_item in def_data.items():
                    full_def_name = "#/definitions/" + def_name
                    if full_def_name in [schema_ref]:
                        #print("swagger_properties_post: found", def_item)
                        prop_block = find_key_link(def_item, "properties")
                        #for var, var_data in prop_block.items():
                        #    print ("  swagger_properties_post
            else:
                print("swagger_properties_post: schema not found:", input_path)
    return prop_block
    
    
    
def swagger_required_items(json_data, input_path):
    """
    get the required properties list from the schema that is referenced by the path in post (or get)
    :param json_data: the swagger file as json struct
    :param input_path: the path to which the if should be queried
    :return: list of if values
    """
    prop_block = []
    #print("swagger_properties_post: path:", input_path)
    schema = None
    for path, path_item in json_data["paths"].items():
        if input_path == path:
            try:
                #schema = path_item["post"]["responses"]["200"]["schema"]
                schema_param = path_item["post"]["parameters"]
                for item in schema_param:
                    schema_found = item.get("schema")
                    if schema_found is not None:
                      schema = schema_found
            except:
                try:
                    schema = path_item["get"]["responses"]["200"]["schema"]
                except:
                    pass
            if schema is not None:
                schema_ref = schema["$ref"]
                #print("swagger_required_items: schema", schema, schema_ref)
                def_data = json_data["definitions"]
                for def_name, def_item in def_data.items():
                    full_def_name = "#/definitions/" + def_name
                    if full_def_name in [schema_ref]:
                        prop_block = find_key_link(def_item, "required")                
            else:
                print("swagger_required_items: schema not found:", input_path)
    return prop_block
    
    
def swagger_properties_filtered(json_data, input_path):
    """
      returns the properties of "GET 200".
      remove common properties & resource properties from the list of properties in the resource
      see Resource spec
    """
    properties_list =  swagger_properties(json_data, input_path)
    my_dict = OrderedDict()
    for item, item_val in properties_list.items():
        #if item not in ["n", "if", "rt", "id", "range", "step", "precision"]:
        if item not in ["n", "if", "rt", "id"]:
            #type = item_val.get("type")
            #if type != None:
            my_dict[item] = item_val
            #print ("swagger_properties_filtered: ", item, item_val)

    return my_dict
    
    
def swagger_properties_filtered_post(json_data, input_path):
    """
      remove common properties & resource properties from the list of properties in the resource
      see Resource spec
    """
    properties_list =  swagger_properties_post(json_data, input_path)
    my_dict = OrderedDict()
    for item, item_val in properties_list.items():
        #if item not in ["n", "if", "rt", "id", "range", "step", "precision" ]:
        if item not in ["n", "if", "rt", "id" ]:
            #type = item_val.get("type")
            #if type != None:
            my_dict[item] = item_val
            #print ("swagger_properties_filtered_post: ", item, item_val)
    return my_dict
    


def retrieve_rt_from_path(parse_tree, path):
    """
    find the rt from path level
    :param parse_tree: full json parse tree of the swagger file
    :param parameter_ref: reference value to be found
    :param value: key in the reference to be found
    :return:
    """
    #print ("retrieve_rt_from_path: rt from path:", path)
    found_values = swagger_rt(parse_tree)
    for value in found_values:
        if value[0] == path:
            return value[1]
    return ""

def query_path(parse_tree, my_path, value):
    """
    find the reference of the query value
    :param parse_tree: full json parse tree of the swagger file
    :param parameter_ref: reference value to be found
    :param value: key in the reference to be found
    :return:
    """
    keys = my_path.split("/")
    index = len(keys)
    #print ("query_ref: reference:",keys[index-1])
    parameter_block = get_value_by_path_name(parse_tree, "parameters", keys[index-1])
    try:
        return parameter_block[value]
    except:
        return ""

def list_query_params(json_data, input_path):
    """
    list all query param blocks
    """
    query_params = []
    for path, path_item in json_data["paths"].items():
        if input_path == path:
            try:
                params = path_item["get"]["parameters"]
                for item in params:
                    if item.get("in") == "query":
                        #print (  " param in of", item_name, item.get("in"))
                        if item.get("name") != "if": 
                          query_params.append(item)
                    elif item.get("$ref") != None:
                        #resolve reference
                        #print ("  ===>", item)
                        reference_name = item.get("$ref")
                        ref = reference_name.split("/")[2]
                        #print ("  ==---=>", reference_name, ref)
                        for param_item_name, param_item in json_data["parameters"].items():
                            #print (param_item_name)
                            if param_item_name == ref:
                                if param_item.get("in") == "query":
                                    if param_item.get("name") != "if": 
                                        query_params.append(param_item)
                        
            except:
                traceback.print_exc()
           
    #print (query_params)
    return query_params
    


#
#  jinga custom functions : tests
#
def ishasbody(method):
    """
    check if the method can have an body: e.g. put, post and patch
    :param method: (get, put, post, ....)
    :return:
    """
    if method in ["put", "post", "patch"]:
        return True
    return False

#
#  jinga custom functions: filter
#
def classsyntax(input_string):
    """
    replace invalid chars so that it can be used and capitalize first char
    :param input_string: string to be adjusted
    :return: adjusted string
    """
    chars_to_replace = "/\  +-*^|%$=~@()[].,"
    return replace_chars(input_string, chars_to_replace).capitalize()

#
#  jinga custom functions: filter
#
def variablesyntax(input_string):
    """
    replace chars so that it can be used as an variable
    :param input_string: string to be adjusted
    :return: adjusted string
    """
    chars_to_replace = "/\  +-*^|%$=~@()[].,"
    return "_"+replace_chars(input_string, chars_to_replace )

#
#  jinga custom functions: filter
#
def variableforbidden(input_string):
    """
    replace chars so that it can be used as an variable
    :param input_string: string to be adjusted
    :return: adjusted string
    """
    if input_string in ["if", "var", "function", "null"]:
        return "_"+input_string
    return input_string

def convert_to_cplus_type(json_type):
    """
    convert the json type to c++ type
    :param json_type: the json type
    :return: c++ type.
    """
    #print ("convert_to_cplus_type: json_type:", json_type)
    if json_type in ["boolean"]:
        return "bool"
    if json_type in ["number"]:
        return "double"
    if json_type in ["integer"]:
        return "int"  # uint8_t ?
    if json_type in ["string"]:
        return "std::string"
    if json_type in ["object"]:
        return "OCRepresentation"
    return "void*"

def convert_to_cplus_array_type(json_data):
    """
    convert the json type to c++ type
    :param json_type: the json type
    :return: c++ type.
    """
    #print ("convert_to_cplus_array_type: json_data:", json_data)
    subtype = json_data["items"].get("type")
    subtype_oneOff = json_data["items"].get("oneOf")
    
    #print ("convert_to_cplus_array_type: json_data: Type:", type)
    if subtype is not None:
        if subtype in ["string", "number", "boolean", "integer"]:
            return "std::vector<"+convert_to_cplus_type(json_data["items"]["type"])+">"
        if subtype in ["object"]:
            return "std::vector<OCRepresentation>"
        if subtype in ["array"]:
            return "std::vector<array>"
    elif subtype_oneOff is not None:
        return "char*"
    return "void*"

    
    
def convert_to_c_type(json_type):
    """
    convert the json type to c type
    :param json_type: the json type
    :return: c type.
    """
    print ("convert_to_c_type: json_type:", json_type)
    if json_type in ["boolean"]:
        return "bool"
    if json_type in ["number"]:
        return "double"
    if json_type in ["integer"]:
        return "int"  # uint8_t ?
    if json_type in ["string"]:
        return "char*"
    
    # array versions e.g. postpended with []
    if json_type in ["string[]"]:
        return "char**"
    if json_type in ["integer[]"]:
        return "int*"
    if json_type in ["boolean[]"]:
        return "bool*"
    if json_type in ["number[]"]:
        return "double*"
        
    return "void*"


def convert_to_c_type_no_pointer(json_type):
    """
    convert the json type to c type
    :param json_type: the json type
    :return: c type.
    """
    print ("convert_to_c_type: json_type:", json_type)
    if json_type == "boolean":
        return "bool"
    if json_type == "number":
        return "double"
    if json_type == "integer":
        return "int"  # uint8_t ?
    if json_type == "string":
        return "char"
    
    # array versions e.g. postpended with []
    if json_type == "string[]":
        return "char"
    if json_type == "integer[]":
        return "int"
    if json_type == "boolean[]":
        return "bool"
    if json_type == "number[]":
        return "double"
        
    # 2D array versions e.g. postpended with [][]
    if json_type == "string[][]":
        return "char"
    if json_type == "integer[][]":
        return "int"
    if json_type == "boolean[][]":
        return "bool"
    if json_type == "number[][]":
        return "double"
        
    return "void*"

def convert_to_c_type_array_size (json_type):
    """
    convert the json type to c type
    :param json_type: the json type
    :return: c type.
    """
    print ("convert_to_c_type: json_type:", json_type)
    if json_type == "boolean":
        return 0
    if json_type == "number":
        return 0
    if json_type == "integer":
        return 0
    if json_type == "string":  
        # string is already an array
        return 1
    
    # array versions e.g. postpended with []
    if json_type == "string[]":
        return 2
    if json_type == "integer[]":
        return 1
    if json_type == "boolean[]":
        return 1
    if json_type == "number[]":
        return 1
        
    # array versions e.g. postpended with [][]
    if json_type == "string[][]":
        return 3
    if json_type == "integer[][]":
        return 2
    if json_type == "boolean[][]":
        return 2
    if json_type == "number[][]":
        return 2
        
    return "void*"

def get_c_data(json_data, prefix=""):
    """
    convert the json type to c struct retrieve code 
    :param json_type: the json type
    : Args:
            nested_json: A nested json object.
    ;Returns:
            dict=  {keyname, [0 = type, 1 = description ]}
    """
    print ("get_c_data ")
    prefix2 = prefix
    if len(prefix) > 0:
        prefix2 = "  "+ prefix + "."
    blah = create_c_struct(json_data)
   
    return blah



def convert_to_cplus_string_array(my_array):
    """
    convert the json type to c type
    :param json_type: the json type
    :return: c type.
    """
    my_ret = '{'
    counter = 0
    if isinstance(my_array, str):
        my_ret += '"'+str(my_array)+'"'
    elif isinstance(my_array, list):
        for item in my_array:
            if counter  > 0:
               my_ret += ','
            my_ret += '"'+str(item)+'"'
            counter +=1
    else:
        pass

    my_ret += '}'
    return my_ret

def convert_array_size(my_array):
    """
    convert the json type to c type
    :param json_type: the json type
    :return: c type.
    """
    counter = 0
    if isinstance(my_array, str):
        return 1
    elif isinstance(my_array, list):
        return len(my_array)
    else:
        pass

    return 0

def code_indent(input_string, indent_str):
    """
    replace chars so that it can be used as an variable
    :param input_string: string to be adjusted
    :return: adjusted string
    """    
    return_string = add_justification_smart(indent_str, input_string, no_dot_split = True )
    return return_string
    
    

def convert_value_to_c_value(my_value):
    """
    convert the json value to c value
    :param my_value the value from swagger_property_data_schema
    :return: c value.
    """
    #print ("convert_value_to_c_type: my_value:", my_value)
    
    if isinstance(my_value, list) :
        if len (my_value) > 0:
            my_value = my_value[0]
        else:
            my_value = ""  # default is empty string
        #return my_value
    
    if isinstance(my_value, bool) :
        if my_value is True:
            my_value = "true"
        else:
            my_value = "false"
        return my_value
    
    if isinstance(my_value, str) :
        new = escape_quotes(my_value)
        my_value = new
        
    return my_value
    
    
    
def init_value_if_empty(my_value, value_type):
    """
    convert the json value to c value
    :param my_value the value from swagger_property_data_schema
    :return: c value.
    """
    print ("init_value_if_empty: my_value:", my_value, " type:", value_type)
    
    new_value = convert_value_to_c_value(my_value)
    
    if value_type in ["number", "integer"]:
        if new_value is None:
            return 0
        if new_value in [""]:
            return 0
            
    if value_type in ["boolean"]:
        return "false"
        
    if new_value is None:
        if value_type in ["string"]:
            return ""
            
    if isinstance(my_value, list) :
        if value_type in ["string"]:
            return '""'
        if value_type in ["number"]:
            return 0
    

    return new_value

def escape_quotes(my_string):
    """
    convert " quotes in to \"
    :param my_value the string to be escaped
    :return: string with escaped
    """
    #print ("escape_quotes: my_value:", my_string)
    data= my_string.split('"')
    new_string=""
    for item in data:
        if item == data[-1]:
            new_string = new_string + item 
        else: 
            new_string = new_string + item + '\\"'
    #print ("escape_quotes: escaped :", new_string)
    
    # remove new line
    new_string2=""
    data= new_string.split('\n')
    for item in data:
      new_string2 = new_string2 + item 
    # remove carrage return
    new_string3=""
    data= new_string2.split('\r')
    for item in data:
      new_string3 = new_string3 + item 
          
    return new_string3

#JLR New functions for ODM     
def odm_supported_model(json_data, name):
    # if there are multiple paths defined, the model is currently not supported (likely a collection or atomic model)
    unsupported = False
    numPaths = 0
    #Test for incompatible model
    try:
        Paths = json_data["paths"].items()
        numPaths = len(Paths)
    except:
        print("WARNING: Model may have no path and is unsupported")
        unsupported = True
        #oic.baseresource.properties-schema.json is caught here
        Paths = {"oic.baseresource.properties-schema.json": "baseresource_path"}.items()
        numPaths = 0
    if numPaths > 1:
        print("WARNING: More than one path found")
        unsupported = True 
    if 'anyOf' in str(json_data):
        print("WARNING: anyOf encountered in schema")
        unsupported = True;
    if 'oneOf' in str(json_data):
        print("WARNING: oneOf encountered in schema")
        unsupported = True;     
    
    if unsupported:
        #debug, write filenames that are supported to hardcoded filename
        #f = open("C:/BUILD/out/iot/unsupported.txt", 'a+')
        #f.write(name + '\n')
        #f.close()
        return False
    else:
        #debug, write filenames that are unsupported to hardcoded filename
        #f = open("C:/BUILD/out/iot/supported.txt", 'a+')
        #f.write(name + '\n')
        #f.close()
        return True

def odm_supported_property(property_name):
    """
    Check to verify that this property is support natively in ODM (without modification)
    :param property_name name to check
    :return: boolean true/false
    """
    #these supported items, assume the input models are valid JSON, and do no addition verification of linking properties to valid types.
    #basic JSON properties
    supportedProperties = ["type", "minimum", "maximum", "uniqueItems", "format"]
    #extended JSON properties
    supportedProperties.extend(["minItems", "maxItems", "default", "exclusiveMinimum", "exclusiveMaximum"])
    #properties used for strings, other modifiers 
    supportedProperties.extend(["maxLength", "minLength"])
    # description, readOnly, enum, $ref handled in a special function, to rename / reorder properties
    if property_name in supportedProperties:
        return True
    else:
        return False


def odm_make_reference_external(iter_json_data, url):
    """
    Checks all $ref and prepend the url to it if it is a local reference (e.g. start with #)
    :param json data
    :param url url to be prefixed to the local reference
    :return: data
    """
    url_base = url.split("#")[0]
    #print ( "odm_make_reference_external :", url_base)
    for property_name, property_data in iter_json_data.items():
        #print (property_name)
        if property_name == "$ref":
            if property_data[0] == "#":
                new_url = url_base + property_data
                iter_json_data[property_name] = new_url
        if isinstance(property_data, dict):
            odm_make_reference_external(property_data, url)
                

def odm_supported_property_non_string(property_name):
    """
    Check to verify that this property is support natively in ODM (without modification)
    :param property_name name to check
    :return: boolean true/false
    """
    supportedProperties = ["minimum", "maximum", "uniqueItems", "default", "exclusiveMinimum"]
    # readOnly, enum, $ref handled in a special function, to rename / reorder properties
    if property_name in supportedProperties:
        return True
    else:
        return False

def odm_property_object(json_data, level):
    """
    Take the property values from a resource type and reformat for odm 
    :param json_data: odmProperty's json_data from resource type
    :param level: "top" = top level, ignore filtered out types, "sub" = subsequent level, no filter required
    :return: json formatted string
    
    """
    print ( "odm_property_object :", level)
    
    if (level == "top"):
        iter_json_data = swagger_properties_filtered(json_data, odm_return_path_info(json_data, "path")).items()
    else:
        #json_data passed in is what's required for iteration below, embedded property blocks
        iter_json_data = json_data.items()

    output = ""
    for i, (property_name, property_data) in enumerate(iter_json_data):
        #print("Pname,Pdata: ", property_name, '\n', property_data)
        output += "\"" + property_name + "\": {"
        #new name field
        output += "\"name\": \"" + decamel_name(property_name) + "\","
        output += odm_properties_block(property_data)
        output += "}"
        if i+1 < len(iter_json_data):
            output += ","
    print ( "odm_property_object : leave", level)
    return output

def odm_properties_block(propertyData):
    #print ( "odm_properties_block : entry", flush=True)

    if propertyData == None:
        return ""
    output_total = ""
    not_outputted = 0
    for j, (propertyData_key, propertyData_value) in enumerate(propertyData.items()):
        output = ""
        if odm_supported_property(propertyData_key):
            #print ("" ,propertyData_key,propertyData_value, isinstance(propertyData_value, int))
            if isinstance(propertyData_value, bool) and propertyData_value == True:
                output += "\"" + propertyData_key + "\":  true"
            elif isinstance(propertyData_value, bool) and propertyData_value == False:
                output += "\"" + propertyData_key + "\":  false"
            elif isinstance(propertyData_value, Number):
                output += "\"" + propertyData_key + "\": "+ str(propertyData_value)
            elif isinstance(propertyData_value, int):
                output += "\"" + propertyData_key + "\": "+ str(propertyData_value)
            else:
                output += "\"" + propertyData_key + "\": "+ "\"" + propertyData_value + "\""
        elif propertyData_key == "description":
            output += ("\"" + propertyData_key + "\": \"" + escape_quotes(propertyData_value) + "\"")
        elif propertyData_key == "enum":
            output += ("\"" + propertyData_key + "\": " + odm_enum_array(propertyData_value))
        elif propertyData_key == "pattern":
            output += ("\"" + propertyData_key + "\": \"" + escape_escapes(propertyData_value) + "\"")
        elif propertyData_key == "readOnly":
            output += ("\"writable\": "  + odm_readOnly_object(propertyData_value))
        elif propertyData_key == "items":
            output += ("\"" + propertyData_key + "\": " + odm_item_object(propertyData_value))
        elif propertyData_key == "$ref":
            output += odm_ref_properties(json_data, propertyData_value)
        elif propertyData_key == "properties":
            output += ("\"" + propertyData_key + "\": {" + odm_property_object(propertyData_value, "sub")) + "}"
        elif propertyData_key == "required":
            output += ("\"" + propertyData_key + "\": " + odm_enum_array(propertyData_value))
        else:
            print (" not handled in sdf.json.jinja2:odm_properties_block: ", propertyData_key)
            #output += ("\"x-problem\": \"" + propertyData_key + " not handled in sdf.json.jinja2:odm_properties_block\"")
            not_outputted += 1
        if j+1 < (len(propertyData.items())-not_outputted):
            output += ","
        output_total += output
        #print ( "  odm_properties_block", output)
        
    #print ( "odm_properties_block: leave", flush=True)
    return output_total

def odm_required_block_check(json_data):
    """
    Return True/False if a required block should be populated
    :json_data: inputted resource type file
    :return: True/False
    """
    if swagger_required_items(json_data, odm_return_path_info(json_data, "path")) is None:
        return False
    else:
        return True

def odm_required_object(json_value):
    """
    Return the required object block for one-data-model
    :param json_value: json object for resource type
    :return: json formatted string for odm required block
    """ 
    output = "["
    requiredItems = swagger_required_items(json_data, odm_return_path_info(json_data, "path"))

    for i, requiredItem in enumerate(requiredItems):
        output += "\"0/odmProperty/" + requiredItem + "\""
        if i+1 < len(requiredItems):
            output += ","
    output += "]"
    return output

def odm_item_object(itemObject):
    """
    Take the item value and additionally parse for odm 
    :param itemObject: item's value
    :return: json formatted string
    """
    print ( "odm_item_object : entry", flush=True)
    i=0
    output = "{"
    for i, (itemKey, itemValue) in enumerate(itemObject.items()):
        #output = output + "\"" + itemKey + "\": " 
        if itemKey == "enum":
            output = output + "\"" + itemKey + "\": " 
            output = output + odm_enum_array(itemValue)
        else:
            print ("   item keyvalue",itemKey, itemValue)
            if itemKey == "maximum":
                output = output + "\"" + itemKey + "\": " 
                output += str(itemValue)
            elif itemKey == "minimum":
                output = output + "\"" + itemKey + "\": " 
                output += str(itemValue)
            elif itemKey == "minItems":
                output = output + "\"" + itemKey + "\": " 
                output += str(itemValue)
            elif itemKey == "maxItems":
                output = output + "\"" + itemKey + "\": " 
                output += str(itemValue)
            elif itemKey == "$ref":
                print('  odm_item_object: $ref!! ', itemKey, itemValue)
                #odm_ref_properties(
                output += odm_ref_properties(json_data, itemValue)
                #output += str(itemValue)
            elif itemValue == True:
                output = output + "\"" + itemKey + "\": " 
                output = output + "true"
            elif itemValue == False:
                output = output + "\"" + itemKey + "\": " 
                output += "false"
            elif itemKey == "properties":
                # recursive !!
                print('  odm_item_object: recurse!! itemkey:', itemKey, itemValue)
                output = output + "\"" + itemKey + "\": " 
                output += "{" + odm_property_object(itemValue, "sub") + "}"
            elif itemKey == "required":
                # recursive !!
                print('  odm_item_object: recurse!! itemkey:', itemKey, itemValue)
                output = output + "\"" + itemKey + "\": " 
                output = output + odm_enum_array(itemValue)
            elif isinstance(itemValue, Number):
                output = output + "\"" + itemKey + "\": " 
                output += str(itemValue)
            else:
                print('\n  odm_item_object: default string type:', type(itemValue), '\n')
                output = output + "\"" + itemKey + "\": " 
                output += "\"" + str(itemValue) + "\""
        if i < len(itemObject)-1:
            output += ","
        else:
            output += "}"
        i = i+1
    
    print ( "odm_item_object : leave", flush=True)
    return output

def odm_ref_properties(json_data, url):
    """
    load referenced json property and return string formatted as odm json schema
    :param json_data: json_data of the inputted resource type
    :param url: location of schema file and reference property, e.g. https://openconnectivityfoundation.github.io/IoTDataModels/schemas/oic.baseresource.properties-schema.json#/definitions/range_integer
    :           or if local reference, #/definitions/AirFlowControlBatch-Retrieve
    :return: string formatted as json schema
    """
    print (" odm_ref_properties : ", url, flush=True)
    if "https" in url:
        ref_json_dict = load_json_schema_fromURL(url)
        odm_make_reference_external(ref_json_dict,url)
    elif "http" in url:
        ref_json_dict = load_json_schema_fromURL(url)
        odm_make_reference_external(ref_json_dict,url)
    else:
        ref_json_dict = json_data

    keyValue = url.split("/")[-1]
    print (" odm_ref_properties : keyValue: ", keyValue)
    
    output = ""
    lookup = None
    try:
        lookup = ref_json_dict['definitions'][keyValue]
    except:
        print ("!!!!odm_ref_properties : error in finding", keyValue, flush=True)
        

    output += odm_properties_block(lookup)

    print (" odm_ref_properties : leave ", flush=True)
    return output 

def odm_readOnly_object(RO_value):
    """
    Take the read only value and convert it for odm writable property
    :param RO_value: Read only value string
    :return: json formatted string
    """ 
    if RO_value:
        #"readOnly" = true
        #"writeable" = false
        return "false"
    else:
        #"readOnly" = false
        #"writeable" = true
        return "true"

def odm_enum_array(enumArray):
    """
    Take the enum array value and additionally parse for odm 
    :param enumArray: array of items associated with enum type
    :return: json formatted string
    """
    output = "["
    for i, item in enumerate(enumArray):
        output = output + "\"" + item + "\""
        if i < len(enumArray)-1:
            output = output + ","
        else:
            output = output + "]"
    return output

def load_json_schema_fromURL(url):
    """
    load the JSON schema file
    :param url: location of schema file, e.g. https://openconnectivityfoundation.github.io/IoTDataModels/schemas/oic.baseresource.properties-schema.json#/definitions/range_integer
    :return: json_dict
    """
    response = requests.get(url)
    json_dict = json.loads(response.text, parse_float=float, object_pairs_hook=OrderedDict)
    return json_dict

def odm_return_path_info(json_data, returnType):
    """
    Return ocf resource type name: OCF name, e.g. oic.r.grinderAppliance returns grinderAppliance or grinderApplianceResURI
    :json_data: inputted resource type file
    :returnType: "name" or "path" or "description"
    :return: if returnType: "name" - string formatted name: e.g. grinder 
                returnType: "description" - returns the description property of the "get" path, 
                returnType: "path" the path name, e.g. /GrinderResURI
    """
    rt = swagger_rt(json_data)
    name = rt[0][1]
    path = rt[0][0]
    name = name.replace('oic.r.','')

    if len(rt) > 1:
        print("WARNING: More than one path found: ", rt)
    if returnType == "name":
        return name
    elif returnType == "description":
        return escape_quotes (remove_nl_crs (json_data["paths"][path]["get"]["description"], True))
    else:
        return path

def odm_verify_writeable_properties(json_data):
    """
    (Unused) Return ocf  type name: OCF name, e.g. oic.r.grinder returns grinder
    :json_data: inputted resource type file
    :input_path: pathname for get/post
    :returnType: "name" or "path"
    :return: if returnType = "name, string formatted name: e.g. grinder
    :        else, the path name, e.g. GrinderResURI
    """
    input_path = odm_return_path_info(json_data, "path")
    postList = swagger_properties_filtered_post(json_data, input_path)
    getList = swagger_properties_filtered(json_data, input_path)
    if postList == getList:
        print("Lists are the same")
    else:
        print("Lists are different")

def sdf_is_writeable(json_value):
    """
    Return the required object block for one-data-model
    :param json_value: json object for resource type
    :return: true if one of the properties is writable
    """ 
    #print ( "sdf_is_writeable")
    returnvalue=False
    try:
        odmObjects = json_data["odmObject"]
        for objname, obj_param in odmObjects.items():
            for paramname, paramobj in obj_param["odmProperty"].items():
               for qualname, qualobj in paramobj.items():
                   if qualname == "writeable":
                       if qualobj == True:
                            returnvalue=True
    except:
        print ("sdf_is_writeable: error in ", args.swagger)
        traceback.print_exc()
        pass
    
    return returnvalue
    
    
def sdf_resolve_odmRef(json_dict):
    """
    Return the required object block for one-data-model
    :param json_value: json object for resource type
    :return: true if one of the properties is writable
    """ 
    try:
        #print ( "sdf_resolve_odmRef", json_dict)
        if isinstance(json_dict, dict):
          if "odmRef" in json_dict:
            my_path = json_dict["odmRef"]
            #print ("    ", my_path)
            #print ("    ", json_data)
            my_path_segments = my_path.split("/")
            my_data = json_data
            for path_seg in my_path_segments:
                print (path_seg)
                if path_seg != "#":
                    my_data = my_data[path_seg]
            #print (my_data)
            return my_data
        else:
            return json_dict
    
    except:
                traceback.print_exc()
    
    return json_dict
    

def remove_nl_crs(my_string, replaceWithSpaces=False):
    """
    Remove New line (slash-n) and Carriage Returns (slash-r)
    :param my_value the string to be escaped
    :return: flattened string
    """
    # remove new line
    new_string=""
    data= my_string.split('\n')
    for item in data:
      #remove spaces, then add a single space (catches newlines without spaces)
      new_string = new_string.rstrip() + " " + item.lstrip() 
    
    # remove carrage return
    new_string2=""
    data= new_string.split('\r')
    for item in data:
        #remove spaces, then add a single space (catches CRs without spaces)
        new_string2 = new_string2.rstrip() + " " + item.lstrip() 
    if replaceWithSpaces:
        new_string2 = re.sub(r'\.(?! )', '. ', new_string2)
        new_string2 = new_string2.strip()
    return new_string2

def escape_escapes(my_string):
    """
    convert '\' to '\\''
    :param my_value the string to be escaped
    :return: string with escaped
    """
    my_string = my_string.replace('\\','\\\\')
    return my_string

def decamel_name(name):
    """
    Return decamelized name:grinderAppliance returns grinder appliance
    :name: inputted resource type file
    :return: space delimited name
    """
    name = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', name)
    return name.lower()

#
#   main of script
#

# version information
my_version = ""
try:
    from version import VERSION

    my_version = VERSION
except:
    pass

print ("************************")
print ("swagger2x ", my_version)
print ("************************")
parser = argparse.ArgumentParser()

parser.add_argument( "-ver"        , "--verbose"    , help="Execute in verbose mode", action='store_true')

parser.add_argument( "-swagger"    , "--swagger"    , default=None,
                     help="swagger file name",  nargs='?', const="", required=True)
#parser.add_argument( "-schema"     , "--schema"     , default=None,
#                     help="schema to be added to word document",  nargs='?', const="", required=False)
parser.add_argument( "-template"     , "--template"     , default=None,
                     help="template to be used",  nargs='?', const="", required=True)
parser.add_argument( "-template_dir"     , "--template_dir"     , default=None,
                     help="template directory",  nargs='?', const="", required=True)

parser.add_argument( "-schemadir"  , "--schemadir"  , default=".",
                     help="path to dir with additional referenced schemas",  nargs='?', const="", required=False)
parser.add_argument( "-out_dir"  , "--out_dir"  , default=".",
                     help="output dir",  nargs='?', const="", required=True)
# generation values
parser.add_argument( "-uuid"  , "--uuid"  , default="9b8fadc6-1e57-4651-bab2-e268f89f3ea7",
                     help="uuid",  nargs='?', const="", required=False)
parser.add_argument( "-manufacturer"  , "--manufacturer"  , default="ocf",
                     help="manufacturer name",  nargs='?', const="", required=False)
parser.add_argument( "-devicetype"  , "--devicetype"  , default="oic.d.light",
                     help="device type , e.g. oic.d.xxx",  nargs='?',  required=False)
#output file
parser.add_argument( "-output_file"  , "--output_file"  , default=None,
                     help="output file , e.g. <filename>.sdf.json",  nargs='?',  required=False)
                     #output file
parser.add_argument( "-jsonindent"  , "--jsonindent"  , default=None,
                     help="jsonindent , e.g. 2",  nargs='?',  required=False)

#(args) supports batch scripts providing arguments
print (sys.argv)
args = parser.parse_args()


print("file          : " + str(args.swagger))
print("out_dir       : " + str(args.out_dir))
print("out_file      : " + str(args.output_file))
print("jsonindent    : " + str(args.jsonindent))
#print("schema        : " + str(args.schema))
print("schemadir     : " + str(args.schemadir))
print("template      : " + str(args.template))
print("template_dir  : " + str(args.template_dir))
print("")
print("uuid          : " + str(args.uuid))
print("device type   : " + str(args.devicetype))
print("manufacturer  : " + str(args.manufacturer))
print("")

try:
    #if os.path.isfile(args.swagger) is False:
    #    print( "swagger file not found:", args.swagger)

    if os.path.exists(args.template_dir) is False:
        print( "template_dir not found:", args.template_dir)

    full_path = os.path.join(args.template_dir, args.template)
    #if os.path.exists((full_path) is False:
    #    print( "template not found:", args.template)

    json_data = load_json_schema(args.swagger)
    object_string = json.dumps(json_data, sort_keys=True, indent=2, separators=(',', ': '))
    print ("parse tree of input file:")
    print (object_string)
    # always in the same order..
    json_dict = json.loads(object_string)
    
    

    template_files = get_dir_list(full_path, ".jinja2")
    env = Environment(loader=FileSystemLoader(full_path))
    env.tests['hasbody'] = ishasbody
    env.filters['classsyntax'] = classsyntax
    env.filters['variablesyntax'] = variablesyntax
    env.filters['variableforbidden'] = variableforbidden
    env.filters['convert_to_c_type'] = convert_to_c_type
    env.filters['convert_to_c_type_no_pointer'] = convert_to_c_type_no_pointer
    env.filters['convert_to_c_type_array_size'] = convert_to_c_type_array_size
    env.filters['get_c_data'] = get_c_data
    
    
    env.filters['convert_to_cplus_type'] = convert_to_cplus_type
    env.filters['convert_to_cplus_array_type'] =convert_to_cplus_array_type

    env.filters['convert_to_c_type_array'] = convert_to_cplus_string_array
    env.filters['convert_array_size'] = convert_array_size
    env.filters['code_indent'] = code_indent
    env.filters['convert_value_to_c_value'] = convert_value_to_c_value
    env.filters['init_value_if_empty'] = init_value_if_empty
    env.filters['escape_quotes'] = escape_quotes
    env.filters['sdf_resolve_odmRef'] = sdf_resolve_odmRef

    for template_file in template_files:
        print ("processing:", template_file)
        template_environment = env.get_template(template_file)
        # add the custom functions
        template_environment.globals['replace_chars'] = replace_chars
        template_environment.globals['path_names'] = path_names
        template_environment.globals['query_ref'] = query_ref
        template_environment.globals['query_rt'] = retrieve_rt_from_path
        template_environment.globals['query_if'] = swagger_if
        template_environment.globals['query_if_exist'] = swagger_if_exist
        template_environment.globals['query_property_names'] = swagger_property_names
        template_environment.globals['swagger_property_data_schema'] = swagger_property_data_schema
        template_environment.globals['query_properties'] = swagger_properties
        template_environment.globals['query_properties_post'] = swagger_properties_post
        template_environment.globals['query_properties_filtered'] = swagger_properties_filtered
        template_environment.globals['query_properties_filtered_post'] = swagger_properties_filtered_post
        template_environment.globals['query_required_items'] = swagger_required_items
        
        template_environment.globals['list_query_params'] = list_query_params

        template_environment.globals['retrieve_path_value'] = retrieve_path_value
        template_environment.globals['retrieve_path_dict'] = retrieve_path_dict
        # new functions for ODM
        template_environment.globals['odm_return_path_info'] = odm_return_path_info
        template_environment.globals['odm_property_object'] = odm_property_object
        template_environment.globals['odm_required_block_check'] = odm_required_block_check
        template_environment.globals['odm_required_object'] = odm_required_object
        template_environment.globals['sdf_is_writeable'] = sdf_is_writeable
        #template_environment.globals['sdf_resolve_odmRef'] = sdf_resolve_odmRef
        
        #check for whether this model is supported for one-data-model
        if args.template == "one-data-model":
            if not odm_supported_model(json_data, args.swagger):
                #prevent parsing of file
                print("modelNotSupported :", args.swagger)
                #quit()
                exit()

        print(" rendering ...\n ");
        text = template_environment.render( json_data=json_data,
            version=my_version,
            uuid= str(args.uuid),
            manufacturer= str(args.manufacturer),
            device_type= str(args.devicetype),
            input_file = args.swagger,
            output_file = args.output_file)
        print(" rendering ...complete.\n ");

        if args.out_dir is not None:
            if (args.output_file) is None:
                outputfile = template_file.replace(".jinja2", "")
                out_file = os.path.join(args.out_dir, outputfile)
            else:
                out_file = os.path.join(args.out_dir, args.output_file) 

            if args.template == "one-data-model":
                #clean json structure. remove extra lines from jinja2 template 
                #(break if invalid json, caught by outer try loop)
                if args.output_file == "auto":
                    #Generate name from resource name for ODM, override out_file
                    #Replace '.' with '_' in oic.r.* names, e.g. oic.r.speech.tts = speech_tts
                    out_file = os.path.join(args.out_dir, ("odmobject-" + odm_return_path_info(json_data, "name").replace('.','_') + ".sdf.json"))
                
                if args.jsonindent is not None:
                    output_json_dict = json.loads(remove_nl_crs(text), object_pairs_hook=OrderedDict)
                    f = open(out_file, 'w')
                    f.write(json.dumps(output_json_dict,indent=2))
                    #Add final \n for github
                    f.write('\n')
                    f.close()
                else:
                    f = open(out_file, 'w')
                    f.write(text)
                    #Add final \n for github
                    f.write('\n')
                    f.close()
            else:
                #standard file output
                #print(" \n\n\n ", text);
                f = open(out_file, 'w')
                if args.jsonindent is not None:
                    output_json_dict = json.loads(remove_nl_crs(text), object_pairs_hook=OrderedDict)
                    f.write(json.dumps(output_json_dict,indent=2))
                    #Add final \n for github
                    f.write('\n')
                else:
                    f.write(text)
                f.close()

    # copy none jinja2 files from Template dir
    all_files = get_dir_list(full_path)
    for file in all_files:
        if ".jinja2" in file:
            continue
        if ".bak" in file:
            continue
        source_file =  os.path.join(full_path, file)
        destination_file =  os.path.join(args.out_dir, file)
        print ("copying template file: ", file)
        copyfile(source_file, destination_file)


except:
    traceback.print_exc()
    #print ("error in ", args.swagger)
    #pass
