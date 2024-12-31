import matplotlib.pyplot as plt
import json
import os
import numpy as np

# 手動輸入檔案名稱
files = {
    2: {"cole": "size_ratio-cole-10000k-fan4-ratio2-mem450000-ts.json",
        "cole_star": "size_ratio-cole_star-10000k-fan4-ratio2-mem450000-ts.json"},
    4: {"cole": "size_ratio-cole-10000k-fan4-ratio4-mem450000-ts.json",
        "cole_star": "size_ratio-cole_star-10000k-fan4-ratio4-mem450000-ts.json"},
    6: {"cole": "size_ratio-cole-10000k-fan4-ratio6-mem450000-ts.json",
        "cole_star": "size_ratio-cole_star-10000k-fan4-ratio6-mem450000-ts.json"},
    8: {"cole": "size_ratio-cole-10000k-fan4-ratio8-mem450000-ts.json",
        "cole_star": "size_ratio-cole_star-10000k-fan4-ratio8-mem450000-ts.json"},
    10: {"cole": "size_ratio-cole-10000k-fan4-ratio10-mem450000-ts.json",
         "cole_star": "size_ratio-cole_star-10000k-fan4-ratio10-mem450000-ts.json"},
    12: {"cole": "size_ratio-cole-10000k-fan4-ratio12-mem450000-ts.json",
         "cole_star": "size_ratio-cole_star-10000k-fan4-ratio12-mem450000-ts.json"},
    14: {"cole": "size_ratio-cole-10000k-fan4-ratio14-mem450000-ts.json",
         "cole_star": "size_ratio-cole_star-10000k-fan4-ratio14-mem450000-ts.json"},
}

# 資料目錄
directory = "./"

# 計算 Throughput 的函數
def calculate_throughput(file_path):
    with open(file_path, "r") as f:
        data = [json.loads(line) for line in f]  # 每行解析 JSON

    # 計算總時間和 Throughput
    total_elapse = sum(item["elapse"] for item in data) / 1_000_000  # 總花費時間 (秒)
    block_count = len(data)  # 區塊數量
    throughput_tps = block_count / total_elapse *1000 # Throughput (TPS)
    return throughput_tps

# 計算所有檔案的 Throughput
throughput_data = {}
for size_ratio, methods in files.items():
    throughput_data[size_ratio] = {}
    for method, file_name in methods.items():
        file_path = os.path.join(directory, file_name)
        throughput_data[size_ratio][method] = calculate_throughput(file_path)

# 繪製圖表
def plot_throughput(throughput_data):
    size_ratios = sorted(throughput_data.keys())  # 按 size_ratio 排序
    methods = list(next(iter(throughput_data.values())).keys())  # 提取方法名稱
    x = range(len(size_ratios))  # x 軸位置
    bar_width = 0.3  # 每個條形的寬度
    hatch_patterns = ["x", "/"]  # 圖案樣式

    plt.figure(figsize=(10, 6))

    # 繪製條形圖
    for i, method in enumerate(methods):
        throughput_values = [throughput_data[size_ratio][method] for size_ratio in size_ratios]
        plt.bar(
            [pos + i * bar_width for pos in x],
            throughput_values,
            bar_width,
            label=method.replace("_", "*"),
            hatch=hatch_patterns[i % len(hatch_patterns)],  # 設置圖案
            edgecolor="black"
        )

    # 設置圖表屬性
    plt.xticks([pos + (len(methods) - 1) * bar_width / 2 for pos in x], size_ratios)
    plt.yscale("log")  # y 軸對數刻度
    plt.xlabel("Size Ratio")
    plt.ylabel("Throughput (TPS)")
    plt.legend(title="Methods", loc="upper right")
    plt.grid(axis="y", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()

# 繪製圖表
plot_throughput(throughput_data)

