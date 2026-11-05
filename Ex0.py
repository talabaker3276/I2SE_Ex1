"""I2SE Ex1: sample triangular or trapezoidal planes from a 3-D NRRD volume."""
import argparse
import csv
import time
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
import nrrd

EPS = 0.001


def _dist(a, b):
    return float(np.linalg.norm(b - a))


def read_planes(filename):
    planes = []
    with open(filename, newline="", encoding="utf-8-sig") as stream:
        for line_number, row in enumerate(csv.reader(stream), 1):
            if not row or all(not cell.strip() for cell in row):
                continue
            if len(row) not in (9, 12):
                raise ValueError(f"CSV line {line_number}: expected 9 or 12 numbers, got {len(row)}")
            try:
                values = np.asarray([float(cell) for cell in row], dtype=np.float64)
            except ValueError as exc:
                raise ValueError(f"CSV line {line_number}: invalid coordinate") from exc
            if not np.all(np.isfinite(values)):
                raise ValueError(f"CSV line {line_number}: coordinates must be finite")
            planes.append(values.reshape((-1, 3)))
    if not planes:
        raise ValueError("CSV contains no planes")
    return planes


def _geometry(points):
    """Return the two equal-length sweep sides (starts, ends) and output width.

    Triangles: a->b and a->c. Trapezoids: a1->b and a2->c.
    Coordinates are voxel indices (x,y,z), not physical world coordinates.
    """
    if points.shape == (3, 3):
        a, b, c = points
        starts = np.stack((a, a))
        ends = np.stack((b, c))
        width = _dist(b, c)
    elif points.shape == (4, 3):
        a1, a2, b, c = points
        starts = np.stack((a1, a2))
        ends = np.stack((b, c))
        top = _dist(a1, a2)
        bottom = _dist(b, c)
        if top > bottom + EPS:
            raise ValueError("Trapezoid requires dist(a1,a2) <= dist(b,c)")
        # Four points are coplanar when the scalar triple product vanishes.
        normal = np.cross(a2 - a1, b - a1)
        norm = float(np.linalg.norm(normal))
        if norm < 1e-12:
            # Degenerate cases cannot reliably specify a plane.
            raise ValueError("Degenerate four-point plane")
        point_to_plane_distance = abs(float(np.dot(c - a1, normal))) / norm
        if point_to_plane_distance >= EPS:
            raise ValueError("Four points are not coplanar")
        width = bottom
    else:
        raise ValueError("Expected three or four 3-D points")

    side_lengths = np.linalg.norm(ends - starts, axis=1)
    if min(side_lengths) < 1e-12:
        raise ValueError("Plane sides must have positive length")
    if abs(side_lengths[0] - side_lengths[1]) >= EPS:
        raise ValueError("Sweep sides must have equal lengths within EPS=0.001")
    if width < 1e-12:
        raise ValueError("Plane must have nonzero width")
    return starts, ends, float(side_lengths[0]), width


def create_projection(data, points):
    """Nearest-neighbour voxel sampling with zero values outside the volume.

    Output is indexed [y,x]. Each sweep row is centered horizontally, as in
    the exercise pseudocode. Dimensions are rounded to voxel-sized pixels.
    """
    starts, ends, length, width = _geometry(np.asarray(points, dtype=np.float64))
    height_px = max(1, int(round(length)) + 1)
    width_px = max(1, int(round(width)) + 1)
    image = np.zeros((height_px, width_px), dtype=data.dtype)
    for y in range(height_px):
        fraction = y / (height_px - 1) if height_px > 1 else 0.0
        left = starts[0] + fraction * (ends[0] - starts[0])
        right = starts[1] + fraction * (ends[1] - starts[1])
        segment = _dist(left, right)
        # Sample in one-voxel steps, always including both endpoints.
        n = max(1, int(round(segment)) + 1)
        fractions = np.linspace(0.0, 1.0, n)
        xyz = left[None, :] + fractions[:, None] * (right - left)[None, :]
        ijk = np.rint(xyz).astype(np.int64)
        xs = np.rint((width_px - 1 - (n - 1)) / 2.0 + np.arange(n)).astype(int)
        valid = (np.all((ijk >= 0) & (ijk < np.asarray(data.shape)), axis=1)
                 & (xs >= 0) & (xs < width_px))
        if np.any(valid):
            p = ijk[valid]
            image[y, xs[valid]] = data[p[:, 0], p[:, 1], p[:, 2]]
    return image


def to_rgb(image, out_height, out_width):
    """Normalize only for display; projection values are unchanged."""
    a = image.astype(np.float64)
    lo, hi = float(a.min()), float(a.max())
    if hi > lo:
        a = np.rint((a - lo) * (255.0 / (hi - lo)))
    else:
        a = np.zeros_like(a)
    gray = a.astype(np.uint8)
    # H.264 requires consistent even dimensions; center on a black canvas.
    canvas = np.zeros((out_height, out_width), dtype=np.uint8)
    y0 = (out_height - gray.shape[0]) // 2
    x0 = (out_width - gray.shape[1]) // 2
    canvas[y0:y0 + gray.shape[0], x0:x0 + gray.shape[1]] = gray
    return np.repeat(canvas[:, :, None], 3, axis=2)


def run(volume_file, csv_file, output_file):
    started = time.perf_counter()
    data, _ = nrrd.read(str(volume_file), index_order="F")
    if data.ndim != 3 or not np.issubdtype(data.dtype, np.integer):
        raise ValueError("NRRD must contain a 3-D integer volume")
    if not all(1 <= n < 1024 for n in data.shape):
        raise ValueError("NRRD dimensions must be between 1 and 1023")
    planes = read_planes(csv_file)
    frames = []
    projection_start = time.perf_counter()
    for i, plane in enumerate(planes, 1):
        result = create_projection(data, plane)
        frames.append(result)
        print(f"Plane {i}/{len(planes)}: {plane.shape[0]} points, image {result.shape}")
    projection_seconds = time.perf_counter() - projection_start
    h = max(frame.shape[0] for frame in frames)
    w = max(frame.shape[1] for frame in frames)
    h += h % 2
    w += w % 2
    with imageio.get_writer(str(output_file), fps=1, codec="libx264", macro_block_size=1) as writer:
        for frame in frames:
            writer.append_data(to_rgb(frame, h, w))
    elapsed = time.perf_counter() - started
    print(f"Loaded NRRD: shape={data.shape}, dtype={data.dtype}")
    print(f"Frames written: {len(frames)} -> {output_file}")
    print(f"Projection time: {projection_seconds:.6f} s; projection FPS: {len(frames)/projection_seconds:.2f}")
    print(f"Total runtime (I/O and video included): {elapsed:.6f} s")
    print("NOTE: compare FPS to assignment target only on a 500^3 volume with sufficient repeated planes.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("nrrd_file")
    parser.add_argument("csv_file")
    parser.add_argument("mp4_file")
    args = parser.parse_args()
    try:
        run(args.nrrd_file, args.csv_file, args.mp4_file)
    except (ValueError, OSError, nrrd.NRRDError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
