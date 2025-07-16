import re
import matplotlib.pyplot as plt
import numpy as np
import csv
import os

# Customize this with your log file paths and model labels
log_files = {
    #"u2net": "/home/ultron/Desktop/results_benchmarks/u2net_benchmark_100_steps.txt",
    #"seanet": "/home/ultron/Desktop/results_benchmarks/seanet_benchmark_100_steps.txt",
    #"samnet": "/home/ultron/Desktop/results_benchmarks/samnet_benchmark_100_steps.txt",
    #"hvpnet": "/home/ultron/Desktop/results_benchmarks/hvpnet_benchmark_100_steps.txt",
    "bofp1": "/home/ultron/Desktop/results_benchmarks/bofp1_benchmark_100_steps.txt",
    "bofp2": "/home/ultron/Desktop/results_benchmarks/bofp2_benchmark_100_steps.txt",
    "bofp3": "/home/ultron/Desktop/results_benchmarks/bofp3_benchmark_100_steps.txt",
    "cluster1": "/home/ultron/Desktop/results_benchmarks/cluster1_benchmark_100_steps.txt",
    "cluster2": "/home/ultron/Desktop/results_benchmarks/cluster2_benchmark_100_steps.txt",
    "cluster3": "/home/ultron/Desktop/results_benchmarks/cluster3_benchmark_100_steps.txt",
}

model_data = {}
model_stats = []

pattern = r"Inference time = (\d+) ms"

for model_name, file_path in log_files.items():
    inference_times = []

    if not os.path.isfile(file_path):
        print(f" Log file not found: {file_path}")
        continue

    with open(file_path, "r") as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                inference_times.append(int(match.group(1)))

    if inference_times:
        model_data[model_name] = inference_times
        arr = np.array(inference_times)

        stats = {
            "Model": model_name,
            "Avg (ms)": np.mean(arr),
            "Std Dev (ms)": np.std(arr),
            "Min (ms)": np.min(arr),
            "Max (ms)": np.max(arr),
            "Runs": len(arr)
        }

        model_stats.append(stats)

      

# Plot cumulative inference times
plt.figure(figsize=(9, 5))

for model_name, times in model_data.items():
    cumulative = np.cumsum(times)
    plt.plot(cumulative, label=model_name)

plt.title("Cumulative Inference Time Comparison")
plt.xlabel("Run")
plt.ylabel("Cumulative Time (ms)")
plt.legend(loc="upper left")
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("cumulative_inference_comparison.png", dpi=300)

