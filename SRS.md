# Software Requirements Specification (SRS)

## 1. Introduction

### 1.1 Purpose
The purpose of this project is to design and implement a program that generates 2D plane projections from 3D volumetric data stored in NRRD format.

### 1.2 Scope
The program will read 3D volumetric data from an NRRD file and plane coordinates from a CSV file. For each plane, the program will generate a 2D projection. The generated projections will be combined into an MP4 video.


## 2. Functional Requirements

### 2.1 Input
The program shall accept:
- An NRRD file containing 3D volumetric data.
- A CSV file containing a list of plane coordinates defined by 3 or 4 points.

### 2.2 Processing
The program shall:
- Read the 3D data from the NRRD file.
- Read the plane coordinates from the CSV file.
- Compute a 2D projection for each plane.

### 2.3 Output
The program shall generate an MP4 video containing one frame for each plane, in the same order as the planes appear in the CSV file.


## 3. Non-Functional Requirements

### 3.1 Performance
The implementation should be runtime-efficient. For a 3D matrix of size 500x500x500, a performance of at least 30 FPS is required, while 100 FPS or more is expected.

### 3.2 Correctness and Stability
The program should be correct and stable when processing valid input files.


## 4. Plane Requirements

### 4.1 Plane Defined by 3 Points
A plane may be represented by three points (a, b, c), where:

|dist(a,b) - dist(a,c)| < EPS

where EPS = 0.001.

### 4.2 Plane Defined by 4 Points
A plane may also be represented by four points (a1, a2, b, c), where:

- |dist(a1,b) - dist(a2,c)| < EPS
- dist(a1,a2) <= dist(b,c)
- The vectors a1→b and a2→c are on the same plane.


## 5. Testing Requirements

The project should include a testing strategy to verify:
- Correct reading of NRRD files.
- Correct reading of plane coordinates from CSV files.
- Correct generation of 2D projections.
- Correct generation of the MP4 output file.
- Runtime performance of the implementation.


## 6. Demo

The program should support execution in the following format:

python Ex0.py file.nrrd file.csv file.mp4
