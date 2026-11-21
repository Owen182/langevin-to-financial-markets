# Random Walk Experiments

A group of numerical investigations that can live inside the `langevin-to-financial-markets` repository.

## Project layout

```text
langevin-to-financial-markets/
  scripts/
    random_walk/
      00_endpoint_probabilities.py
      01_trajectory_explorer.py
      02_diffusion_scaling.py
      03_density_and_entropy.py
      04_first_passage_and_recurrence.py
      05_modified_random_walks.py
      06_self_avoiding_walk.py
  reports/
    RandomWalk/
  docs/
    random_walk_report_notes.md
```

This ZIP already follows the suggested layout. Copy `scripts/random_walk/` into your existing repository, merge `docs/` and `reports/`, and keep the rest of your project unchanged. The scripts expect you to run them **from the repository root**, not from within `scripts/random_walk/`.

## Running

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

From your project root:

```powershell
python scripts/random_walk/00_endpoint_probabilities.py
python scripts/random_walk/01_trajectory_explorer.py
python scripts/random_walk/02_diffusion_scaling.py
python scripts/random_walk/03_density_and_entropy.py
python scripts/random_walk/04_first_passage_and_recurrence.py
python scripts/random_walk/05_modified_random_walks.py
python scripts/random_walk/06_self_avoiding_walk.py
```

The same commands work directly after extracting this ZIP and opening its top-level folder.

The Random Walk scripts write figures to `reports/RandomWalk/`. The scripts that print numerical results also save those results as `*_summary.txt` in the same folder. Each successful run replaces that script's previous summary. To experiment, edit the variables at the top of each file.

`python scripts/langevin` saves its position and velocity statistics in `reports/Langevin/langevin_summary.txt`. `python scripts/brownian_motion` saves its final statistics in `reports/Brownian/brownian_motion_summary.txt` and displays its figure. The report figure generator saves its Langevin statistics in `docs/brownian_langevin_source/make_figures_summary.txt`.

## Scientific notes

- Random walks assume independent nearest-neighbor jumps unless the specific experiment says otherwise.
- The 2D and 3D models choose one coordinate axis per step; total squared displacement is still expected to be `n`.
- `03_density_and_entropy.py` uses SciPy only to smooth **displayed contour lines**. Probability heatmap uses unsmoothed data. Discrete entropy is in **nats**, not differential entropy.
- A finite first-passage simulation has **censored** non-hits. Do not treat the mean among observed hits as the true mean hitting time.
- Finite-time return fractions are **not** infinite-time recurrence probabilities.
- Greedy self-avoiding paths are *not* sampled uniformly from all fixed-length self-avoiding walks.
- In biased walks, compare `Var(X)` and `E[X^2]` separately so drift is not confused with enhanced diffusion.

## Suggested order for a report

Start with 00, 02 and 03 (binomial → diffusion and Gaussian approximation); connect them to Brownian motion, the diffusion equation and your Langevin simulation. Use 04–06 as extensions, or as the basis for a separate repository later.
