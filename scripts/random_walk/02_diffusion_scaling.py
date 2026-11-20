import math
import random

import matplotlib.pyplot as plt

from pathlib import Path

project_dir = Path(__file__).resolve().parents[2]
figure_dir = project_dir / "reports" / "RandomWalk"
figure_dir.mkdir(parents=True, exist_ok=True)

# Experiment 2: random motion can be unpredictable, but MSD is predictable.
walks = 2500
steps = 600
record_every = 10

times = list(range(0, steps + 1, record_every))
sum_x = [0.0] * len(times)
sum_x2 = [0.0] * len(times)

for i in range(walks):
    x = 0
    index = 0
    for step in range(steps + 1):
        if step % record_every == 0:
            sum_x[index] += x
            sum_x2[index] += x*x
            index += 1
        if step < steps:
            x += random.choice([-1, 1])

mean = [x / walks for x in sum_x]
msd = [x / walks for x in sum_x2]
variance = [msd[i] - mean[i]**2 for i in range(len(times))]

# Fit log(MSD) = alpha * log(t) + constant, ignoring t=0.
log_t = []
log_msd = []
for i in range(1, len(times)):
    if msd[i] > 0:
        log_t.append(math.log(times[i]))
        log_msd.append(math.log(msd[i]))

mean_t = sum(log_t) / len(log_t)
mean_m = sum(log_msd) / len(log_msd)
top = sum((log_t[i] - mean_t) * (log_msd[i] - mean_m) for i in range(len(log_t)))
bottom = sum((x - mean_t)**2 for x in log_t)
alpha = top / bottom

print(f"Measured MSD scaling exponent alpha = {alpha:.4f} | Theory = 1")
print(f"Final MSD = {msd[-1]:.3f} | Theory = {steps}")
print(f"Final variance = {variance[-1]:.3f} | Theory = {steps}")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.plot(times, msd, label="Simulation: E[X^2]")
ax1.plot(times, times, "--", label="Theory: n")
ax1.plot(times, variance, ":", label="Simulation: Var(X)")
ax1.set_xlabel("Number of steps")
ax1.set_ylabel("Squared displacement")
ax1.set_title("Diffusive Spreading")
ax1.grid(alpha=0.25)
ax1.legend()

ax2.loglog(times[1:], msd[1:], "o", markersize=3, label=f"Measured alpha = {alpha:.3f}")
ax2.loglog(times[1:], times[1:], "--", label="Theory: alpha = 1")
ax2.set_xlabel("Steps (log scale)")
ax2.set_ylabel("MSD (log scale)")
ax2.set_title("Finding the Scaling Law")
ax2.grid(alpha=0.25)
ax2.legend()
plt.tight_layout()
plt.savefig(figure_dir / "02_diffusion_scaling.png", dpi=160)
plt.close()
