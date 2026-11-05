# I2SE Ex1 — 3D volume plane projection

Introduction to Software Engineering, Ariel University. This program samples a triangular or trapezoidal plane through a 3D NRRD raster and produces one MP4 frame per plane in CSV order.

## Problem and scope

Input is a 3D integer voxel matrix `M[x,y,z]`, with each dimension from 1 to 1023, and a list of 3-point isosceles triangles or 4-point isosceles trapezoids. The output is an MP4 video of 2D sampled slices, not an accumulation/ray-cast projection. Voxel coordinates are used, not physical millimeters; nearest-neighbor lookup is used, and out-of-bounds samples become zero. The sampling/design choices and assumptions appear in [ALGORITHM.md](ALGORITHM.md).

The work includes input validation, CSV parsing, plane sampling and video output. It does not include an interactive 3D viewer or medical interpretation. The MRI volume must be supplied separately; `MRHead_1.nrrd` is not tracked in this repository.

## Install and run

Python 3.10+ and an FFmpeg-capable environment are recommended.

```bash
python -m pip install -r requirements.txt
python Ex0.py MRHead_1.nrrd planes.csv result.mp4
```

The exact required CLI is `python Ex0.py file.nrrd file.csv file.mp4`. Each CSV row contains 9 comma-separated coordinates for `a,b,c` or 12 for `a1,a2,b,c`, flattened as `x,y,z` triples, no header. The 4-point ordering matters. An example appears in [planes.csv](planes.csv). Every plane must pass geometry validation; invalid input gives an error and no new video.

## Documentation

- [SRS.md](SRS.md) — requirements and acceptance criteria
- [ALGORITHM.md](ALGORITHM.md) — detailed design and sampling choices
- [DATASET.md](DATASET.md) — dataset provenance and limits
- [TESTING.md](TESTING.md) — reproducible tests
- [RESULTS.md](RESULTS.md) — experimental status, methodology and unverified historical claims

## Performance

The exercise asks for at least 30 FPS and expects 100 FPS on a 500×500×500 volume. This project reports *projection throughput* separately from file loading and video encoding. No verified benchmark at 500³ is included yet; do not interpret results on a small MRI or four frames as proof that the requirement is met. Execute the program and document actual machine, volume, number of planes and runtime in RESULTS.md.
