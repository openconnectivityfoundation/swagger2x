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
#include <signal.h>
#include <thread>
#include <functional>

#include "server.h"
//#include "sensors.h"
#include "namedefs.h"
//using namespace Sensors;


/*
 tool_version          : 20171123
 input_file            : ../test/in/test_swagger_5/TemperatureResURI.swagger.json
 version of input_file : v1.1.0-20160519
 title of input_file   : OICTemperature
*/

// Set of strings for each of platform Info fields
std::string gPlatformId = "0A3E0D6F-DBF5-404E-8719-D6880042463A";
std::string gManufacturerName = "OCF";
std::string gManufacturerLink = "https://openconnectivity.org/";
std::string gModelNumber = "ModelNumber";
std::string gDateOfManufacture = "2017-12-01";
std::string gPlatformVersion = "1.0";
std::string gOperatingSystemVersion = "myOS";
std::string gHardwareVersion = "1.0";
std::string gFirmwareVersion = "1.0";
std::string gSupportLink = "https://openconnectivity.org/";
std::string gSystemTime = "2017-12-01T12.00";

// Set of strings for each of device info fields
std::string  gDeviceName = "OICTemperature";
std::string  gDeviceType = "oic.wk.tv";
std::string  gSpecVersion = "ocf.1.3.0";
//std::vector<std::string> gDataModelVersions = {"ocf.res.1.1.0", "ocf.sh.1.1.0"};
std::vector<std::string> gDataModelVersions = {"ocf.res.1.3.0", "ocf.dev.1.3.0"};
std::string  gProtocolIndependentID = "fa008167-3bbf-4c9d-8604-c9bcb96cb712";


/**
*  DuplicateString
*
* @param targetString  destination string, will be allocated
* @param sourceString  soruce string, e.g. will be copied

*  TODO: don't use strncpy
*/
void DuplicateString(char ** targetString, std::string sourceString)
{
    *targetString = new char[sourceString.length() + 1];
    strncpy(*targetString, sourceString.c_str(), (sourceString.length() + 1));
}


/**
*  intialize platform
*  TODO: put here the security and introspection loading
*/
void IoTServer::initializePlatform()
{
    cout << "Running initializePlatform" << endl;
    m_platformConfig = make_shared<PlatformConfig>(ServiceType::InProc, ModeType::Server, "0.0.0.0",
                                                   0, OC::QualityOfService::HighQos);
    OCPlatform::Configure(*m_platformConfig);
    
    // initialize "oic/p"
    OCStackResult result = SetPlatformInfo(gPlatformId, gManufacturerName, gManufacturerLink,
            gModelNumber, gDateOfManufacture, gPlatformVersion, gOperatingSystemVersion,
            gHardwareVersion, gFirmwareVersion, gSupportLink, gSystemTime);
    result = OCPlatform::registerPlatformInfo(m_platformInfo);
    if (result != OC_STACK_OK)
    {
        std::cout << "Platform Registration (oic/p) failed\n";
    }
    
    // initialize "oic/d"
    result = SetDeviceInfo();
    if (result != OC_STACK_OK)
    {
        std::cout << "Device Registration (oic/p) failed\n";
    }
}

/**
*  constructor
*
*/
IoTServer::IoTServer()
{
    cout << "Running IoTServer constructor" << endl;
    initializePlatform();
    setupResources();  
}

/**
*  destructor
*
*/
IoTServer::~IoTServer()
{
    cout << "Running IoTServer destructor" << endl;
    //ClosePins();
    
    DeletePlatformInfo();
}

