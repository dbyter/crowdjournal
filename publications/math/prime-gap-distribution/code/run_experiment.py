"""
Prime Gap Distribution Analysis up to N = 1,000,000

Generates all primes up to N using the Sieve of Eratosthenes,
computes consecutive prime gaps, and produces summary statistics
and a frequency distribution saved to the results/ directory.
"""

import json
import math
import os

N = 1_000_000

# ── Sieve of Eratosthenes ──────────────────────────────────────────────────
def sieve(n):
    is_prime = bytearray([1]) * (n + 1)
    is_prime[0] = is_prime[1] = 0
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = bytearray(len(is_prime[i*i::i]))
    return [i for i, v in enumerate(is_prime) if v]

# ── Compute gaps ───────────────────────────────────────────────────────────
primes = sieve(N)
gaps = [primes[i+1] - primes[i] for i in range(len(primes) - 1)]

# ── Summary statistics ─────────────────────────────────────────────────────
n_primes   = len(primes)
n_gaps     = len(gaps)
mean_gap   = sum(gaps) / n_gaps
max_gap    = max(gaps)
max_gap_after = primes[gaps.index(max_gap)]   # prime before the max gap

# Theoretical mean gap ~ ln(N) by Prime Number Theorem
theoretical_mean = math.log(N)

# Frequency distribution of gap sizes
freq = {}
for g in gaps:
    freq[g] = freq.get(g, 0) + 1

# Sort by gap size
freq_sorted = {k: freq[k] for k in sorted(freq)}

# Even-gap proportion (Polignac conjecture: all even gaps appear infinitely)
even_gaps = {k: v for k, v in freq_sorted.items() if k % 2 == 0}
odd_gaps  = {k: v for k, v in freq_sorted.items() if k % 2 != 0}

# Top-10 most common gaps
top10 = sorted(freq.items(), key=lambda x: -x[1])[:10]

summary = {
    "N": N,
    "prime_count": n_primes,
    "gap_count": n_gaps,
    "mean_gap": round(mean_gap, 6),
    "theoretical_mean_ln_N": round(theoretical_mean, 6),
    "relative_error_percent": round(abs(mean_gap - theoretical_mean) / theoretical_mean * 100, 4),
    "max_gap": max_gap,
    "max_gap_after_prime": max_gap_after,
    "distinct_gap_sizes": len(freq),
    "top10_most_common_gaps": [{"gap": g, "count": c} for g, c in top10],
    "odd_gap_sizes": list(odd_gaps.keys()),
}

# ── Write results ──────────────────────────────────────────────────────────
results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(results_dir, exist_ok=True)

with open(os.path.join(results_dir, "summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

with open(os.path.join(results_dir, "gap_frequency.json"), "w") as f:
    json.dump(freq_sorted, f, indent=2)

# Human-readable report
report_lines = [
    "Prime Gap Distribution Analysis",
    "=" * 40,
    f"Range          : 2 to {N:,}",
    f"Primes found   : {n_primes:,}",
    f"Gaps analysed  : {n_gaps:,}",
    "",
    "── Mean Gap ──",
    f"  Observed     : {mean_gap:.6f}",
    f"  ln(N)        : {theoretical_mean:.6f}",
    f"  Rel. error   : {summary['relative_error_percent']:.4f}%",
    "",
    "── Extremes ──",
    f"  Minimum gap  : {min(gaps)} (gap of 1 only between 2 and 3)" if 1 in freq else f"  Minimum gap  : {min(gaps)}",
    f"  Maximum gap  : {max_gap} (after prime {max_gap_after:,})",
    "",
    "── Top 10 Most Common Gaps ──",
]
for gap_val, cnt in top10:
    report_lines.append(f"  Gap {gap_val:>4d} : {cnt:>6,} occurrences")

report_lines += [
    "",
    "── Odd Gaps (anomalies) ──",
    f"  Odd gap sizes observed: {odd_gaps}",
    "  (Only 2→3 can produce gap=1; all other gaps between odd primes are even)",
]

report = "\n".join(report_lines)
print(report)

with open(os.path.join(results_dir, "report.txt"), "w") as f:
    f.write(report + "\n")

print(f"\nResults written to {os.path.abspath(results_dir)}/")
