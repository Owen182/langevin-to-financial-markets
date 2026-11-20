import random

import matplotlib.pyplot as plt

from pathlib import Path

project_dir = Path(__file__).resolve().parents[2]
figure_dir = project_dir / "reports" / "RandomWalk"
figure_dir.mkdir(parents=True, exist_ok=True)

# Experiment 4A: time until a 1D walker first reaches +target.
target = 10
walks = 2500
max_steps = 4000
hitting_times = []

for i in range(walks):
    x = 0
    for step in range(1, max_steps + 1):
        x += random.choice([-1, 1])
        if x == target:
            hitting_times.append(step)
            break

print(f"Hit +{target} by {max_steps} steps: {len(hitting_times)/walks:.2%}")
if hitting_times:
    print(f"Mean hitting time among hits only: {sum(hitting_times)/len(hitting_times):.1f}")
    print("This conditional/censored mean is NOT the unconditional theoretical expectation.")
print("Theory: eventual hit probability = 1, but expected hitting time = infinity.")

checkpoints = list(range(0, max_steps + 1, 40))
survival = []
for t in checkpoints:
    hits = sum(hit_time <= t for hit_time in hitting_times)
    survival.append(1 - hits/walks)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.hist(hitting_times, bins=70, alpha=0.75)
ax1.set_title("First-passage Times (Observed Hits Only)")
ax1.set_xlabel("First time to reach target")
ax1.set_ylabel("Number of walkers")
ax2.plot(checkpoints, survival)
ax2.set_title("Survival: Not Yet Hit the Target")
ax2.set_xlabel("Step")
ax2.set_ylabel("Fraction that have never hit")
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(figure_dir / "04_first_passage.png", dpi=160)
plt.close()

# Experiment 4B: return to the origin for simple lattice walks in 1D/2D/3D.
# A finite run measures P(return by max_steps), not eventual return probability.
walks_return = 900
max_steps_return = 2500
checkpoints = [10, 30, 100, 300, 1000, 2500]

fig, ax = plt.subplots(figsize=(8, 5))
for dimension in [1, 2, 3]:
    return_times = []
    for i in range(walks_return):
        position = [0] * dimension
        for step in range(1, max_steps_return + 1):
            axis = random.randrange(dimension)
            position[axis] += random.choice([-1, 1])
            if all(x == 0 for x in position):
                return_times.append(step)
                break

    probability = []
    for t in checkpoints:
        probability.append(sum(x <= t for x in return_times) / walks_return)
    ax.plot(checkpoints, probability, "o-", label=f"{dimension}D")
    print(f"{dimension}D: returned by step {max_steps_return}: {len(return_times)/walks_return:.3f}")

ax.set_xscale("log")
ax.set_ylim(0, 1)
ax.set_xlabel("Maximum allowed steps")
ax.set_ylabel("P(return by this step)")
ax.set_title("Recurrence vs Dimension (Finite-Time Estimates)")
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig(figure_dir / "04_recurrence.png", dpi=160)
plt.close()
print("Infinite-time theory: 1D and 2D eventual return = 1; 3D < 1.")
