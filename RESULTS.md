# Experiment and Results

## Experiment
The program was tested using the `MRHead_1.nrrd` MRI volume.

The `planes.csv` file contained three different planes, each defined by three 3D points.

The program was executed using:

python Ex0.py MRHead_1.nrrd planes.csv result.mp4

## Results
The NRRD volume was loaded successfully.

All three planes were validated and a 2D projection was generated for each plane.

The generated projections were combined into an MP4 video in the same order as the planes in the CSV file.

The output video `result.mp4` was created and opened successfully.

## Conclusion
The experiment demonstrates that the program can read volumetric NRRD data, process multiple plane definitions, generate their 2D projections, and create the required MP4 output.
