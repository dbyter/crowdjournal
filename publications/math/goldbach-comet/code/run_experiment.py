"""
Goldbach Comet: Representation Counts for Even Integers up to N = 100,000
For each even n in [4, N], counts the number of ways to write n = p + q
where p <= q and both p, q are prime.

Algorithm: for each prime p <= N//2, scan primes q >= p until p+q > N.
Since p <= q, we only need p <= N//2. Total work ~ sum over p of pi(N-p),
roughly 24M operations for N=100,000.
"""

import bisect
import json
import math
from collections import Counter

N = 100_000


def sieve(limit):
    is_prime = bytearray([1]) * (limit + 1)
    is_prime[0] = is_prime[1] = 0
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i * i :: i] = bytearray(len(is_prime[i * i :: i]))
    return is_prime


def main():
    print(f"Sieving primes up to {N:,}...")
    is_prime = sieve(N)
    primes = [i for i in range(2, N + 1) if is_prime[i]]
    half_primes = [p for p in primes if p <= N // 2]

    print(f"Primes up to {N:,}: {len(primes):,}  |  up to {N//2:,}: {len(half_primes):,}")
    print("Computing Goldbach representations...")

    counts = [0] * (N + 1)
    for p in half_primes:
        start_idx = bisect.bisect_left(primes, p)
        for q in primes[start_idx:]:
            s = p + q
            if s > N:
                break
            # p and q same parity => p+q even; or p=q=2 => s=4 even
            if s % 2 == 0:
                counts[s] += 1

    even_ns = list(range(4, N + 1, 2))
    reps = [counts[n] for n in even_ns]
    failed = [n for n, r in zip(even_ns, reps) if r == 0]

    total = len(even_ns)
    mean_rep = sum(reps) / total
    sorted_reps = sorted(reps)
    median_rep = sorted_reps[total // 2]
    variance = sum((x - mean_rep) ** 2 for x in reps) / total
    std_dev = math.sqrt(variance)

    max_rep = max(reps)
    max_rep_n = even_ns[reps.index(max_rep)]
    min_rep = min(reps)
    min_rep_n = even_ns[reps.index(min_rep)]

    freq = Counter(reps)
    rep_distribution = {str(k): v for k, v in sorted(freq.items(), key=lambda x: int(x[0]))}

    # Comet: mean reps per bin of width 1000
    bins = {}
    for n, r in zip(even_ns, reps):
        b = ((n - 4) // 1000) * 1000 + 4
        bins.setdefault(b, []).append(r)
    comet_data = {str(b): round(sum(v) / len(v), 4) for b, v in sorted(bins.items())}

    summary = {
        "N": N,
        "even_integers_checked": total,
        "goldbach_conjecture_holds": len(failed) == 0,
        "failed_cases": failed,
        "min_representations": int(min_rep),
        "min_rep_n": int(min_rep_n),
        "max_representations": int(max_rep),
        "max_rep_n": int(max_rep_n),
        "mean_representations": round(mean_rep, 6),
        "median_representations": int(median_rep),
        "std_dev_representations": round(std_dev, 6),
        "distinct_rep_counts": len(freq),
    }

    import os
    os.makedirs("results", exist_ok=True)

    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    with open("results/rep_distribution.json", "w") as f:
        json.dump(rep_distribution, f, indent=2)
    with open("results/comet_data.json", "w") as f:
        json.dump(comet_data, f, indent=2)

    with open("results/report.txt", "w") as f:
        f.write("Goldbach Comet Report\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Range: even integers 4 to {N:,}\n")
        f.write(f"Total checked: {total:,}\n")
        f.write(f"Conjecture holds: {len(failed) == 0}\n")
        if failed:
            f.write(f"Failed cases: {failed}\n")
        f.write(f"\nMin representations: {min_rep}  (n = {min_rep_n:,})\n")
        f.write(f"Max representations: {max_rep}  (n = {max_rep_n:,})\n")
        f.write(f"Mean representations: {mean_rep:.6f}\n")
        f.write(f"Median representations: {median_rep}\n")
        f.write(f"Std deviation: {std_dev:.6f}\n")
        f.write(f"Distinct rep counts: {len(freq)}\n\n")
        f.write("Comet trend (mean reps per 1000-wide bin of n):\n")
        for b, avg in comet_data.items():
            f.write(f"  n ~ {int(b):>7,}: mean reps = {avg:.2f}\n")

    print("Done.")
    print(f"  Conjecture holds: {len(failed) == 0}")
    print(f"  Max representations: {max_rep} at n={max_rep_n:,}")
    print(f"  Mean representations: {mean_rep:.4f}")


if __name__ == "__main__":
    main()