/**
*  method to setup all the resources.
*
*/
void IoTServer::setupResources()
{
    cout << "Running setupResources" << endl;EntityHandler cb1 = bind(&IoTServer::f_TemperatureResURIEntityHandler, this, placeholders::_1);
    createResource( m_TemperatureResURI_RESOURCE_ENDPOINT, 
                    m_TemperatureResURI_RESOURCE_TYPE[0], 
                    m_TemperatureResURI_RESOURCE_INTERFACE[0], cb1,
                    m_TemperatureResURIResourceHandle);
    IoTObserverCb temp_TemperatureResURICb = bind(&IoTServer::f_TemperatureResURIObserverLoopFunc, this);
    m_TemperatureResURIObserverLoop = make_shared<IoTObserver>(temp_TemperatureResURICb);
    // add the additional interfaces
    for( unsigned int a = 1; a < sizeof(m_TemperatureResURI_RESOURCE_INTERFACE); a++ )
    {
        OCStackResult result = OCBindResourceInterfaceToResource(m_TemperatureResURIResourceHandle, m_TemperatureResURI_RESOURCE_INTERFACE[a]);
        if (result != OC_STACK_OK)
            cerr << "Could not bind interface:" << m_TemperatureResURI_RESOURCE_INTERFACE[a] << endl;
    }
    // add the additional resource types
    for( unsigned int a = 1; a < sizeof(m_TemperatureResURI_RESOURCE_TYPE); a++1 )
    {
        OCStackResult result = OCBindResourceTypeToResource(m_TemperatureResURIResourceHandle, m_TemperatureResURI_RESOURCE_TYPE[a]);
        if (result != OC_STACK_OK)
            cerr << "Could not bind resource type:" << m_TemperatureResURI_RESOURCE_INTERFACE[a] << endl;
    }
 
    // initialize member variables for each resource
    // initialize member variables /TemperatureResURI 
    m_TemperatureResURI_n = "";  // current value of property "n"  
    m_TemperatureResURI_temperature = 0.0; // current value of property "temperature"  
    m_TemperatureResURI_precision = 0.0; // current value of property "precision"  
    m_TemperatureResURI_id = "";  // current value of property "id" 


}

/**
*  method to create the resource.
*
* @param Uri the URI to use.
* @param Type the resource type (rt).
* @param EntityHandler the entity handler for the resource.
* @param OCResourceHandle the resource handle
*/
void IoTServer::createResource(string Uri, string Type, string resourceInterface, EntityHandler Cb, OCResourceHandle& Handle)
{
    string resourceUri = Uri;
    string resourceType = Type;
    uint8_t resourceFlag = OC_DISCOVERABLE | OC_OBSERVABLE;

    OCStackResult result = OCPlatform::registerResource(Handle, resourceUri, resourceType,
                                                        resourceInterface, Cb, resourceFlag);

    if (result != OC_STACK_OK)
        cerr << "Could not create " << Type << " resource" << endl;
    else
        cout << "Successfully created " << Type << " resource" << endl;
}

/**
*  method for /TemperatureResURI to respond to all observers if something is changed
*/
void IoTServer::f_TemperatureResURIObserverLoopFunc()
{
    usleep(1500000);
    cout << "/TemperatureResURI Observer Callback" << endl;
    shared_ptr<OCResourceResponse> resourceResponse(new OCResourceResponse());
    resourceResponse->setResourceRepresentation(get_TemperatureResURIRepresentation(),
    m_TemperatureResURI_RESOURCE_INTERFACE);
    OCStackResult result = OCPlatform::notifyListOfObservers(m_TemperatureResURIResource,
                                                             m_TemperatureResURIObservers,
                                                             resourceResponse);
    if (result == OC_STACK_NO_OBSERVERS)
    {
        cout << "No more observers..Stopping observer loop..." << endl;
        m_TemperatureResURIObserverLoop->stop();
    }
}
 
