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
// path /BinarySwitchResURI
var _BinarySwitchResURI_handle = {};
var _BinarySwitchResURI_resourceTypes = oic.r.switch.binary;
var _BinarySwitchResURI_interfaces = ['oic.if.a'];
// list all variables as globals
var _if; // readonly:  type: array description: ReadOnly, The interface set supported by this resource
var _rt; // readonly:  type: string description: ReadOnly, Resource Type
var _value; // readonly:  type: boolean description: Status of the switch
var _p; // readonly:  type: string description: ReadOnly, bitmap indicating observable and discoverable
var _range; // readonly:  type: string description: 
var _id; // readonly:  type: string description: ReadOnly, Instance ID of this specific resource
var _n; // readonly:  type: string description: Friendly name of the resource
console.log( "Starting OCF stack in server mode" );

// Start iotivity and set up the processing loop
iotivity.OCInit( null, 0, iotivity.OCMode.OC_SERVER );

// set the device data
iotivity.OCSetPropertyValue( iotivity.OCPayloadType.PAYLOAD_TYPE_DEVICE,
	iotivity.OC_RSRVD_SPEC_VERSION, "res.1.1.0" );
iotivity.OCSetPropertyValue( iotivity.OCPayloadType.PAYLOAD_TYPE_DEVICE,
	iotivity.OC_RSRVD_DATA_MODEL_VERSION, "abc.0.0.1" );
iotivity.OCSetPropertyValue( iotivity.OCPayloadType.PAYLOAD_TYPE_DEVICE,
	iotivity.OC_RSRVD_DEVICE_NAME, "OICBinarySwitch" );

// set the platform data
iotivity.OCSetPropertyValue( iotivity.OCPayloadType.PAYLOAD_TYPE_PLATFORM,
	iotivity.OC_RSRVD_PLATFORM_ID, "9b8fadc6-1e57-4651-bab2-e268f89f3ea7" );
iotivity.OCSetPropertyValue( iotivity.OCPayloadType.PAYLOAD_TYPE_PLATFORM,
	iotivity.OC_RSRVD_MFG_NAME, "ocf.org" );

// helper functions
intervalId = setInterval( function() {
	iotivity.OCProcess();
}, 1000 );

function validateResourceProperties( theArray ) {
    var index;

    if ( Array.isArray( theArray ) && theArray.length > 0 ) {
        for ( index in theArray ) {
            if ( typeof theArray[ index ] !== "string" ) {
                return false;
            }
        }
        return true;
    }

    return false;
}

function bindStringsToResource( handle, strings, binder ) {
    var index, result;

    for ( index = 0; index < strings.length; index++ ) {
         result = iotivity[ binder ]( handle, strings[ index ] );
         if ( result !== iotivity.OCStackResult.OC_STACK_OK ) {
             console.log( "Error: Failed to perform: " + binder );
             return false;
         }
    }

    return true;
}

console.log( "Registering resources" );

if ( !( validateResourceProperties( _BinarySwitchResURI_resourceTypes ) &&
        validateResourceProperties( _BinarySwitchResURI_interfaces ) ) ) {
    console.log( "Error: Invalid resource properties" );
    exitHandler();
}

// Create a new resource for /BinarySwitchResURI
iotivity.OCCreateResource(
	// The bindings fill in this object
	_BinarySwitchResURI_handle,
	_BinarySwitchResURI_resourceTypes[ 0 ],
	_BinarySwitchResURI_interfaces[ 0 ],
	"/BinarySwitchResURI",
	function( flag, request ) {
		console.log( "Entity handler called with flag = " + flag + " and the following request:" );
		console.log( JSON.stringify( request, null, 4 ) );
       
        // GET method
		if ( request && request.method === iotivity.OCMethod.OC_REST_GET ) {
        
            // list the query params for get
            var _if = ""; // string 
            if (request["if"] != undefined ) {
               // possible values: ['oic.if.a'].
               _if = request["if"];
            }
            iotivity.OCDoResponse( {
				requestHandle: request.requestHandle,
				resourceHandle: request.resource,
				ehResult: iotivity.OCEntityHandlerResult.OC_EH_OK,
				payload: {
					type: iotivity.OCPayloadType.PAYLOAD_TYPE_REPRESENTATION,
					values: {
                        "rt" : _rt,
                        "value" : _value,
                        "id" : _id
                        }
				},
				resourceUri: "/BinarySwitchResURI",
				sendVendorSpecificHeaderOptions: []
			} );
            return iotivity.OCEntityHandlerResult.OC_EH_OK; 
        }            
        // POST method
		if ( request && request.method === iotivity.OCMethod.OC_REST_POST ) {
            
            // list the query params for post
            var _if = "" ; // string 
            if (request["if"] != undefined ) {
                // possible values: ['oic.if.a'].
                _if = request["if"] ;
            }
            if ( request && request.payload)
            {
              // update the global variables
              _id = request.payload.id;
              _value = request.payload.value;
              }
            // do something with the new values like printing them..
            console.log( "new value (id) : " + _id );
            console.log( "new value (value) : " + _value );
            iotivity.OCDoResponse( {
				requestHandle: request.requestHandle,
				resourceHandle: request.resource,
				ehResult: iotivity.OCEntityHandlerResult.OC_EH_OK,
				payload: {
					type: iotivity.OCPayloadType.PAYLOAD_TYPE_REPRESENTATION,
					values: {
						"id" : _id,
                        "value" : _value
                        }
				},
				resourceUri: "/BinarySwitchResURI",
				sendVendorSpecificHeaderOptions: []
			} );
            return iotivity.OCEntityHandlerResult.OC_EH_OK;
        }
        // By default we error out
		return iotivity.OCEntityHandlerResult.OC_EH_ERROR;
	},
    // always discoverable
	iotivity.OCResourceProperty.OC_DISCOVERABLE );

if ( !( bindStringsToResource( _BinarySwitchResURI_handle.handle,  _BinarySwitchResURI_resourceTypes.slice( 1 ),
                "OCBindResourceTypeToResource") &&
        bindStringsToResource( _BinarySwitchResURI_handle.handle,  _BinarySwitchResURI_interfaces.slice( 1 ),
                "OCBindResourceInterfaceToResource" ) ) ) {
    exitHandler();
}

console.log( "Server ready" );

// Cleanup when interrupted
function exitHandler() {
    console.log( "SIGINT: Quitting..." );

    // Tear down the processing loop and stop iotivity
    clearInterval( intervalId );
    // deleting all handles
    if ( _BinarySwitchResURI_handle.handle )
        iotivity.OCDeleteResource( _BinarySwitchResURI_handle.handle );
    // stop the stack
    iotivity.OCStop();
    // Exit
    process.exit( 0 );
}

// Exit gracefully when interrupted
process.on('SIGINT', exitHandler);