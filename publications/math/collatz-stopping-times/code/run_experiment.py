"""
Collatz Stopping Time Distribution up to N = 1,000,000
Computes total stopping times and produces summary statistics.
"""

import json
import math
from collections import Counter

N = 1_000_000


def collatz_stopping_time(n: int) -> int:
    """Return the total stopping time of n (steps to reach 1)."""
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps


def main():
    print(f"Computing Collatz stopping times for n = 2 to {N:,}...")

    stopping_times = []
    for n in range(2, N + 1):
        stopping_times.append(collatz_stopping_time(n))

    # Summary statistics
    total = len(stopping_times)
    mean_st = sum(stopping_times) / total
    min_st = min(stopping_times)
    max_st = max(stopping_times)
    max_n = stopping_times.index(max_st) + 2  # offset: index 0 = n=2

    sorted_st = sorted(stopping_times)
    median_st = sorted_st[total // 2]

    # Variance and std dev
    variance = sum((x - mean_st) ** 2 for x in stopping_times) / total
    std_dev = math.sqrt(variance)

    # Frequency distribution (histogram with bin width 10)
    freq = Counter(stopping_times)
    bin_width = 10
    histogram = {}
    for st, count in freq.items():
        bin_label = (st // bin_width) * bin_width
        histogram[bin_label] = histogram.get(bin_label, 0) + count
    histogram = {str(k): v for k, v in sorted(histogram.items(), key=lambda x: int(x[0]))}

    # Top 10 most common stopping times
    top10 = sorted(freq.items(), key=lambda x: -x[1])[:10]
    top10_serializable = [[int(st), int(cnt)] for st, cnt in top10]

    summary = {
        "N": N,
        "count": total,
        "min_stopping_time": int(min_st),
        "max_stopping_time": int(max_st),
        "n_with_max_stopping_time": int(max_n),
        "mean_stopping_time": round(mean_st, 6),
        "median_stopping_time": int(median_st),
        "std_dev_stopping_time": round(std_dev, 6),
        "distinct_stopping_times": len(freq),
    }

    results_dir = "results"
    import os
    os.makedirs(results_dir, exist_ok=True)

    with open(f"{results_dir}/summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    with open(f"{results_dir}/histogram.json", "w") as f:
        json.dump(histogram, f, indent=2)

    with open(f"{results_dir}/top10_stopping_times.json", "w") as f:
        json.dump(top10_serializable, f, indent=2)

    # Human-readable report
    with open(f"{results_dir}/report.txt", "w") as f:
        f.write("Collatz Stopping Time Report\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Range analyzed: 2 to {N:,}\n")
        f.write(f"Total values:   {total:,}\n\n")
        f.write(f"Min stopping time: {min_st}\n")
        f.write(f"Max stopping time: {max_st}  (n = {max_n:,})\n")
        f.write(f"Mean stopping time: {mean_st:.6f}\n")
        f.write(f"Median stopping time: {median_st}\n")
        f.write(f"Std deviation: {std_dev:.6f}\n")
        f.write(f"Distinct stopping times: {len(freq)}\n\n")
        f.write("Top 10 most common stopping times:\n")
        for st, cnt in top10:
            pct = 100 * cnt / total
            f.write(f"  {st:>4}: {cnt:>7,} occurrences ({pct:.2f}%)\n")

    print("Done. Results written to results/")
    print(f"  Max stopping time: {max_st} at n={max_n:,}")
    print(f"  Mean stopping time: {mean_st:.4f}")


if __name__ == "__main__":
    main()
