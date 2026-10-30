# Testing Strategy

## 1. NRRD Input Test
Verify that the program can successfully read the `MRHead_1.nrrd` file and load the 3D volumetric data.

## 2. CSV Input Test
Verify that the program can correctly read plane coordinates from a CSV file for planes defined by 3 or 4 points.

## 3. Projection Test
Verify that the algorithm generates a valid 2D projection for each plane defined in the CSV file.

## 4. Boundary Test
Test planes that contain points outside the boundaries of the 3D matrix. Points outside the volume should receive the value 0.

## 5. MP4 Output Test
Verify that the program creates an MP4 file containing one frame for each plane in the CSV file, in the same order.

## 6. Performance Test
Measure the runtime performance of the projection algorithm and verify that it satisfies the required performance of at least 30 FPS.

In the experiment with four planes, the measured performance was approximately 72.59 FPS, so the performance requirement was satisfied.

## 7. Demo Test
Test the complete program using the required command:

python Ex0.py file.nrrd file.csv file.mp4

Verify that valid NRRD and CSV input files produce the expected MP4 output file.
