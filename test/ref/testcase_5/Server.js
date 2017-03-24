//    copyright 2016 Open Interconnect Consortium, Inc. All rights reserved.
//
//    Redistribution and use in source and binary forms, with or without modification,
//    are permitted provided that the following conditions are met:
//    1.  Redistributions of source code must retain the above copyright notice,
//        this list of conditions and the following disclaimer.
//    2.  Redistributions in binary form must reproduce the above copyright notice,
//        this list of conditions and the following disclaimer in the documentation and/or other materials provided
//        with the distribution.
//         
//    THIS SOFTWARE IS PROVIDED BY THE OPEN INTERCONNECT CONSORTIUM, INC. "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
//    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE OR
//    WARRANTIES OF NON-INFRINGEMENT, ARE DISCLAIMED. IN NO EVENT SHALL THE OPEN INTERCONNECT CONSORTIUM, INC. OR
//    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
//    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
//    OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
//    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
//    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
// Generated code from swagger2x
// generates an IOTivity node server based on
// https://github.com/otcshare/iotivity-node
// documentation available at:
// https://github.com/01org/iot-js-api/tree/master/api/ocf

var intervalId;
var iotivity = require( "iotivity-node/lowlevel" );

// resource_handles for each end point  
// path /TemperatureResURI
var  _TemperatureResURI_handle = {};
// list all variables as globals
var _temperature; // readonly:  type: number description: Current temperature setting or measurement
var _range; // readonly:  type: array description: The valid range for the value Property
var _units; // readonly: True type:  description: Units for the temperature value
var _rt; // readonly: True type: array description: Resource Type
var _id; // readonly: True type: string description: Instance ID of this specific resource
var _n; // readonly: True type: string description: Friendly name of the resource
var _precision; // readonly: True type: number description: Accuracy granularity of the exposed value
var _if; // readonly: True type: array description: The interface set supported by this resource
var _step; // readonly: True type:  description: Step value across the defined range
var _value; // readonly:  type:  description: The value sensed or actuated by this Resource
console.log( "Starting OCF stack in server mode" );

// Start iotivity and set up the processing loop
iotivity.OCInit( null, 0, iotivity.OCMode.OC_SERVER );

// set the device data
iotivity.OCSetDeviceInfo( {
	specVersion: "res.1.1.0",
	dataModelVersions: [ "abc.0.0.1" ],
	deviceName: "OICTemperature",
	types: []
} );
// set the platform data
iotivity.OCSetPlatformInfo( {
	platformID: "9b8fadc6-1e57-4651-bab2-e268f89f3ea7",
	manufacturerName: "ocf.org"
} );
// helper function
intervalId = setInterval( function() {
	iotivity.OCProcess();
}, 1000 );

console.log( "Registering resources" );
// Create a new resource for /TemperatureResURI
iotivity.OCCreateResource(
	// The bindings fill in this object
	_TemperatureResURI_handle,
    iotivity.OC_RSRVD_INTERFACE_DEFAULT, //['oic.if.a', 'oic.if.s', 'oic.if.baseline'], // this should be an array in the API
    "['oic.r.temperature']", // this should be an array in the API
	"/TemperatureResURI",
	function( flag, request ) {
		console.log( "Entity handler called with flag = " + flag + " and the following request:" );
		console.log( JSON.stringify( request, null, 4 ) );
       
        // POST method
		if ( request && request.method === iotivity.OCMethod.OC_REST_POST ) {
            
            // list the query params for post
            var _if = "" ; // string 
            if (request._if != undefined ) {
                // possible values: ['oic.if.a', 'oic.if.s', 'oic.if.baseline'].
                _if = request._if ;
            }
            if ( request && request.payload)
            {
              // update the global variables
              _temperature = request.payload.temperature;
              _id = request.payload.id;
              }
            // do something with the new values like printing them..
            console.log( "new value (temperature) : " + _temperature );
            console.log( "new value (id) : " + _id );
            iotivity.OCDoResponse( {
				requestHandle: request.requestHandle,
				resourceHandle: request.resource,
				ehResult: iotivity.OCEntityHandlerResult.OC_EH_OK,
				payload: {
					type: iotivity.OCPayloadType.PAYLOAD_TYPE_REPRESENTATION,
					values: {
						"temperature" : _temperature,
                        "id" : _id
                        }
				},
				resourceUri: "/TemperatureResURI",
				sendVendorSpecificHeaderOptions: []
			} );
            return iotivity.OCEntityHandlerResult.OC_EH_OK;
        }
        // GET method
		if ( request && request.method === iotivity.OCMethod.OC_REST_GET ) {
        
            // list the query params for get
            var _if = ""; // string 
            if (request._if != undefined ) {
               // possible values: ['oic.if.a', 'oic.if.s', 'oic.if.baseline'].
               _if = request._if;
            }
            var _units = "" ;  // string Units
            if (request.units != undefined ) {
                // possible values: ['C', 'F', 'K']
               _units = request.units ;
            }
            iotivity.OCDoResponse( {
				requestHandle: request.requestHandle,
				resourceHandle: request.resource,
				ehResult: iotivity.OCEntityHandlerResult.OC_EH_OK,
				payload: {
					type: iotivity.OCPayloadType.PAYLOAD_TYPE_REPRESENTATION,
					values: {
                        "range" : _range,
                        "temperature" : _temperature,
                        "units" : _units,
                        "id" : _id,
                        "rt" : _rt
                        }
				},
				resourceUri: "/TemperatureResURI",
				sendVendorSpecificHeaderOptions: []
			} );
            return iotivity.OCEntityHandlerResult.OC_EH_OK; 
        }            
        // By default we error out
		return iotivity.OCEntityHandlerResult.OC_EH_ERROR;
	},
    // always discoverable
	iotivity.OCResourceProperty.OC_DISCOVERABLE );

console.log( "Server ready" );

// Exit gracefully when interrupted
process.on( "SIGINT", function() {
    console.log( "SIGINT: Quitting..." );

    // Tear down the processing loop and stop iotivity
    clearInterval( intervalId );
    // deleting all handles
    iotivity.OCDeleteResource( _TemperatureResURI_handle.handle );
    // stop the stack
    iotivity.OCStop();
    // Exit
    process.exit( 0 );
} );