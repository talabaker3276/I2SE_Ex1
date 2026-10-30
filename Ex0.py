import sys
import nrrd
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio


# --------------------------------------------------
# Create a 2D projection from one 3-point plane
# --------------------------------------------------
def create_projection(data, a, b, c):

    # Calculate distances
    dist_ab = np.linalg.norm(b - a)
    dist_ac = np.linalg.norm(c - a)

    # Validate plane
    EPS = 0.001

    if abs(dist_ab - dist_ac) >= EPS:
        raise ValueError("Invalid plane")

    # Normalized vectors
    v_ab = (b - a) / dist_ab
    v_ac = (c - a) / dist_ac

    # Output image dimensions
    height = int(round(dist_ab))
    width = int(round(np.linalg.norm(c - b)))

    E = np.zeros((height + 1, width + 1), dtype=data.dtype)

    a1 = a.copy()
    a2 = a.copy()

    # Move from point a toward b and c
    for y in range(height + 1):

        if y > 0:
            a1 = a1 + v_ab
            a2 = a2 + v_ac

        d12 = np.linalg.norm(a2 - a1)

        if d12 == 0:
            p = a1.copy()
            points_in_row = 1
            dp = np.zeros(3)

        else:
            p = a1.copy()
            points_in_row = int(round(d12)) + 1
            dp = (a2 - a1) / d12

        # Sample points between a1 and a2
        for x1 in range(points_in_row):

            voxel = np.rint(p).astype(int)

            vx, vy, vz = voxel

            # Check if the voxel is inside the volume
            if (
                    0 <= vx < data.shape[0]
                    and 0 <= vy < data.shape[1]
                    and 0 <= vz < data.shape[2]
            ):
                value = data[vx, vy, vz]

            else:
                value = 0

            # Center the row in the output image
            x = int(round((width / 2) - (d12 / 2) + x1))

            if 0 <= x < E.shape[1]:
                E[y, x] = value

            p = p + dp

    return E


# --------------------------------------------------
# Check command line arguments
# --------------------------------------------------
if len(sys.argv) != 4:
    print("Usage: python Ex0.py file.nrrd file.csv file.mp4")
    sys.exit(1)


# --------------------------------------------------
# Input files
# --------------------------------------------------
nrrd_file = sys.argv[1]
csv_file = sys.argv[2]
output_file = sys.argv[3]


# --------------------------------------------------
# Read NRRD volume
# --------------------------------------------------
data, header = nrrd.read(nrrd_file)

print("NRRD loaded successfully")
print("Volume shape:", data.shape)


# --------------------------------------------------
# Read all planes from CSV
# --------------------------------------------------
planes = []

with open(csv_file, "r") as file:

    for line_number, line in enumerate(file, start=1):

        line = line.strip()

        # Ignore empty lines
        if not line:
            continue

        values = list(map(float, line.split(",")))

        # 3 points = 9 values
        if len(values) != 9:
            print(
                "Error: Plane on line",
                line_number,
                "must contain 9 values."
            )
            sys.exit(1)

        a = np.array(values[0:3])
        b = np.array(values[3:6])
        c = np.array(values[6:9])

        planes.append((a, b, c))


print("Number of planes:", len(planes))


# --------------------------------------------------
# Create projections
# --------------------------------------------------
projections = []

for i, (a, b, c) in enumerate(planes, start=1):

    print()
    print("-----------------------------")
    print("Processing plane", i)
    print("-----------------------------")

    print("Point a:", a)
    print("Point b:", b)
    print("Point c:", c)

    dist_ab = np.linalg.norm(b - a)
    dist_ac = np.linalg.norm(c - a)

    print("Distance a-b:", dist_ab)
    print("Distance a-c:", dist_ac)

    try:

        E = create_projection(data, a, b, c)

        projections.append(E)

        print("Valid plane")
        print("Projection created successfully")
        print("Projection shape:", E.shape)

    except ValueError:

        print("Invalid plane")
        sys.exit(1)


# --------------------------------------------------
# Print file information
# --------------------------------------------------
print()
print("-----------------------------")
print("Files")
print("-----------------------------")

print("NRRD file:", nrrd_file)
print("CSV file:", csv_file)
print("Output file:", output_file)

# --------------------------------------------------
# Create MP4 video
# --------------------------------------------------
frames = []

for E in projections:
    frame = E.astype(np.float32)

    # Normalize values to 0-255
    if frame.max() > frame.min():
        frame = (frame - frame.min()) / (frame.max() - frame.min()) * 255

    frame = frame.astype(np.uint8)

    # Convert grayscale to RGB
    frame = np.stack([frame, frame, frame], axis=-1)

    frames.append(frame)


# Write projections to MP4
with imageio.get_writer(output_file, fps=1) as writer:
    for frame in frames:
        writer.append_data(frame)


print("MP4 video created successfully:", output_file)