import math
import random

import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path

project_dir = Path(__file__).resolve().parents[2]
figure_dir = project_dir / "reports" / "RandomWalk"
figure_dir.mkdir(parents=True, exist_ok=True)

# Experiment 3: predictable distributions emerge from unpredictable steps.
walks = 16000
steps_to_show = [4, 16, 64, 256]
last_step = max(steps_to_show)

positions_at_time = {step: [] for step in steps_to_show}
for i in range(walks):
    x = 0
    for step in range(1, last_step + 1):
        x += random.choice([-1, 1])
        if step in positions_at_time:
            positions_at_time[step].append(x)

fig, axes = plt.subplots(2, 2, figsize=(11, 8))
for ax, n in zip(axes.flat, steps_to_show):
    positions = positions_at_time[n]
    possible = list(range(-n, n + 1, 2))
    counts = [0] * len(possible)
    for x in positions:
        counts[(x+n)//2] += 1

    measured = [c / walks for c in counts]
    theory = [math.comb(n, k) / 2**n for k in range(n+1)]
    entropy = -sum(p * math.log(p) for p in measured if p > 0)
    entropy_theory = -sum(p * math.log(p) for p in theory if p > 0)

    ax.bar(possible, measured, width=1.6, alpha=0.65, label="Simulation")
    ax.plot(possible, theory, ".", markersize=3, label="Binomial theory")
    ax.set_title(f"n={n} | entropy={entropy:.3f} (theory {entropy_theory:.3f})")
    ax.set_xlabel("Position")
    ax.set_ylabel("Probability")
    ax.legend()
    print(f"Step {n}: empirical entropy {entropy:.4f} | theory {entropy_theory:.4f}")

fig.suptitle("1D Probability Distributions: Entropy in Natural Units (nats)")
plt.tight_layout()
plt.savefig(figure_dir / "03_distribution_entropy.png", dpi=160)
plt.close()

# 2D density: probability contours, rather than decorative contours.
walks_2d = 18000
steps_2d = 160
final_x = []
final_y = []
for i in range(walks_2d):
    x = 0
    y = 0
    for step in range(steps_2d):
        direction = random.randrange(4)
        if direction == 0: x += 1
        if direction == 1: x -= 1
        if direction == 2: y += 1
        if direction == 3: y -= 1
    final_x.append(x)
    final_y.append(y)

# The Gaussian is a large-step approximation to the discrete lattice walk.
# For this 2D square-lattice walk, Var(X)=Var(Y)=steps/2.
limit = 28
bins = np.arange(-limit - 0.5, limit + 1.5, 1)
hist, edges_x, edges_y = np.histogram2d(final_x, final_y, bins=(bins, bins))
# Smooth only for plotting contours (not for computing physical probabilities).
from scipy.ndimage import gaussian_filter
smoothed = gaussian_filter(hist / walks_2d, sigma=2.0)
centers = (bins[:-1] + bins[1:]) / 2

fig, ax = plt.subplots(figsize=(7, 6))
mesh = ax.pcolormesh(edges_x, edges_y, hist.T / walks_2d, shading="auto")
ax.contour(centers, centers, smoothed.T, levels=6, colors="white", linewidths=1)
ax.set_title("2D Endpoint Probability Mass (Contours are Smoothed)")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_aspect("equal")
plt.colorbar(mesh, ax=ax, label="Probability per lattice cell")
plt.tight_layout()
plt.savefig(figure_dir / "03_density_contour.png", dpi=160)
plt.close()
