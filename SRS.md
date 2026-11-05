# Software Requirements Specification (SRS)

## Purpose and scope

The application converts specified triangular/trapezoidal cross-sections of a 3D NRRD integer volume into a sequence of MP4 frames. It is a sampling program rather than a 3D display or medical analysis tool.

## Functional requirements

| ID | Requirement | Acceptance check |
|---|---|---|
| FR-01 | CLI accepts `python Ex0.py file.nrrd file.csv file.mp4` | Valid invocation produces output; missing arguments show usage |
| FR-02 | Read 3D integer NRRD data, dimensions 1–1023 per axis | Valid sample loads; invalid dimensions/data types fail clearly |
| FR-03 | Parse every nonblank CSV row as 9 (triangle) or 12 (trapezoid) finite numbers | Malformed inputs fail with line number |
| FR-04 | Validate triangle: `abs(dist(a,b)-dist(a,c)) < 0.001`, nonzero side/base | Reject unequal or degenerate sides |
| FR-05 | Validate trapezoid: equal-length `a1->b` and `a2->c` (EPS=0.001), top width <= bottom width, and coplanarity | Reject violated geometry |
| FR-06 | Sample nearest voxel on each horizontal row of the plane; out-of-volume => 0 | Compare with synthetic data and boundary tests |
| FR-07 | Preserve CSV order in output video, exactly one frame per nonblank row | Check frame count and frame ordering |
| FR-08 | MP4 contains consistent, even-size grayscale RGB images (canvas padding is black) | Decode video and inspect dimensions |

## Nonfunctional requirements

- **Correctness:** deterministic projections from valid inputs, finite-coordinate validation and clear errors.
- **Runtime:** assignment target is >=30 FPS and expected >=100 FPS for 500³ input. A benchmark must measure projection time and document environment, workload and actual measurements; it is not automatically guaranteed.
- **Reliability:** avoid partially replacing an existing video on input-validation failure (all plane computations precede encoding).
- **Maintainability:** standalone geometry/parser/projection functions, source-controlled changes, reproducible test plan.

## Assumptions and limitations

Voxel positions are interpreted in index order `(x,y,z)` and rounded to nearest integer. Input data is not resampled using NRRD spatial directions. Each plane has potentially different native image dimensions: for the MP4, smaller planes are centered on a black canvas with a uniform even width and height. Each frame is independently contrast-scaled for visual output; raw sampled matrix values are not changed. H.264/FFmpeg must be available.
