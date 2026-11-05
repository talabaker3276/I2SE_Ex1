# Dataset definition

The assignment suggests an MRI NRRD volume downloadable through the 3D Slicer project, such as `MRHead_1.nrrd`. Place the real file alongside `Ex0.py` or use its absolute path. This repository does **not** contain `MRHead_1.nrrd`, so the example command requires downloading it separately. The former project notes mention dimensions `256×256×130`, but the file and its exact header have not been independently rechecked here; use the program's printed shape to confirm your own copy.

`planes.csv` provides **four** proposed plane definitions: three isosceles triangles and one isosceles trapezoid. It is an example set in voxel-index coordinates, not proof of clinical image quality. For validation, use a small synthetic constant/coordinate-coded NRRD and a real MRI NRRD. A 500×500×500 representative volume and enough planes should be used for the required FPS experiment. Document provenance, dimensions, numeric data type and SHA256 checksum of each real tested input.

MRI data must be checked for usage restrictions before public redistribution; do not commit unrelated patient data.
