import math
import random
import statistics
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

out = Path(__file__).resolve().parent
rng = random.Random(42)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True,
                     "grid.alpha": 0.22, "axes.labelcolor": "#233954"})

# Brownian example from the chat.
dt = 0.01
times = [step * dt for step in range(101)]
paths = []
for _ in range(100):
    x = 0.0
    path = [x]
    for _ in range(100):
        x += math.sqrt(dt) * rng.gauss(0, 1)
        path.append(x)
    paths.append(path)

msd = [sum(path[j]**2 for path in paths) / len(paths) for j in range(101)]
fig, (ax, bx) = plt.subplots(1, 2, figsize=(9, 3), layout="constrained")
for path in paths:
    ax.plot(times, path, color="#176a84", alpha=0.13, linewidth=0.65)
ax.set(xlabel="Time", ylabel="W(t)", title="100 Wiener paths")
bx.plot(times, msd, color="#176a84", label="Simulation")
bx.plot(times, times, "--", color="#a64b2a", label="Theory: MSD = t")
bx.set(xlabel="Time", ylabel="Mean squared displacement", title="Ensemble MSD")
bx.legend()
fig.savefig(out / "brownian_example.pdf")
plt.close(fig)

# User's Langevin update, plus the 100-path plotting subset.
rng = random.Random(42)
num_particles = 10000
m = gamma = kBT = 1.0
total_time = 10.0
total_steps = 1000
dt = total_time / total_steps
a = gamma / m
b = math.sqrt(2 * gamma * kBT) / m
noise_scale = b * math.sqrt(dt)
times = [step * dt for step in range(total_steps + 1)]
pos_final, velo_final, pos_stored = [], [], []
for particle in range(num_particles):
    x = v = 0.0
    positions = [x]
    for step in range(total_steps):
        z = rng.gauss(0, 1)
        x += v * dt
        v += -a * v * dt + noise_scale * z
        if particle < 100:
            positions.append(x)
    if particle < 100:
        pos_stored.append(positions)
    pos_final.append(x)
    velo_final.append(v)

t = times[-1]
var_v = b**2 / (2*a) * (1 - math.exp(-2*a*t))
var_x = (b/a)**2 * (t - 2*(1-math.exp(-a*t))/a
                    + (1-math.exp(-2*a*t))/(2*a))
theory_x = statistics.NormalDist(0, math.sqrt(var_x))
theory_v = statistics.NormalDist(0, math.sqrt(var_v))

fig, (ax, hx) = plt.subplots(1, 2, figsize=(9, 3.1), sharey=True,
                            gridspec_kw={"width_ratios": [3, 1]},
                            layout="constrained")
for path in pos_stored:
    ax.plot(times, path, color="#176a84", alpha=0.17, linewidth=0.7)
ax.set(xlabel="Time", ylabel="Position", title="First 100 trajectories")
hx.hist(pos_final, bins=40, density=True, orientation="horizontal",
        color="#176a84", alpha=0.55, label="Simulation")
lo, hi = hx.get_ylim()
grid = [lo + (hi - lo) * i / 299 for i in range(300)]
hx.plot([theory_x.pdf(x) for x in grid], grid, "--",
        color="#a64b2a", label="Theory")
hx.set(xlabel="Density", title="Position at t = 10")
hx.legend(fontsize=8)
fig.savefig(out / "langevin_position.pdf")
plt.close(fig)

fig, ax = plt.subplots(figsize=(6.5, 2.6), layout="constrained")
ax.hist(velo_final, bins=40, density=True, color="#176a84", alpha=0.55,
        label="Simulation")
lo, hi = ax.get_xlim()
grid = [lo + (hi - lo) * i / 299 for i in range(300)]
ax.plot(grid, [theory_v.pdf(v) for v in grid], "--",
        color="#a64b2a", label="Theory")
ax.set(xlabel="Velocity", ylabel="Density", title="Velocity at t = 10")
ax.legend()
fig.savefig(out / "langevin_velocity.pdf")
plt.close(fig)

for data, var in [(pos_final, var_x), (velo_final, var_v)]:
    print(f"{statistics.mean(data):.6f} {statistics.pvariance(data):.6f} {var:.6f}")
