# Random Walk Report Notes (starting outline)

## 1. Model

One-dimensional unbiased walk: `X_n = sum_{i=1}^n xi_i` where `xi_i` is +1 or -1 with equal probability, independently.

`P(X_n = 2k-n) = C(n,k) / 2^n`, `E[X_n] = 0`, `E[X_n^2] = Var(X_n) = n`.

For N independent walkers, probability that all have the same final position:

`sum_{k=0}^n [C(n,k) / 2^n]^N`.

## 2. Scaling and continuum connection

With physical step length `a` and timestep `dt`, `E[x(t)^2] = (a^2/dt)t = 2Dt` for one dimension; `D = a^2/(2dt)`. A suitably rescaled walk converges in distribution to Brownian motion (under standard assumptions).

For the 2D lattice model moving one unit along one of four cardinal directions per step, `E[r^2] = n`, with `Var(x)=Var(y)=n/2`.

## 3. Probability and entropy

Discrete Shannon entropy is `H = -sum_x p(x) ln p(x)` in nats. This is not the same as continuous differential entropy. For the 1D binomial endpoint distribution, asymptotically `H ~ (1/2) ln(pi e n / 2)` for large n.

Compare empirical frequencies with the exact binomial PMF. A Gaussian is an approximate large-n envelope; attainable parity positions remain discrete.

## 4. First passage and return

The probability a symmetric 1D walk eventually reaches a fixed positive threshold is 1, but the expected hitting time is infinite. Simulations with a maximum step count have right-censored trajectories; report non-hit rates.

Simple symmetric lattice walk: 1D and 2D are recurrent; 3D is transient. Finite-step simulations approach, but do not equal, eventual return probabilities.

## 5. Modified walks

Biased step probability `P(+1)=p`: `E[X_n]=n(2p-1)` and `Var(X_n)=4np(1-p)`. Thus `E[X_n^2]=4np(1-p)+n^2(2p-1)^2`. A quadratic-looking MSD by itself is not proof of superdiffusive fluctuations.

Persistent walk: correlated steps give near-ballistic early growth; correlations decay, and normal diffusion typically emerges at long times for a finite persistence length. Greedy self-avoiding walks can trap early, and have a different sampling law from uniform SAWs.

## 6. Questions to investigate

1. Does the simulation MSD converge to `n` when the number of walkers increases?
2. How does measured entropy grow with n? Does it approach the asymptotic logarithmic trend?
3. Why does the empirical average first-passage time depend strongly on the simulation cutoff?
4. How does return probability change between one, two, and three dimensions?
5. Does persistent motion look ballistic over a short range and diffusive over a long range?

## 7. Limitations and reproducibility

Use random seeds if you need repeatable figures. Record all parameters and numerical errors. Results are stochastic and vary from run to run; finite samples do not establish asymptotic laws.
