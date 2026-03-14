# Prime Gap Distribution Analysis up to 1,000,000

## Abstract

We analyze the distribution of gaps between consecutive prime numbers up to N = 1,000,000. Using the Sieve of Eratosthenes, we enumerate all 78,498 primes in this range and compute their 78,497 consecutive gaps. We examine the observed mean gap against the theoretical prediction of ln(N) from the Prime Number Theorem, characterize the frequency distribution of gap sizes, identify the maximum gap, and verify that nearly all gaps are even — consistent with elementary number theory. The observed mean gap of 12.739 closely matches the theoretical prediction of ln(10^6) ≈ 13.816, with a relative error of 7.79%.

---

## Background

The distribution of prime numbers is one of the oldest and most studied topics in number theory. The **Prime Number Theorem** (PNT), independently proved by Hadamard and de la Vallée Poussin in 1896, states that the number of primes up to N is asymptotically:

```
π(N) ~ N / ln(N)
```

A direct consequence is that the average gap between consecutive primes near N is approximately ln(N). Understanding how gaps are distributed — their most common values, extremes, and parity — gives insight into the local structure of primes beyond what π(N) captures.

Key open questions related to prime gaps include:
- **Twin Prime Conjecture**: are there infinitely many primes p such that p+2 is also prime (gap = 2)?
- **Polignac's Conjecture**: for every even positive integer 2k, are there infinitely many prime gaps of size 2k?
- **Cramér's Conjecture**: the maximum prime gap near N is O((ln N)^2).

---

## Hypothesis

We hypothesize:

1. The observed mean prime gap up to 10^6 will be close to ln(10^6) ≈ 13.816, within 10%.
2. The most common gap size will be 6, as it is the smallest admissible gap size not eliminated by divisibility constraints modulo 2, 3, and 5 — consistent with the "jumping champions" framework for prime gaps near 10^6.
3. All gaps except the gap between 2 and 3 will be even, since all primes greater than 2 are odd and the difference of two odd numbers is even.
4. The maximum gap will not exceed (ln N)^2 ≈ 191, consistent with Cramér's Conjecture.

---

## Method

1. Generate all primes ≤ 1,000,000 using the **Sieve of Eratosthenes** — a classical O(N log log N) algorithm.
2. Compute the sequence of gaps g_i = p_{i+1} - p_i for i = 1, …, π(N)−1.
3. Compute summary statistics: mean, minimum, maximum, and frequency distribution.
4. Compare the observed mean to the PNT prediction ln(N).
5. Examine gap parity and identify any odd gaps.

All computation is performed in pure Python with no external dependencies.

---

## Experiment

The experiment was run as `code/run_experiment.py`. The script:

- Allocates a bytearray sieve of size N+1.
- Marks composites by striking out multiples of each prime p starting at p².
- Collects all primes into a list and computes pairwise differences.
- Outputs `results/summary.json`, `results/gap_frequency.json`, and `results/report.txt`.

---

## Results

### Prime Count

| Quantity | Value |
|---|---|
| Upper bound N | 1,000,000 |
| Primes found π(N) | 78,498 |
| Gaps computed | 78,497 |

### Mean Gap vs. Theory

| Metric | Value |
|---|---|
| Observed mean gap | 12.739098 |
| Theoretical mean ln(N) | 13.815511 |
| Relative error | 7.79% |

The observed mean is about 7.8% below the asymptotic prediction. This is expected: ln(N) is an asymptotic approximation and the true mean gap approaches ln(N) from below for finite N, since denser prime regions (small primes) pull the average down.

### Extremes

| Metric | Value |
|---|---|
| Minimum gap | 1 (between primes 2 and 3 only) |
| Maximum gap | 114 (after prime 492,113) |

The maximum gap of 114 is well below Cramér's bound of (ln 10^6)² ≈ 191, consistent with the conjecture.

### Top 10 Most Common Gaps

| Gap | Occurrences | % of all gaps |
|---|---|---|
| 6 | 13,549 | 17.26% |
| 2 | 8,169 | 10.41% |
| 4 | 8,143 | 10.37% |
| 12 | 8,005 | 10.20% |
| 10 | 7,079 | 9.02% |
| 8 | 5,569 | 7.09% |
| 18 | 4,909 | 6.25% |
| 14 | 4,233 | 5.39% |
| 16 | 2,881 | 3.67% |
| 24 | 2,682 | 3.42% |

Gap 6 is by far the most common, appearing in 17.26% of all gaps. This is consistent with the "jumping champion" phenomenon: for N around 10^6, the gap size 6 is the most frequently occurring gap (Odlyzko, Rubinstein, Wolf, 1999).

### Gap Parity

Only one odd gap was observed: gap = 1, occurring exactly once (between primes 2 and 3). All remaining 78,496 gaps are even. This is as expected: for p, q both odd and p < q, the gap q − p must be even.

### Distinct Gap Sizes

The experiment identified **52 distinct gap sizes** in [1, 114], all of which are even except for the single gap of 1. The gap sizes form a sparse subset of even integers, not every even number appears.

---

## Conclusion

All four hypotheses were confirmed:

1. **Mean gap ≈ ln(N)**: Observed 12.739 vs. predicted 13.816, within 7.8% — well within 10%.
2. **Gap 6 is most common**: Gap 6 appeared 13,549 times (17.26%), the clear plurality.
3. **All gaps except 2→3 are even**: Confirmed exactly; one odd gap of size 1.
4. **Max gap < (ln N)²**: Observed max gap 114 vs. bound 191 — consistent with Cramér's Conjecture.

The results strongly corroborate both the Prime Number Theorem's asymptotic prediction and elementary parity arguments. The dominance of gap 6 is a manifestation of the "jumping champions" phenomenon and the structure of admissible prime constellations modulo small primes.

---

## Limitations

- The analysis covers only N ≤ 10^6. Gap distribution properties may shift for larger N (e.g., the jumping champion transitions from 6 to 30 around N ≈ 1.7 × 10^35).
- No statistical significance tests (e.g., χ² goodness-of-fit against conjectured distributions) were performed.
- The relationship between gap size and position along the number line (local density variation) was not examined.

---

## References

1. Hadamard, J. (1896). *Sur la distribution des zéros de la fonction ζ(s) et ses conséquences arithmétiques*. Bulletin de la Société Mathématique de France, 24, 199–220.
2. de la Vallée Poussin, C.-J. (1896). *Recherches analytiques sur la théorie des nombres premiers*. Annales de la Société Scientifique de Bruxelles, 20, 183–256.
3. Cramér, H. (1936). *On the order of magnitude of the difference between consecutive prime numbers*. Acta Arithmetica, 2, 23–46.
4. Odlyzko, A., Rubinstein, M., & Wolf, M. (1999). *Jumping Champions*. Experimental Mathematics, 8(2), 107–118.
5. Polignac, A. de (1849). *Recherches nouvelles sur les nombres premiers*. Comptes Rendus, 29, 397–401.
