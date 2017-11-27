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
*/

using namespace std;
using namespace OC;

class IoTServer
{
    shared_ptr<PlatformConfig> m_platformConfig;
    void initializePlatform();
    void setupResources();
    void createResource(string, string, EntityHandler, OCResourceHandle&);
 
    // path: /TemperatureResURI
    OCRepresentation m_TemperatureResURIRepresentation;
    OCResourceHandle m_TemperatureResURIResourceHandle;
    ObservationIds m_TemperatureResURIObservers;
    shared_ptr<IoTObserver> m_TemperatureResURIObserverLoop;
    OCRepresentation get_TemperatureResURIRepresentation();
    OCEntityHandlerResult m_TemperatureResURIEntityHandler(shared_ptr<OCResourceRequest>);


    // variables for the resources
 
    static string m_TemperatureResURI_RESOURCE_ENDPOINT = "/TemperatureResURI";  // used path
    static string m_TemperatureResURI_RESOURCE_TYPE[] = {"oic.r.temperature"}; // rt value (should be an array)
    static string m_TemperatureResURI_RESOURCE_INTERFACE[] = {"oic.if.baseline","oic.if.ll","oic.if.b","oic.if.lb","oic.if.rw","oic.if.r","oic.if.a","oic.if.s"}; // interface if  
    // membervariables for path: /TemperatureResURI
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_id = "id"; // the name for the attribute
    std::string m_TemperatureResURI_id; // the value for the attribute
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_value = "value"; // the name for the attribute
    void* m_TemperatureResURI_value; // the value for the attribute
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_range = "range"; // the name for the attribute
    void* m_TemperatureResURI_range; // the value for the attribute
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_temperature = "temperature"; // the name for the attribute
    float m_TemperatureResURI_temperature; // the value for the attribute
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_n = "n"; // the name for the attribute
    std::string m_TemperatureResURI_n; // the value for the attribute
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_if = "if"; // the name for the attribute
    void* m_TemperatureResURI_if; // the value for the attribute
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_step = "step"; // the name for the attribute
    void* m_TemperatureResURI_step; // the value for the attribute
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_units = "units"; // the name for the attribute
    void* m_TemperatureResURI_units; // the value for the attribute
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_rt = "rt"; // the name for the attribute
    void* m_TemperatureResURI_rt; // the value for the attribute
    static string m_TemperatureResURI_RESOURCE_PROPERTY_NAME_precision = "precision"; // the name for the attribute
    float m_TemperatureResURI_precision; // the value for the attribute

    // OCPlatformInfo Contains all the platform info to be stored
    OCPlatformInfo m_platformInfo;
    
    // delete the platform information
    void DeletePlatformInfo();
    
    // set the platform information
    OCStackResult SetPlatformInfo(std::string platformID, std::string manufacturerName,
        std::string manufacturerUrl, std::string modelNumber, std::string dateOfManufacture,
        std::string platformVersion, std::string operatingSystemVersion,
        std::string hardwareVersion, std::string firmwareVersion, std::string supportUrl,
        std::string systemTime);
      
    // set the device information      
    OCStackResult SetDeviceInfo();

public:
    IoTServer();
    virtual ~IoTServer();
};

#endif /* SERVER_H_ */