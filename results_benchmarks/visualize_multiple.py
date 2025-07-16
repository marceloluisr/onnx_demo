import re
import matplotlib.pyplot as plt
import numpy as np
import csv
import os

#  Customize this with your log file paths and model labels
log_files = {
    "u2net": "/home/ultron/Desktop/results_benchmarks/u2net_benchmark_100_steps.txt",
    "seanet": "/home/ultron/Desktop/results_benchmarks/seanet_benchmark_100_steps.txt",
    "samnet": "/home/ultron/Desktop/results_benchmarks/samnet_benchmark_100_steps.txt",
    "hvpnet": "/home/ultron/Desktop/results_benchmarks/hvpnet_benchmark_100_steps.txt",
    "bofp1": "/home/ultron/Desktop/results_benchmarks/bofp1_benchmark_100_steps.txt",
    "bofp2": "/home/ultron/Desktop/results_benchmarks/bofp2_benchmark_100_steps.txt",
    "bofp3": "/home/ultron/Desktop/results_benchmarks/bofp3_benchmark_100_steps.txt",
    "cluster1": "/home/ultron/Desktop/results_benchmarks/cluster1_benchmark_100_steps.txt",
    "cluster2": "/home/ultron/Desktop/results_benchmarks/cluster2_benchmark_100_steps.txt",
    "cluster3": "/home/ultron/Desktop/results_benchmarks/cluster3_benchmark_100_steps.txt",
    
}

# Store all model data and stats
model_data = {}
model_stats = []

# Regex to extract inference time lines
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

        # Compute statistics
        times_array = np.array(inference_times)
        stats = {
            "Model": model_name,
            "Avg (ms)": np.mean(times_array),
            "Std Dev (ms)": np.std(times_array),
            "Min (ms)": np.min(times_array),
            "Max (ms)": np.max(times_array),
            "Runs": len(inference_times)
        }

        model_stats.append(stats)

        # 📢 Show stats in console
        print(f"\n📊 Stats for {model_name}")
        for k, v in stats.items():
            print(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}")

# 📈 Plot all models
plt.figure(figsize=(8, 5))
for model_name, times in model_data.items():
    plt.plot(
    	times, 
    	label=model_name, 
    	#marker='o', 
    	linestyle='-'
    )

plt.title("Inference Time Comparison Across Models")
plt.xlabel("Run")
plt.ylabel("Inference Time (ms)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save high-resolution plot
plt.savefig("inference_comparison.png", dpi=300)
# plt.show()  # Uncomment to view the plot

# Save stats to CSV
with open("model_stats.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=model_stats[0].keys())
    writer.writeheader()
    writer.writerows(model_stats)

