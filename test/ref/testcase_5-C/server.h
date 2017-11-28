//******************************************************************
//
// Copyright 2017 Open Connectivity Foundation
//
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#ifndef SERVER_H_
#define SERVER_H_

#include <string>
#include <iostream>
#include <memory>
#include "ocstack.h"
#include "observer.h"
#include "OCPlatform.h"
#include "OCApi.h"

/*
 tool_version          : 20171123
 input_file            : ../test/in/test_swagger_5/TemperatureResURI.swagger.json
 version of input_file : v1.1.0-20160519
 title of input_file   : OICTemperature
 
 
 typical device resource tree
 
 |-- oic/res
 |
 |-- oic/p
 |-- oic/d
 |-- virtual security resources
 |
 |-- resource-1
 .
 |-- resource-n
 
 content of oic/res is determined by the resources that are tagged with OC_DISCOVERABLE
 oic/p : content is determined by the globals in the cpp file
 oic/d : content is determined by the globals in the cpp file
 
*/

using namespace std;
using namespace OC;

class IoTServer
{

// path: /TemperatureResURI
    // the resource representation
    OCRepresentation m_TemperatureResURIRepresentation;
    // the resource handle
    OCResourceHandle m_TemperatureResURIResourceHandle;
    // the list of observers
    ObservationIds m_TemperatureResURIObservers;
    // the list of observers
    shared_ptr<IoTObserver> m_TemperatureResURIObserverLoop;
    /**
    *  method for /TemperatureResURI to respond to all observers if something is changed
    */
    void f_TemperatureResURIObserverLoopFunc();
    /**
    *  The entity handler for /TemperatureResURI
    * @param Request the request representation.
    */
    OCEntityHandlerResult f_TemperatureResURIEntityHandler(shared_ptr<OCResourceRequest> Request);
 
    /**
    *  get method for /TemperatureResURI to assign the values to be returned
    * @param requestRep the request representation.
    */
    OCRepresentation get_TemperatureResURIRepresentation(OCRepresentation requestRep);
 
    /**
    *  post method for /TemperatureResURI to assign the request values to the member values
    * @param requestRep the request representation.
    */
    OCRepresentation post_TemperatureResURIRepresentation(OCRepresentation requestRep);


    // variables for the resources

    static string m_TemperatureResURI_RESOURCE_ENDPOINT = "/TemperatureResURI";  // used path for this resource
    static string m_TemperatureResURI_RESOURCE_TYPE[] = {"oic.r.temperature"}; // rt value (as an array)
    static string m_TemperatureResURI_RESOURCE_INTERFACE[] = {"oic.if.baseline","oic.if.ll","oic.if.b","oic.if.lb","oic.if.rw","oic.if.r","oic.if.a","oic.if.s"}; // interface if (as an array) 

    // membervariables for path: /TemperatureResURI
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_n = "n"; // the name for the attribute
    std::string m_TemperatureResURI_n; // the value for the attribute 
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_temperature = "temperature"; // the name for the attribute
    float m_TemperatureResURI_temperature; // the value for the attribute 
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_precision = "precision"; // the name for the attribute
    float m_TemperatureResURI_precision; // the value for the attribute 
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_rt = "rt"; // the name for the attribute
    void* m_TemperatureResURI_rt; // the value for the attribute 
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_step = "step"; // the name for the attribute
    void* m_TemperatureResURI_step; // the value for the attribute 
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_range = "range"; // the name for the attribute
    void* m_TemperatureResURI_range; // the value for the attribute 
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_id = "id"; // the name for the attribute
    std::string m_TemperatureResURI_id; // the value for the attribute 
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_units = "units"; // the name for the attribute
    void* m_TemperatureResURI_units; // the value for the attribute 
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_if = "if"; // the name for the attribute
    void* m_TemperatureResURI_if; // the value for the attribute 
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_value = "value"; // the name for the attribute
    void* m_TemperatureResURI_value; // the value for the attribute // OCPlatformInfo Contains all the platform info to be stored
    OCPlatformInfo m_platformInfo;
    // the platform
    shared_ptr<PlatformConfig> m_platformConfig;
    
    /**
    *  intialize the platform
    */
    void initializePlatform();
    
    /**
    *  set up the resources
    */
    void setupResources();
    
    /**
    *  create Resource
    *  helper function used in initializePlatform()
    * @param Uri the URI of the resource, must be unique
    * @param Type the resource type (rt), the first one
    * @param resourceInterface the resource inteface (if), the first one
    * @param Cb the entity handler, to handle an incomming request for this resource
    * @param Handle the resourceHandle
    */
    void createResource(string Uri, string Type, string resourceInterface, EntityHandler Cb, OCResourceHandle& Handle);
    
    /**
    *  delete the platform information
    */
    void DeletePlatformInfo();
    
    /**
    *  set the platform information
    * @param platformID the platformID
    * @param manufacturerName the manufacturerName
    * @param manufacturerUrl the manufacturerUrl
    * @param modelNumber the modelNumber
    * @param platformVersion the platformVersion
    * @param operatingSystemVersion the operatingSystemVersion
    * @param hardwareVersion the hardwareVersion
    * @param firmwareVersion the firmwareVersion
    * @param supportUrl the supportUrl
    * @param systemTime the systemTime
    */
    OCStackResult SetPlatformInfo(std::string platformID, std::string manufacturerName,
        std::string manufacturerUrl, std::string modelNumber, std::string dateOfManufacture,
        std::string platformVersion, std::string operatingSystemVersion,
        std::string hardwareVersion, std::string firmwareVersion, std::string supportUrl,
        std::string systemTime);
      
    /**
    *  set the device information
    */    
    OCStackResult SetDeviceInfo();

public:
    IoTServer();
    virtual ~IoTServer();
};

#endif /* SERVER_H_ */