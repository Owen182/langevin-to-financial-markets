import random

import matplotlib.pyplot as plt

from pathlib import Path

project_dir = Path(__file__).resolve().parents[2]
figure_dir = project_dir / "reports" / "RandomWalk"
figure_dir.mkdir(parents=True, exist_ok=True)
summary_lines = []

# Experiment 6: ordinary vs self-avoiding walks in 2D.
# This is a kinetic-growth (greedy) self-avoiding walk, NOT uniform sampling
# from all self-avoiding walks of a given length. It can get trapped early.
walks = 8
steps = 250

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

for i in range(walks):
    x = y = 0
    path_x = [x]
    path_y = [y]
    for step in range(steps):
        direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        x += direction[0]
        y += direction[1]
        path_x.append(x)
        path_y.append(y)
    ax1.plot(path_x, path_y, alpha=0.65)

    x = y = 0
    path_x = [x]
    path_y = [y]
    visited = {(x, y)}
    for step in range(steps):
        options = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (x+dx, y+dy) not in visited:
                options.append((dx, dy))
        if not options:
            break
        dx, dy = random.choice(options)
        x += dx
        y += dy
        visited.add((x, y))
        path_x.append(x)
        path_y.append(y)
    ax2.plot(path_x, path_y, alpha=0.65)
    summary_lines.append(f"Self-avoiding path {i+1}: {len(path_x)-1} steps before trap or limit")

ax1.set_title("Ordinary 2D Walks")
ax2.set_title("Kinetic-Growth Self-Avoiding Walks")
for ax in [ax1, ax2]:
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.axis("equal")
    ax.grid(alpha=0.2)
plt.tight_layout()
plt.savefig(figure_dir / "06_self_avoiding.png", dpi=160)
plt.close()

summary = "\n".join(summary_lines)
(figure_dir / "06_self_avoiding_walk_summary.txt").write_text(summary + "\n", encoding="utf-8")
print(summary)
