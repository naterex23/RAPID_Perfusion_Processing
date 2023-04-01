# RAPID_Perfusion_Processing

The purpose of this repository is to host code associated with the processing of RAPID perfusion images associated with the ESCAPE-NA1 Database.

The original ESCAPE-NA1 publication can be found at: https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)30258-0/fulltext 

All code should be executable with functions included in standard python libraries without modification.

A link to any associated publications will be added when available. 

Note that this code takes generic RAPID output files (in their raw ".dcm" form), similar to below: 

![image (4)](https://user-images.githubusercontent.com/58052594/214413819-c18dd66a-513e-427d-9583-19c48c817cb6.png)

And converts each to 2 nifti (".nii"/".nii.gz") files types, including one "lesion mask" file and one "brain extracted" (or, perhaps more accurately, "text removed") file. Each lesion mask contains multiple thresholds to a segmentation that can be analyzed using a variety of medical imaging software packages. Notably, I used 3D Slicer (http://slicer.org). 

If you have any questions, comments, or inquiries regarding access to source code feel free to comment or email me at nathaniel(underscore)rex(at)brown.edu 
