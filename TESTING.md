# Testing strategy

Tests should record **input, expected outcome, actual outcome, runtime, and pass/fail**, rather than declaring success without executing the code.

| ID | Test | Expected result |
|---|---|---|
| T01 | Synthetic 3D integer NRRD with known voxel values | Plane samples equal expected voxel values |
| T02 | Triangle with `dist(a,b)=dist(a,c)` | Accepted and projected |
| T03 | Unequal triangle sides | Clear `ValueError` |
| T04 | Four coplanar points with equal sweep-side lengths, top<=bottom | Accepted and projected |
| T05 | Noncoplanar or unequal trapezoid sides | Rejected |
| T06 | Plane partially outside 3D array | Outside positions are zero |
| T07 | CSV row with 8/10/11 values, malformed number or NaN | Rejected with line number |
| T08 | Three triangles + one trapezoid from `planes.csv` | Exactly 4 ordered output frames |
| T09 | Different projection dimensions | Output has fixed even dimensions and decodes properly |
| T10 | Real NRRD/MRI and example CLI | NRRD read + MP4 output + logged dimensions |
| T11 | Many planes against a 500³ byte NRRD | Record projection FPS; check >=30 and compare with 100 expected |

## Commands

```bash
python -m pip install -r requirements.txt
python Ex0.py MRHead_1.nrrd planes.csv result.mp4
python -m unittest discover -s tests -v
```

Projection FPS is `number_of_planes / elapsed_projection_seconds`. Measure video encoding and loading separately. Use repeated geometries (e.g. >=100) and an adequately sized volume for stable performance estimates. Only report a test as passed after actually running it.