/**
*  post method for /TemperatureResURI to assign the returned values to the member values
* @param requestRep the request representation.
* TODO: this function is also referenced when only get is implemented, something to fix..
*/
OCRepresentation IoTServer::post_TemperatureResURIRepresentation(OCRepresentation requestRep)
{
    OCEntityHandlerResult result = OC_EH_OK;  // default ok
    
    // only integer, float and string
    if (requestRep.hasAttribute(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_n))
    {
        try
        {
            cout << "IoTServer::post_TemperatureResURIRepresentation setting: m_TemperatureResURI_n" << endl;
        
        
            m_TemperatureResURI_n = requestRep.getValue<std::string>(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_n);
        }
        catch (...)
        {
            cerr << "Client sent invalid resource value type: " << m_TemperatureResURI_RESOURCE_PROPERTY_NAME_n<< endl;
            result = OC_EH_ERROR;
        }
    }
    if (requestRep.hasAttribute(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_temperature))
    {
        try
        {
            cout << "IoTServer::post_TemperatureResURIRepresentation setting: m_TemperatureResURI_temperature" << endl;
            m_TemperatureResURI_temperature = requestRep.getValue<float>(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_temperature);
        
        
        }
        catch (...)
        {
            cerr << "Client sent invalid resource value type: " << m_TemperatureResURI_RESOURCE_PROPERTY_NAME_temperature<< endl;
            result = OC_EH_ERROR;
        }
    }
    if (requestRep.hasAttribute(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_precision))
    {
        try
        {
            cout << "IoTServer::post_TemperatureResURIRepresentation setting: m_TemperatureResURI_precision" << endl;
            m_TemperatureResURI_precision = requestRep.getValue<float>(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_precision);
        
        
        }
        catch (...)
        {
            cerr << "Client sent invalid resource value type: " << m_TemperatureResURI_RESOURCE_PROPERTY_NAME_precision<< endl;
            result = OC_EH_ERROR;
        }
    }
    if (requestRep.hasAttribute(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_rt))
    {
        try
        {
            cout << "IoTServer::post_TemperatureResURIRepresentation setting: m_TemperatureResURI_rt" << endl;
        
        
        
        }
        catch (...)
        {
            cerr << "Client sent invalid resource value type: " << m_TemperatureResURI_RESOURCE_PROPERTY_NAME_rt<< endl;
            result = OC_EH_ERROR;
        }
    }
    if (requestRep.hasAttribute(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_step))
    {
        try
        {
            cout << "IoTServer::post_TemperatureResURIRepresentation setting: m_TemperatureResURI_step" << endl;
        
        
        
        }
        catch (...)
        {
            cerr << "Client sent invalid resource value type: " << m_TemperatureResURI_RESOURCE_PROPERTY_NAME_step<< endl;
            result = OC_EH_ERROR;
        }
    }
    if (requestRep.hasAttribute(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_range))
    {
        try
        {
            cout << "IoTServer::post_TemperatureResURIRepresentation setting: m_TemperatureResURI_range" << endl;
        
        
        
        }
        catch (...)
        {
            cerr << "Client sent invalid resource value type: " << m_TemperatureResURI_RESOURCE_PROPERTY_NAME_range<< endl;
            result = OC_EH_ERROR;
        }
    }
    if (requestRep.hasAttribute(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_id))
    {
        try
        {
            cout << "IoTServer::post_TemperatureResURIRepresentation setting: m_TemperatureResURI_id" << endl;
        
        
            m_TemperatureResURI_id = requestRep.getValue<std::string>(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_id);
        }
        catch (...)
        {
            cerr << "Client sent invalid resource value type: " << m_TemperatureResURI_RESOURCE_PROPERTY_NAME_id<< endl;
            result = OC_EH_ERROR;
        }
    }
    if (requestRep.hasAttribute(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_units))
    {
        try
        {
            cout << "IoTServer::post_TemperatureResURIRepresentation setting: m_TemperatureResURI_units" << endl;
        
        
        
        }
        catch (...)
        {
            cerr << "Client sent invalid resource value type: " << m_TemperatureResURI_RESOURCE_PROPERTY_NAME_units<< endl;
            result = OC_EH_ERROR;
        }
    }
    if (requestRep.hasAttribute(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_if))
    {
        try
        {
            cout << "IoTServer::post_TemperatureResURIRepresentation setting: m_TemperatureResURI_if" << endl;
        
        
        
        }
        catch (...)
        {
            cerr << "Client sent invalid resource value type: " << m_TemperatureResURI_RESOURCE_PROPERTY_NAME_if<< endl;
            result = OC_EH_ERROR;
        }
    }
    if (requestRep.hasAttribute(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_value))
    {
        try
        {
            cout << "IoTServer::post_TemperatureResURIRepresentation setting: m_TemperatureResURI_value" << endl;
        
        
        
        }
        catch (...)
        {
            cerr << "Client sent invalid resource value type: " << m_TemperatureResURI_RESOURCE_PROPERTY_NAME_value<< endl;
            result = OC_EH_ERROR;
        }
    }
    return result;
}
 
