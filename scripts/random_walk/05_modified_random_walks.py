import math
import random

import matplotlib.pyplot as plt

from pathlib import Path

project_dir = Path(__file__).resolve().parents[2]
figure_dir = project_dir / "reports" / "RandomWalk"
figure_dir.mkdir(parents=True, exist_ok=True)

# Experiment 5: ordinary, biased and persistent 1D random walks.
walks = 1800
steps = 600
record_every = 10
bias_right = 0.65
p_keep_direction = 0.90

# For biased walks, E[X^2] contains the growing mean^2 term.
# Compare centered variance as well as MSD to distinguish drift from diffusion.
models = ["Ordinary", "Biased", "Persistent"]
times = list(range(0, steps + 1, record_every))
results = {}

for model in models:
    sum_x = [0.0] * len(times)
    sum_x2 = [0.0] * len(times)

    for i in range(walks):
        x = 0
        direction = random.choice([-1, 1])
        index = 0
        for step in range(steps + 1):
            if step % record_every == 0:
                sum_x[index] += x
                sum_x2[index] += x*x
                index += 1
            if step == steps:
                break

            if model == "Ordinary":
                move = random.choice([-1, 1])
            elif model == "Biased":
                move = 1 if random.random() < bias_right else -1
            else:
                if random.random() >= p_keep_direction:
                    direction *= -1
                move = direction
            x += move

    mean = [s/walks for s in sum_x]
    msd = [s/walks for s in sum_x2]
    variance = [max(0.0, msd[j]-mean[j]**2) for j in range(len(times))]
    results[model] = (mean, msd, variance)


# Comparing the modified walks with theory
print("\n--- Modified Random Walk Results ---")

for model in models:
    mean, msd, variance = results[model]

    if model == "Ordinary":
        theory_mean = 0
        theory_variance = steps
        theory_msd = steps

    elif model == "Biased":
        drift = 2 * bias_right - 1

        theory_mean = drift * steps
        theory_variance = (1 - drift**2) * steps
        theory_msd = theory_variance + theory_mean**2

    else:
        # Correlation between steps in the persistent walk
        correlation = 2 * p_keep_direction - 1

        theory_mean = 0
        theory_variance = steps

        for k in range(1, steps):
            theory_variance += 2 * (steps - k) * correlation**k

        theory_msd = theory_variance

    mean_error = abs(mean[-1] - theory_mean)
    variance_error = abs(variance[-1] - theory_variance)
    msd_error = abs(msd[-1] - theory_msd)

    print(f"\n{model} Walk")

    print(f"Mean: {mean[-1]:.4f} | Theory: {theory_mean:.4f}")
    print(f"Absolute difference: {mean_error:.4f}")

    print(f"Variance: {variance[-1]:.4f} | Theory: {theory_variance:.4f}")
    print(f"Absolute difference: {variance_error:.4f}")

    print(f"MSD: {msd[-1]:.4f} | Theory: {theory_msd:.4f}")
    print(f"Absolute difference: {msd_error:.4f}")

    if theory_msd > 0:
        print(f"MSD relative error: {msd_error / theory_msd * 100:.3f}%")


fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for model in models:
    mean, msd, variance = results[model]
    axes[0].plot(times, mean, label=model)
    axes[1].plot(times, msd, label=model)
    axes[2].plot(times, variance, label=model)
    print(f"{model}: final mean={mean[-1]:.2f}, MSD={msd[-1]:.2f}, variance={variance[-1]:.2f}")

axes[0].plot(times, [(2*bias_right-1)*t for t in times], "k--", alpha=0.5, label="Biased mean theory")
axes[1].plot(times, times, "k--", alpha=0.5, label="Ordinary MSD theory")
axes[2].plot(times, times, "k--", alpha=0.5, label="Ordinary variance theory")
for ax, title, ylabel in zip(axes, ["Mean Displacement", "Uncentered MSD", "Centered Variance"], ["E[X]", "E[X^2]", "Var(X)"]):
    ax.set_title(title)
    ax.set_xlabel("Step")
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.25)
    ax.legend()
plt.tight_layout()
plt.savefig(figure_dir / "05_modified_walks.png", dpi=160)
plt.close()
print("Note: a persistent walk crosses from near-ballistic to diffusive scaling.")
print("A biased walk's MSD can appear quadratic because of drift; check variance.")
