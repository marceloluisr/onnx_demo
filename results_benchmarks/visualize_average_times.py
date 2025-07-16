import csv
import matplotlib.pyplot as plt

# Load and sort data from CSV
file_path = "/home/ultron/Desktop/results_benchmarks/model_stats.csv"
records = []

with open(file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        records.append({
            "Model": row["Model"],
            "Avg (ms)": float(row["Avg (ms)"])
        })

# Sort by Avg (ms) ascending or descending
records.sort(key=lambda x: x["Avg (ms)"])  # ascending
# records.sort(key=lambda x: x["Avg (ms)"], reverse=True)  # descending

# Prepare data
models = [r["Model"] for r in records]
avg_times = [r["Avg (ms)"] for r in records]

# Plot sorted bar chart
plt.figure(figsize=(8, 5))
bars = plt.bar(models, avg_times, color='lightcoral', edgecolor='black')

# Label bars with value
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 5, f"{height:.1f}", ha='center', fontsize=9)

plt.title("Sorted Average Inference Time per Model")
plt.xlabel("Model")
plt.ylabel("Average Time (ms)")
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

# Save sorted plot
plt.savefig("sorted_avg_inference_barplot.png", dpi=300)
# plt.show()

