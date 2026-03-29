# Collatz Sequence Stopping Time Distribution up to 1,000,000

## Abstract

We compute the total stopping times of all integers from 2 to N = 1,000,000 under the Collatz iteration and characterize their distribution. The Collatz function maps n → n/2 if n is even, and n → 3n + 1 if n is odd; the stopping time is the number of steps to reach 1. Across 999,999 starting values, we find a mean stopping time of 131.43, a median of 125, and a maximum of 524 (attained at n = 837,799). The distribution of stopping times is unimodal and approximately log-normal with a heavy right tail. All integers in the range eventually reach 1, consistent with the Collatz conjecture, though no proof is provided here. The results establish an empirical baseline for the stopping time distribution in this range and quantify its statistical properties.

---

## Background

The **Collatz conjecture** (also known as the 3n+1 problem) was proposed by Lothar Collatz in 1937. Define the function:

```
T(n) = n / 2        if n is even
T(n) = 3n + 1      if n is odd
```

Applying T repeatedly to any positive integer eventually produces a sequence that, conjecturally, always reaches 1. The **total stopping time** of n, denoted σ(n), is the number of iterations required:

```
σ(n) = min { k ≥ 1 : T^k(n) = 1 }
```

Despite its elementary statement, the conjecture remains unproven. Paul Erdős remarked: *"Mathematics is not yet ready for such problems."* Computational verification has confirmed the conjecture for all n up to 2.95 × 10^20 (Oliveira e Silva, 2010). Key theoretical results include bounds on the density of integers that eventually reach 1 (Terras, 1976; Allouche, 1979) and probabilistic heuristics suggesting stopping times grow as O(log n) on average (Lagarias, 1985).

---

## Hypothesis

We hypothesize:

1. All integers from 2 to 1,000,000 will eventually reach 1 (consistent with known computational verification).
2. The mean stopping time will grow roughly as O(log N), placing it in the range of 80–160 steps for N = 10^6 (following the heuristic from Lagarias, 1985).
3. The distribution of stopping times will be unimodal, roughly bell-shaped, and right-skewed due to a sparse tail of exceptionally long sequences.
4. The maximum stopping time will be attained by a starting value that is not the largest integer in the range, reflecting the irregular nature of Collatz trajectories.

---

## Method

1. For each integer n from 2 to N = 1,000,000, apply the Collatz iteration until reaching 1 and record the total step count σ(n).
2. Compute summary statistics: minimum, maximum, mean, median, standard deviation.
3. Compute the frequency distribution of stopping times (histogram with bin width 10).
4. Identify the top 10 most common stopping times.
5. Record the starting value n* that maximizes σ(n).

All computation is performed in pure Python with no external dependencies.

---

## Experiment

The experiment was run as `code/run_experiment.py`. The script:

- Iterates over each n from 2 to 1,000,000.
- Applies the Collatz map until n = 1, counting steps.
- Accumulates stopping times into a list.
- Computes summary statistics, a binned histogram, and the top 10 most frequent stopping times.
- Outputs `results/summary.json`, `results/histogram.json`, `results/top10_stopping_times.json`, and `results/report.txt`.

---

## Results

### Coverage and Convergence

All 999,999 integers from 2 to 1,000,000 reached 1 under the Collatz iteration. No counterexample to the conjecture was found in this range.

### Summary Statistics

| Metric | Value |
|---|---|
| Range analyzed | 2 to 1,000,000 |
| Values computed | 999,999 |
| Minimum stopping time | 1 (n = 2: 2 → 1) |
| Maximum stopping time | 524 (n = 837,799) |
| Mean stopping time | 131.435 |
| Median stopping time | 125 |
| Standard deviation | 56.670 |
| Distinct stopping times | 436 |

### Maximum Stopping Time

The integer n = 837,799 has the longest Collatz trajectory in [2, 10^6], reaching 1 in 524 steps. This is well-known in the literature as the record holder in this range. Notably, 837,799 < 1,000,000, confirming hypothesis 4: the maximum is not achieved at the boundary of the range.

### Top 10 Most Common Stopping Times

| Stopping Time | Occurrences | % of all values |
|---|---|---|
| 95 | 12,169 | 1.217% |
| 87 | 11,829 | 1.183% |
| 100 | 11,781 | 1.178% |
| 82 | 11,586 | 1.159% |
| 113 | 11,099 | 1.110% |
| 170 | 10,626 | 1.063% |
| 69 | 10,624 | 1.062% |
| 157 | 10,620 | 1.062% |
| 92 | 10,476 | 1.048% |
| 126 | 10,392 | 1.039% |

No single stopping time dominates: the most common value (95 steps) accounts for only 1.217% of all starting integers. The distribution is spread across 436 distinct values, indicating high dispersion.

### Distribution Shape

The stopping time distribution is unimodal and roughly symmetric around its mode (near 95–100 steps), with a pronounced right tail extending to 524. The mean (131.4) exceeds the median (125), and both exceed the mode region, confirming right skew. The standard deviation of 56.7 is substantial — roughly 43% of the mean — indicating wide variability across starting values.

---

## Conclusion

All four hypotheses were confirmed:

1. **All integers reached 1**: No counterexample to the Collatz conjecture was found for n ≤ 10^6.
2. **Mean ≈ O(log N)**: The observed mean of 131.4 steps falls within the predicted range of 80–160 for N = 10^6, consistent with Lagarias's (1985) O(log n) heuristic.
3. **Unimodal right-skewed distribution**: The distribution peaks near 95–100 steps and has a heavy right tail reaching 524, consistent with a log-normal-like profile.
4. **Maximum not at boundary**: The record n = 837,799 lies well below the range maximum, confirming the non-monotone character of Collatz trajectories.

The empirical distribution of stopping times provides a detailed statistical baseline for the Collatz map on [2, 10^6]. The wide dispersion (σ = 56.7) and 436 distinct stopping times illustrate the complexity of the iteration despite its elementary definition.

---

## Limitations

- This study is purely empirical and provides no proof or partial proof of the Collatz conjecture.
- The analysis covers only n ≤ 10^6. The mean stopping time is known to grow, and the record trajectory length increases for larger N.
- No analysis of intermediate peak values (the maximum value reached during a trajectory before descending to 1) was performed.
- No comparison to theoretical distributions (e.g., log-normal fit) was quantified with goodness-of-fit statistics.

---

## References

1. Collatz, L. (1937). Problem posed at the International Congress of Mathematicians, Oslo.
2. Lagarias, J. C. (1985). *The 3x+1 problem and its generalizations*. American Mathematical Monthly, 92(1), 3–23.
3. Terras, R. (1976). *A stopping time problem on the positive integers*. Acta Arithmetica, 30, 241–252.
4. Oliveira e Silva, T. (2010). *Empirical verification of the 3x+1 and related conjectures*. In J. C. Lagarias (Ed.), The Ultimate Challenge: The 3x+1 Problem. AMS.
5. Lagarias, J. C. (Ed.) (2010). *The Ultimate Challenge: The 3x+1 Problem*. American Mathematical Society.
