#############################
#
#    copyright 2016 Open Interconnect Consortium, Inc. All rights reserved.
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
# tool_version          : 20171123
# input_file            : ../test/in/test_swagger_1/test_swagger_1.swagger.json
# version of input_file : v1.0.0-20151223
# title of input_file   : oic.d.light

import os
import shutil
import subprocess
import sys
import time
import threading
import json

from flask import Flask, render_template, jsonify, redirect, abort, request, send_from_directory, Response
app = Flask(__name__)



# path /BinarySwitchResURI

# method: get
@app.route('/BinarySwitchResURI', methods=['get'])
def get__BinarySwitchResURI():
    # Method: get
    # description : This resource describes a binary switch (on/off).@crThe value is a boolean.@crA value of <COMMA>true<COMMA> means that the switch is on.@crA value of <COMMA>false<COMMA> means that the switch is off.@cr
    # query params
    
    
      
    # property name : #/parameters/interface : if 
    # enum     : ['oic.if.a']
    # required     : 
    __if = request.args.get('if')
    
    

    
    
    response_200 = 200
    response_200_example = {'value': False, 'id': 'unique_example_id', 'rt': 'oic.r.switch.binary'}
    # schema: {'$ref': '#/definitions/BinarySwitch'}
    return Response(json.dumps(response_200_example),  mimetype='application/json')
    


# method: post
@app.route('/BinarySwitchResURI', methods=['post'])
def post__BinarySwitchResURI():
    # Method: post
    # description : 
    # query params
    
    
      
    # property name : #/parameters/interface : if 
    # enum     : ['oic.if.a']
    # required     : 
    __if = request.args.get('if')
    
     
         
    # example body: {'value': True, 'id': 'unique_example_id'}
    # data in string format and you have to parse into dictionary
    req_data = request.data
    req_data_dict = json.loads(req_data)
    

    
    
    response_200 = 200
    response_200_example = {'value': True, 'id': 'unique_example_id'}
    # schema: {'$ref': '#/definitions/BinarySwitch'}
    return Response(json.dumps(response_200_example),  mimetype='application/json')
    




if __name__ == '__main__':

    HOST_NAME = 'localhost';
    SERVER_PORT = 8888;

    # set the execution path of the tool
    if hasattr(sys, 'frozen'):
        my_dir = os.path.dirname(sys.executable)
    else:
        my_dir = os.path.dirname(sys.argv[0])

    if my_dir:
        os.chdir(my_dir)

    app.run(host=HOST_NAME, port=int(SERVER_PORT), debug=True)
    #app.run(use_debugger=True)