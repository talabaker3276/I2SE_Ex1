# Experiment and Results

## Experiment
The program was tested using the `MRHead_1.nrrd` MRI volume.

The `planes.csv` file contained four different planes:
- Three planes defined by 3 points (triangles).
- One plane defined by 4 points (isosceles trapezoid).

The program was executed using:

python Ex0.py MRHead_1.nrrd planes.csv result.mp4

## Results
The NRRD volume was loaded successfully.

All four planes were validated successfully and a 2D projection was generated for each plane.

The program successfully processed both 3-point and 4-point plane definitions.

The four projections were combined into an MP4 video in the same order as the planes in the CSV file.

The output video `result.mp4` was created successfully.

## Performance
The processing time for the four projections was approximately 0.055 seconds.

The measured performance was approximately 72.59 FPS.

Therefore, the implementation successfully passed the required performance of at least 30 FPS.

## Conclusion
The experiment demonstrates that the program can read volumetric NRRD data, process 3-point triangular planes and 4-point trapezoidal planes, generate their 2D projections, and create the required MP4 output while meeting the performance requirement.
