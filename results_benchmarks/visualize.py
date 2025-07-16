import re
import matplotlib.pyplot as plt
import numpy as np

# Load and parse log file
log_path = "/home/ultron/Desktop/results_benchmarks/u2net_benchmark_100_steps.txt"
pattern = r"Inference time = (\d+) ms"
inference_times = []

with open(log_path, "r") as file:
    for line in file:
        match = re.search(pattern, line)
        if match:
            inference_times.append(int(match.group(1)))

# 

# Compute statistics
times_array = np.array(inference_times)
avg = np.mean(times_array)
std_dev = np.std(times_array)
min_time = np.min(times_array)
max_time = np.max(times_array)



# 📊 Plot setup
plt.figure(figsize=(6, 4))  # Good paper size (approx 15cm x 10cm)
plt.plot(inference_times, marker='o', linestyle='-', color='royalblue')
plt.title("Model Inference Time per Run")
plt.xlabel("Run")
plt.ylabel("Inference Time (ms)")
plt.grid(True)

# Annotate stats
stats_text = f"Avg: {avg:.2f} ms | Std Dev: {std_dev:.2f} ms\nMin: {min_time} ms | Max: {max_time} ms"
plt.figtext(0.5, 0.01, stats_text, ha="center", fontsize=10, bbox={"facecolor": "lightgray", "alpha":0.5, "pad":5})

plt.tight_layout()

# 🖼 Save with high DPI
plt.savefig("inference_plot.png", dpi=300)

# Optional: show plot while testing
# plt.show()

