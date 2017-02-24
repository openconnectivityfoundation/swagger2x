
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

var intervalId;
var iotivity = require( "iotivity-node/lowlevel" );
    

// path /BinarySwitchResURI
var  BinarySwitchResURI;


console.log( "Starting OCF stack in server mode" );

// Start iotivity and set up the processing loop
iotivity.OCInit( null, 0, iotivity.OCMode.OC_SERVER );

iotivity.OCSetDeviceInfo( {
	specVersion: "res.1.1.0",
	dataModelVersions: [ "abc.0.0.1" ],
	deviceName: "oic.d.light",
	types: []
} );
iotivity.OCSetPlatformInfo( {
	platformID: "9b8fadc6-1e57-4651-bab2-e268f89f3ea7",
	manufacturerName: "ocf.org"
} );

intervalId = setInterval( function() {
	iotivity.OCProcess();
}, 1000 );

console.log( "Registering resource" );




// Create a new resource
iotivity.OCCreateResource(

	// The bindings fill in this object
	BinarySwitchResURI,

	"core.fan",
	iotivity.OC_RSRVD_INTERFACE_DEFAULT,
	"/BinarySwitchResURI",
	function( flag, request ) {
		console.log( "Entity handler called with flag = " + flag + " and the following request:" );
		console.log( JSON.stringify( request, null, 4 ) );

		// If we find the magic question in the request, we return the magic answer
		if ( request && request.payload && request.payload.values &&
				request.payload.values.question ===
				"How many angels can dance on the head of a pin?" ) {

			iotivity.OCDoResponse( {
				requestHandle: request.requestHandle,
				resourceHandle: request.resource,
				ehResult: iotivity.OCEntityHandlerResult.OC_EH_OK,
				payload: {
					type: iotivity.OCPayloadType.PAYLOAD_TYPE_REPRESENTATION,
					values: {
						"answer": "As many as wanting."
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


    
console.log( "Server ready" );

// Exit gracefully when interrupted
process.on( "SIGINT", function() {
	console.log( "SIGINT: Quitting..." );

	// Tear down the processing loop and stop iotivity
	clearInterval( intervalId );
    // deleting all handles

    iotivity.OCDeleteResource( BinarySwitchResURI.handle );

	iotivity.OCStop();

	// Exit
	process.exit( 0 );
} );