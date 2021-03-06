# Template: SDF2AsyncAPI

Converts SDF files to AsyncAPI2.0 files.

## Usage

input options to use:

    -swagger <filename>, the input SDF file
    -template SDF2AsyncAPI, the template to convert SDF to AsyncAPI 2.0.0
    -out_dir <foldername>, the folder for the output_file
    -jsonindent <number>, nice format JSON with indent = 2
    -output_file <myfilename>, the output filename, should end with .async.json

## what is generated

- channel with the sdfObject name

### templates

- publisher.ascyncapi.json
  - template to generate a publisher
  - using component/schema nodes for declaration of the message payloads
- subscriber.ascyncapi.json
  - template to generate a subscriber
  - using inline declaration of the message payloads
- pubsub.ascyncapi.json
  - template for a publisher and subscriber
  - using component/schema nodes for declaration of the message payloads

### what needs to be changed in the generated output

- stub server information

## AsyncAPI info

website: https://www.asyncapi.com/

## AsyncAPI verification

The verification of the output file is achieved by spectral lint.
spectral lint is capable of verifying AsyncAPI files.

https://github.com/stoplightio/spectral
