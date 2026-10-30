# I2SE_Ex1 - 3D Volume Plane Projection

## Project Description
This project is part of the Introduction to Software Engineering course.

The goal of the project is to design and implement an efficient algorithm
for generating 2D plane projections from 3D volumetric data stored in NRRD format.

## Problem
Given a 3D raster data matrix and a plane defined by 3 or 4 points,
the program computes a 2D image representing the projection of
that plane within the 3D volume.

The implementation supports:
- 3-point planes forming an isosceles triangle.
- 4-point planes forming an isosceles trapezoid.

## Project Scope
The project:
- Reads 3D volumetric data from an NRRD file.
- Reads plane coordinates from a CSV file.
- Validates 3-point and 4-point plane definitions.
- Generates a 2D projection for each plane.
- Creates an MP4 video containing the generated projections as frames.
- Tests correctness, stability, and runtime performance.

## Usage

Run the program using:

python Ex0.py file.nrrd file.csv file.mp4

Example:

python Ex0.py MRHead_1.nrrd planes.csv result.mp4

## Performance
The implementation was tested using four plane projections.

The measured performance was approximately 72.59 FPS,
which satisfies the required minimum performance of 30 FPS.

## Output
The program generates an MP4 file containing one frame for each plane
defined in the CSV file, in the same order as the input planes.
