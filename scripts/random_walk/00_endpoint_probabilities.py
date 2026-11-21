import math
import random
import statistics

import matplotlib.pyplot as plt

from pathlib import Path

project_dir = Path(__file__).resolve().parents[2]
figure_dir = project_dir / "reports" / "RandomWalk"
figure_dir.mkdir(parents=True, exist_ok=True)
summary_lines = []

# Experiment 0: distribution of final positions (1D)
particles = 10
steps = 12
repeats = 10000

all_leftist = 0
all_rightist = 0
on_origin = 0
all_same_position_count = 0
half_left_right_count = 0

positions_all = []

for _ in range(repeats):
    positions = [0] * particles

    for i in range(particles):
        for step in range(steps):
            positions[i] += random.choice([-1, 1])

    if all(x == -steps for x in positions):
        all_leftist += 1
    if all(x == steps for x in positions):
        all_rightist += 1
    if all(x == positions[0] for x in positions):
        all_same_position_count += 1

    on_origin += positions.count(0)

    # For even particles: exactly half at -steps, half at +steps.
    # For odd particles: floor(N/2) at each endpoint, one in the interior.
    half = particles // 2
    remaining = particles - 2 * half
    if positions.count(-steps) == half and positions.count(steps) == half:
        if remaining == 0 or (remaining == 1 and sum(-steps < x < steps for x in positions) == 1):
            half_left_right_count += 1

    positions_all.extend(positions)

# Theoretical binomial distribution
possible_positions = []
theory_probabilities = []

for right_moves in range(steps + 1):
    possible_positions.append(2 * right_moves - steps)
    theory_probabilities.append(math.comb(steps, right_moves) / 2**steps)

p_endpoint = 1 / 2**steps if steps > 0 else 1
p_same = sum(p**particles for p in theory_probabilities)
p_origin = theory_probabilities[steps // 2] if steps % 2 == 0 else 0

half = particles // 2
remaining = particles - 2 * half
ways = math.comb(particles, half) * math.comb(particles - half, half)
p_half = ways * p_endpoint**(2 * half)
if remaining == 1:
    p_half *= (1 - 2 * p_endpoint) if steps > 0 else 0

summary_lines.append(f"Particles: {particles} | Steps: {steps} | Repeats: {repeats}")
summary_lines.append(f"All same: {all_same_position_count / repeats:.6f} | Theory: {p_same:.6f}")
summary_lines.append(f"All left: {all_leftist / repeats:.6f} | Theory: {p_endpoint**particles:.6f}")
summary_lines.append(f"All right: {all_rightist / repeats:.6f} | Theory: {p_endpoint**particles:.6f}")
summary_lines.append(f"At origin: {on_origin / (particles * repeats):.6f} | Theory: {p_origin:.6f}")
summary_lines.append(f"Half at each extreme: {half_left_right_count / repeats:.6f} | Theory: {p_half:.6f}")
summary_lines.append(f"Mean: {statistics.mean(positions_all):.4f} | Theory: 0")
summary_lines.append(f"Variance: {statistics.pvariance(positions_all):.4f} | Theory: {steps}")

# The points are separated by 2, so use bins centered on attainable positions.
bin_edges = [x - 1 for x in possible_positions] + [possible_positions[-1] + 1]
theory_counts = [p * particles * repeats for p in theory_probabilities]

plt.figure(figsize=(9, 5))
plt.hist(positions_all, bins=bin_edges, alpha=0.65, label="Simulation")
plt.plot(possible_positions, theory_counts, "o-", label="Binomial theory")
plt.xticks(possible_positions[::max(1, len(possible_positions) // 12)])
plt.xlabel("Final position")
plt.ylabel("Number of particles")
plt.title("1D Random Walk: Endpoint Distribution")
plt.grid(axis="y", alpha=0.25)
plt.legend()
plt.tight_layout()
plt.savefig(figure_dir / "00_endpoint_distribution.png", dpi=160)
plt.close()

summary = "\n".join(summary_lines)
(figure_dir / "00_endpoint_probabilities_summary.txt").write_text(summary + "\n", encoding="utf-8")
print(summary)
