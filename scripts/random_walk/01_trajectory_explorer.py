import random

import matplotlib.pyplot as plt

from pathlib import Path

project_dir = Path(__file__).resolve().parents[2]
figure_dir = project_dir / "reports" / "RandomWalk"
figure_dir.mkdir(parents=True, exist_ok=True)

# Experiment 1: individual paths in 1D, 2D, and 3D
steps = 1200
walks = 6

fig = plt.figure(figsize=(16, 5))
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133, projection="3d")

for i in range(walks):
    x = 0
    y = 0
    z = 0
    path_x = [x]
    path_y = [y]
    path_z = [z]

    for step in range(steps):
        x += random.choice([-1, 1])
        path_x.append(x)

    ax1.plot(range(steps + 1), path_x, alpha=0.65)

    x = 0
    y = 0
    path_x = [0]
    path_y = [0]
    for step in range(steps):
        direction = random.randrange(4)
        if direction == 0: x += 1
        if direction == 1: x -= 1
        if direction == 2: y += 1
        if direction == 3: y -= 1
        path_x.append(x)
        path_y.append(y)
    ax2.plot(path_x, path_y, alpha=0.65)

    x = y = z = 0
    path_x = [0]
    path_y = [0]
    path_z = [0]
    for step in range(steps):
        direction = random.randrange(6)
        if direction == 0: x += 1
        if direction == 1: x -= 1
        if direction == 2: y += 1
        if direction == 3: y -= 1
        if direction == 4: z += 1
        if direction == 5: z -= 1
        path_x.append(x)
        path_y.append(y)
        path_z.append(z)
    ax3.plot(path_x, path_y, path_z, alpha=0.7)

ax1.set_title("1D Walks")
ax1.set_xlabel("Step")
ax1.set_ylabel("Position")
ax2.set_title("2D Square Lattice")
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.axis("equal")
ax3.set_title("3D Cubic Lattice")
ax3.set_xlabel("x")
ax3.set_ylabel("y")
ax3.set_zlabel("z")
plt.tight_layout()
plt.savefig(figure_dir / "01_trajectories.png", dpi=160)
plt.close()
print("Saved trajectories in 1D, 2D and 3D.")
