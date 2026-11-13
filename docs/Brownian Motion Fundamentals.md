# Brownian Motion

## Random Walk and Wiener Process

Let's begin with a random walk. In a coin-flip random walk, an object moves left or right depending on the result of the flipped coin with fixed amount of magnitude (eg., +1, -1). This giving a discrete evolution of object behaviour. Wiener process, on the other hand, will have the process in continuous form.

A coin-flip random walk approaches Brownian motion as we take more steps per second and make each step smaller. In this project, I shall simulate Brownian motion directly by drawing Gaussian increments. This gives the correct distribution at the times we sample.

## Why does $W_t - W_s \sim \mathcal{N}(0, t-s)$?

Suppose we flip a fair coin $n$ times per second and take a step of size $1/\sqrt{n}$ to the left or right on each flip. The mean of one step is zero. Using the variance formula,

$$
\operatorname{Var}(X) = E[X^2] - (E[X])^2 = \frac{1}{n}.
$$

As $n$ increases, the Central Limit Theorem explains why the sum of those steps approaches a normal distribution.

## Why do we use $\Delta W = \sqrt{\Delta t}\,Z$?

In the simulation, one Gaussian draw represents the net change over a whole time step $\Delta t$. We want that change to have variance $\Delta t$, so its standard deviation would be $\sqrt{\Delta t}$.

Drawing $Z$ from the standard normal distribution, $Z\sim\mathcal{N}(0,1)$. The numbers $0$ and $1$ denote its mean and variance. A draw can be negative or greater than $1$, and because $Z$ has standard deviation of $1$, multiplying it by $\sqrt{\Delta t}$ will gives us the variance we want.