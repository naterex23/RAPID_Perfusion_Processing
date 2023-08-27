# RAPID_Perfusion_Processing

The purpose of this repository is to host code associated with the processing of RAPID perfusion images associated with the ESCAPE-NA1 Database.

The original ESCAPE-NA1 publication can be found at: https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)30258-0/fulltext 

All code should be executable with functions included in standard python libraries without modification.

A link to any associated publications will be added when available. 

Note that this code takes generic RAPID output files (in their raw ".dcm" form), similar to below: 

![image (4)](https://user-images.githubusercontent.com/58052594/214413819-c18dd66a-513e-427d-9583-19c48c817cb6.png)

And converts each to 2 nifti (".nii"/".nii.gz") files types, including one "lesion mask" file and one "brain extracted" (or, perhaps more accurately, "text removed") file. Each lesion mask contains multiple thresholds to a segmentation that can be analyzed using a variety of medical imaging software packages. Notably, I used 3D Slicer (http://slicer.org). 

If you use this code for your work, please consider citing the following publication:


CT Perfusion Does Not Modify the Effect of Reperfusion in Patients with Acute Ischemic Stroke Undergoing Endovascular Treatment in the ESCAPE-NA1 Trial
N.B. Rex, R.V. McDonough, J.M. Ospel, N. Kashani, A. Sehgal, J.C. Fladt, R.A. McTaggart, R. Nogueira, B. Menon, A.M. Demchuk, M. Tymianski, M.D. Hill, M. Goyal
American Journal of Neuroradiology Aug 2023, DOI: 10.3174/ajnr.A7954

https://www.ajnr.org/content/early/2023/08/24/ajnr.A7954

If you have any questions, comments, or inquiries regarding access to source code feel free to comment or email me at nathaniel(underscore)rex(at)brown.edu 
