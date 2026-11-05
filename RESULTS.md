# Experiment and Results (verified run: 2026-11-05)

## Input and command
- Input: `MRHead_1.nrrd`, 3D MRI, shape **256 × 256 × 130**, signed 16-bit integers.
- Input SHA256: `e9b54e8855e9024f2238e27224702c1dcb49c64407d937499a3cc42fb1114c8b`.
- CSV: four planes, in order: three isosceles triangles and one four-point trapezoid.
- Command: `python Ex0.py MRHead_1.nrrd planes.csv result.mp4`.
- The run used a temporary minimal NRRD reader compatible with this file's gzip-compressed little-endian short data because `pynrrd` was unavailable in the execution environment. The submitted script imports `pynrrd` as documented in `requirements.txt`.

## Observed results
- All four planes were processed without an error.
- Output projection shapes: `(101, 142)`, `(101, 142)`, `(101, 142)`, `(103, 61)`.
- The output `result.mp4` was created and independently decoded: **4 frames**, encoded canvas **142 × 104**.
- Measured projection-only elapsed time: **0.038601 seconds** for four planes, equivalent to **103.63 projection FPS** in this single run.
- End-to-end runtime (reading, projecting, and encoding): **0.723025 seconds**.

## Limits of the result
- These measurements apply to this **256 × 256 × 130** volume and four sample planes on the execution environment used, **not** the required `500³` benchmark.
- The assignment's **>=30 FPS on a 500³ volume** has **not** been verified. Four samples are not a robust performance benchmark.
- Visual review against 3D Slicer reference slices has not been performed. This is a successful functional smoke test, not proof of full correctness.
- The previous `72.59 FPS` claim was unsupported and has been removed.
