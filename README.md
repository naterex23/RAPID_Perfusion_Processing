# RAPID_Perfusion_Processing

The purpose of this repository is to house the code associated with the processing of RAPID perfusion images associated with the ESCAPE-NA1 Database. 

All code should be executable with functions included in standard python libraries without modification.

A link to the publication will be added when appropriate. 

Note that this code takes generic RAPID output files (in their raw ".dcm" form), similar to below: 

![image (4)](https://user-images.githubusercontent.com/58052594/214413819-c18dd66a-513e-427d-9583-19c48c817cb6.png)

And converts each to 2 nifti (".nii"/".nii.gz") files types, including one "lesion mask" file and one "brain extracted" file. Each lesion mask contains multiple thresholds to a segmentation that can be analyzed using a variety of medical imaging software. Notably, I used 3D Slicer (http://slicer.org). 

If you have any questions, comments, or inquiries regarding access to source code feel free to comment or email me at nathaniel(underscore)rex(at)brown.edu 