/**
*  get method for /TemperatureResURI to create an representation from the member values to respond to the call

*/
OCRepresentation IoTServer::get_TemperatureResURIRepresentation()
{
    OCRepresentation rep;
    
    // Add the attribute name and values in the representation (only integer, number and string)
 
    rep.setValue(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_n, m_TemperatureResURI_n ); 
    rep.setValue(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_temperature, m_TemperatureResURI_temperature ); 
    rep.setValue(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_precision, m_TemperatureResURI_precision );  
    rep.setValue(m_TemperatureResURI_RESOURCE_PROPERTY_NAME_id, m_TemperatureResURI_id ); 
       
    return rep  
}
   
 

/**
*  the entity handler for /TemperatureResURI
* @param Request the incomming request for this resource to handle
*/
OCEntityHandlerResult IoTServer::f_TemperatureResURIEntityHandler(shared_ptr<OCResourceRequest> Request)
{
    OCEntityHandlerResult result = OC_EH_ERROR;
    if (Request)
    {
        string requestType = Request->getRequestType();
        int requestFlag = Request->getRequestHandlerFlag();
        if (requestFlag & RequestHandlerFlag::RequestFlag)
        {
            auto Response = std::make_shared<OC::OCResourceResponse>();
            Response->setRequestHandle(Request->getRequestHandle());
            Response->setResourceHandle(Request->getResourceHandle());
 
            if (requestType == OC_REST_GET)
            {
                cout << "GET request for /TemperatureResURI reading" << endl;
                if (Response)
                {
                    Response->setResponseResult(OC_EH_OK);
                    Response->setResourceRepresentation(get_TemperatureResURIRepresentation());
                    if (OCPlatform::sendResponse(Response) == OC_STACK_OK)
                    {
                        result = OC_EH_OK;
                    }
                }
            }              
            else if (requestType == OC_REST_POST)
            {
                cout << "POST request for /TemperatureResURI" << endl;
                // post function sets the member variables correctly.
                result = Request->post_TemperatureResURIRepresentation(requestRep);
                if (result == OC_EH_OK)
                {
                    // TODO, we might need to return something..
                    //Response->setResourceRepresentation(get_TemperatureResURIRepresentation());
                    Response->setResponseResult(OC_EH_OK);
                    if (OCPlatform::sendResponse(Response) == OC_STACK_OK)
                    {
                        result = OC_EH_OK;
                    }
                }
                else
                {
                    Response->setResponseResult(OC_EH_ERROR);
                    OCPlatform::sendResponse(Response);
                    cerr << "Unsupported request type" << endl;
                    return result;
                }
            }   
            else
            {
                Response->setResponseResult(OC_EH_ERROR);
                OCPlatform::sendResponse(Response);
                cerr << "Unsupported request type" << endl;
                return result;
            }
        }
        if (requestFlag & RequestHandlerFlag::ObserverFlag)
        {
            ObservationInfo observationInfo = Request->getObservationInfo();
            if (ObserveAction::ObserveRegister == observationInfo.action)
            {
                cout << "Starting observer for /TemperatureResURI" << endl;
                m_TemperatureResURIObservers.push_back(observationInfo.obsId);
                m_TemperatureResURIObserverLoop->start();
            }
            else if (ObserveAction::ObserveUnregister == observationInfo.action)
            {
                m_temperatureObservers.erase(
                        remove(m_TemperatureResURIObservers.begin(), m_TemperatureResURIObservers.end(),
                               observationInfo.obsId),
                        m_TemperatureResURIObservers.end());
            }
        }
    }
    return result;
}
/**
*  DeletePlatformInfo
*  Deletes the allocated platform information
*/
void IoTServer::DeletePlatformInfo()
{
    delete[] m_platformInfo.platformID;
    delete[] m_platformInfo.manufacturerName;
    delete[] m_platformInfo.manufacturerUrl;
    delete[] m_platformInfo.modelNumber;
    delete[] m_platformInfo.dateOfManufacture;
    delete[] m_platformInfo.platformVersion;
    delete[] m_platformInfo.operatingSystemVersion;
    delete[] m_platformInfo.hardwareVersion;
    delete[] m_platformInfo.firmwareVersion;
    delete[] m_platformInfo.supportUrl;
    delete[] m_platformInfo.systemTime;
}

