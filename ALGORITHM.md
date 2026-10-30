# Main Algorithm

## 1. Input
The algorithm receives:
- A 3D raster matrix M.
- Three points (a, b, c) defining the plane.

## 2. Output
The algorithm generates a 2D matrix E representing the plane projection.

## 3. Algorithm Steps

1. Calculate the distances:
   - Dab = dist(a, b) = dist(a, c)
   - Dbc = dist(b, c)

2. Calculate the normalized direction vectors:
   - v(a,b) = vector(a,b) / Dab
   - v(a,c) = vector(a,c) / Dab

3. Create the output matrix E with size Dab × Dbc.

4. Initialize:
   - a1 = a
   - a2 = a

5. Move a1 toward b and a2 toward c.

6. For each step:
   - Calculate the distance between a1 and a2.
   - Move from a1 toward a2.
   - Read the corresponding value from the 3D matrix M.
   - If the point is outside M, use the value 0.
   - Store the value in the corresponding position in E.

7. Return E.

## 4. Four-Point Plane

The algorithm also supports a plane defined by four points (a1, a2, b, c), forming an isosceles trapezoid.

The following conditions must be satisfied:
- |dist(a1,b) - dist(a2,c)| < EPS
- dist(a1,a2) <= dist(b,c)
- The vectors a1→b and a2→c are on the same plane.

The projection is generated using the same approach as the three-point case:
1. Move along the two sides of the trapezoid.
2. For each step, sample the points between the two sides.
3. Read the corresponding values from the 3D matrix M.
4. Store the sampled values in the 2D output matrix E.
