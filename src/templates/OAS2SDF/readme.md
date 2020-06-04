# template: OAS2SDF

Converts OAS2.0 (swagger) files to SDF files.

input options to use:

    -swagger <filename>, the input SDF file
    -template OAS2SDF, the template to convert SDF to OAS2.0
    -out_dir <foldername>, the folder for the output_file
    -jsonindent <number>, nice format JSON with indent = 2
    -output_file <myfilename>, the output filename, should end with .swagger.json

# Handling of SDF features
- auto renaming function of the file.
    - remove . (dot) and replace it with _ in the filename 
- rt value being used for the object name (e.g. stripping oic.r from the name)
- keep the . in the rt value for the object name
- conversion of readOnly into writable indication