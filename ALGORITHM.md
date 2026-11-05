# Main algorithm and detailed design

## Inputs and plane constraints

`M` is a 3D integer NRRD array indexed `M[x,y,z]`. Each CSV row is either `(a,b,c)` (9 values) or `(a1,a2,b,c)` (12 values). The triangle needs equal sides `|a-b|` and `|a-c|` (difference `< 0.001`). The trapezoid needs equal sweep sides `|a1-b|` and `|a2-c|` (`< 0.001`), a shorter-or-equal top edge `|a1-a2| <= |b-c|`, and four coplanar points (point-to-plane distance `< 0.001`). Zero-length/degenerate geometry is rejected.

## Sampling design

1. For triangles, set start endpoints `L0=R0=a` and end endpoints `L1=b, R1=c`. For trapezoids, set `L0=a1, R0=a2, L1=b, R1=c`.
2. Let `D` be the equal sweep-side length and `W` be the bottom edge length (`|b-c|`). Allocate `E` with `round(D)+1` rows and `round(W)+1` columns, initialized to zero. Rounded integer dimensions include both endpoints.
3. For each image row `y=0..round(D)`, interpolate `t=y/round(D)`; calculate current endpoints `L=(1-t)L0+tL1` and `R=(1-t)R0+tR1`. This avoids accumulated floating-point drift.
4. Let `d=|L-R|`, sample `n=round(d)+1` positions along the segment (for a collapsed apex use 1 sample). Center the shorter row horizontally in the full width; rounded column coordinates are clamped by output bounds.
5. For each sampled point `q`, take integer voxel coordinate `rint(q)` (nearest neighbor). If all 3 indices lie inside M, assign `E[y,x]=M[ix,iy,iz]`; otherwise keep `E[y,x]=0`.
6. Return `E`. Repeat for all CSV rows in order.
7. For video: linearly map each image's min/max to 0..255 for display, create a common even-sized black canvas, center each image, convert to RGB, and encode one MP4 frame per plane (1 playback frame/second).

This implements the provided exercise's two moving sides, centered scanlines and zero outside M. Exact rounding, row indexing `[y,x]`, endpoint inclusion, and MP4 image sizing are explicit design choices where the exercise pseudocode leaves implementation details unspecified. The code uses NumPy vectorized voxel lookups per scanline, but loops over rows.

## Complexity

For a plane with H rows and at most W columns, sampling takes O(HW) time and O(HW) space for the output. The per-frame video canvas can require additional O(maxH*maxW) memory. Loading the 3D volume requires O(sx*sy*sz) memory. Runtime depends on output dimensions, memory bandwidth and video encoding.

## Edge cases

Malformed CSV, non-finite coordinates, zero-length sides, non-isosceles geometry, non-coplanar trapezoids and wrong NRRD dimensions/types produce errors. Samples outside the volume are zero. No interpolation between voxels is performed. Physical-space NRRD orientation is not applied; all positions are voxel indices.