/**
*  SetPlatformInfo 
*  Sets the platform information ("oic/p"), from the globals

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
OCStackResult IoTServer::SetPlatformInfo(std::string platformID, std::string manufacturerName,
        std::string manufacturerUrl, std::string modelNumber, std::string dateOfManufacture,
        std::string platformVersion, std::string operatingSystemVersion,
        std::string hardwareVersion, std::string firmwareVersion, std::string supportUrl,
        std::string systemTime)
{
    DuplicateString(&m_platformInfo.platformID, platformID);
    DuplicateString(&m_platformInfo.manufacturerName, manufacturerName);
    DuplicateString(&m_platformInfo.manufacturerUrl, manufacturerUrl);
    DuplicateString(&m_platformInfo.modelNumber, modelNumber);
    DuplicateString(&m_platformInfo.dateOfManufacture, dateOfManufacture);
    DuplicateString(&m_platformInfo.platformVersion, platformVersion);
    DuplicateString(&m_platformInfo.operatingSystemVersion, operatingSystemVersion);
    DuplicateString(&m_platformInfo.hardwareVersion, hardwareVersion);
    DuplicateString(&m_platformInfo.firmwareVersion, firmwareVersion);
    DuplicateString(&m_platformInfo.supportUrl, supportUrl);
    DuplicateString(&m_platformInfo.systemTime, systemTime);

    return OC_STACK_OK;
}

/**
*  SetDeviceInfo
*  Sets the device information ("oic/d"), from the globals
*/
OCStackResult IoTServer::SetDeviceInfo()
{
    OCStackResult result = OC_STACK_ERROR;

    OCResourceHandle handle = OCGetResourceHandleAtUri(OC_RSRVD_DEVICE_URI);
    if (handle == NULL)
    {
        cout << "Failed to find resource " << OC_RSRVD_DEVICE_URI << endl;
        return result;
    }

    result = OCBindResourceTypeToResource(handle, gDeviceType.c_str());
    if (result != OC_STACK_OK)
    {
        cout << "Failed to add device type" << endl;
        return result;
    }

    result = OCPlatform::setPropertyValue(PAYLOAD_TYPE_DEVICE, OC_RSRVD_DEVICE_NAME, gDeviceName);
    if (result != OC_STACK_OK)
    {
        cout << "Failed to set device name" << endl;
        return result;
    }

    result = OCPlatform::setPropertyValue(PAYLOAD_TYPE_DEVICE, OC_RSRVD_DATA_MODEL_VERSION,
                                          gDataModelVersions);
    if (result != OC_STACK_OK)
    {
        cout << "Failed to set data model versions" << endl;
        return result;
    }

    result = OCPlatform::setPropertyValue(PAYLOAD_TYPE_DEVICE, OC_RSRVD_SPEC_VERSION, gSpecVersion);
    if (result != OC_STACK_OK)
    {
        cout << "Failed to set spec version" << endl;
        return result;
    }

    result = OCPlatform::setPropertyValue(PAYLOAD_TYPE_DEVICE, OC_RSRVD_PROTOCOL_INDEPENDENT_ID,
                                          gProtocolIndependentID);
    if (result != OC_STACK_OK)
    {
        cout << "Failed to set piid" << endl;
        return result;
    }

    return OC_STACK_OK;
}




// global needs static, otherwise it can be compiled out and then Ctrl-C does not work
static int quit = 0;
// handler for the signal to stop the application
void handle_signal(int signal)
{
    quit = 1;
}

// main application
// starts the server 
int main()
{
    struct sigaction sa;
    sigfillset(&sa.sa_mask);
    sa.sa_flags = 0;
    sa.sa_handler = handle_signal;
    sigaction(SIGINT, &sa, NULL);
    cout << "Press Ctrl-C to quit...." << endl;
    // create the server
    IoTServer server;
    do
    {
        usleep(2000000);
    }
    while (quit != 1);
    // delete the server
    delete IoTServer;
    
    return 0;
}
