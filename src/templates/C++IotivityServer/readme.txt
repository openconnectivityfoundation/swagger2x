Template: IOTivity C++ server

The generated code acts as an simulator:
- it creates values at start update
- handles incomming requests, 
    - stores the values on POST
    - respond on GET by giving out the stored values

what is generated:
        
- server.cpp implementation code
    - per resource an class is generated.
        - constructor
            - creates the resource
            - has entity handler
            - get function to use the variables to create the return payload
            - post function to assign the variables from the request payload

what is not checked:            
- security
- introspection
            
what is missing/incorrect:
- handling query params and interfaces
- handling observe
- only double, int and boolean properties are used and stored.
- creation/deletion of resources (PUT/DELETE functions)
- no correct makefile/scons file, so we do not yet know how to insert this in the IOTivity tree and then compile

notes:
- only tested on windows

## SCONS adaption in resource/examples

######################################################################
# Source files and Targets
######################################################################
example_names = [
    'simpleserver', 'simpleclient', 'server',
    'simpleclientserver',
    'directpairingclient',
    'devicediscoveryserver', 'devicediscoveryclient',
    'simpleserverHQ', 'simpleclientHQ',
    ]

if target_os not in ['windows', 'msys_nt']:
    example_names += [
        'fridgeserver', 'fridgeclient',
        'presenceserver', 'presenceclient',
        'roomserver', 'roomclient',
        'garageserver',
        'garageclient',
        'groupserver',
        'groupclient',
        'lightserver',
        'threadingsample',
        'server',
        'observer',
        ]
    if 'CLIENT' in examples_env.get('RD_MODE'):
        examples_env.AppendUnique(CPPPATH = ['../csdk/resource-directory/include'])
        examples_env.AppendUnique(LIBS = ['resource_directory'])
        example_names += ['rdclient']

examples = map(make_single_file_cpp_program, example_names)


## WINDOWS run.bat changes:

REM *** BUILD OPTIONS ***

if "!RUN_ARG!"=="server" (
  cd %BUILD_DIR%\resource\examples
  REM %DEBUG% simpleserver.exe
  %DEBUG% server.exe
) else if "!RUN_ARG!"=="client" (
