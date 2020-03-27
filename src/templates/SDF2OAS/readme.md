# template: SDF2OAS

Converts SDF files to OAS2.0 files.

input options to use:

    -swagger <filename>, the input SDF file
    -template SDF2OAS, the template to convert SDF to OAS2.0
    -out_dir <foldername>, the folder for the output_file
    -jsonindent <number>, nice format JSON with indent = 2
    -output_file <myfilename>, the output filename, should end with .swagger.json

# Handling of rt
The conversion template checks on the copyright. 
If the copy right contains OCF then the rt is  
- rt values are created as oic.r.XXXX  
otherwise the 
- rt values are created as x.unknown.XXXX  
where XXXX is the odmObject name.

# Fixed parameters
- if parameter block
  this is fixed in the template, e.g. all OAS files will have the same set of interfaces