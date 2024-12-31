import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np

# 假設每組的檔案列表
file_groups = [
    ["smallbank-mpt-1000k-fan4-ratio4-mem64-ts.json", "smallbank-cole_star-1000k-fan4-ratio4-mem450000-ts.json", "smallbank-cole-1000k-fan4-ratio4-mem450000-ts.json"],  # 第一組對應 10^4
    ["smallbank-mpt-10000k-fan4-ratio4-mem64-ts.json", "smallbank-cole_star-10000k-fan4-ratio4-mem450000-ts.json", "smallbank-cole-10000k-fan4-ratio4-mem450000-ts.json"]   # 第二組對應 10^5
]
labels = ["$10^4$", "$10^5$"]  # Block Height 標籤
methods = ["MPT", "COLE", "COLE*"]  # 方法名稱
colors = ["purple", "green", "blue"]  # 方法對應的顏色

# 儲存延遲數據
latency_data = []

# 逐組讀取檔案
for files in file_groups:
    for file in files:
        with open(file, "r") as f:
            data = [json.loads(line) for line in f]  # 每行讀取 JSON
        df = pd.DataFrame(data)  # 轉換為 DataFrame
        df["latency_ms"] = df["elapse"] / 1_000_000  # 奈秒轉毫秒
        latency_data.append(df["latency_ms"])  # 儲存每個方法的延遲數據

# 準備繪製位置
positions = []
group_offset = len(methods) + 1  # 每組方法間的間隔
for i in range(len(file_groups)):  # 每個區塊高度
    base = i * group_offset  # 每組的基礎位置
    for j in range(len(methods)):  # 每個方法的位置
        positions.append(base + j + 1)

# 計算 x 軸標籤位置
xtick_positions = [
    (positions[len(methods) * i] + positions[len(methods) * i + len(methods) - 1]) / 2
    for i in range(len(file_groups))
]

# 建立圖表
plt.figure(figsize=(8, 6))
boxprops = plt.boxplot(
    latency_data,
    positions=positions,
    widths=0.6,
    patch_artist=True,
)

# 上色
for patch, color in zip(boxprops["boxes"], colors * len(file_groups)):
    patch.set_facecolor(color)

# 設置軸標籤和刻度
plt.xticks(xtick_positions, labels)  # 設置 Block Height 標籤位置
plt.yscale("log")  # 設置對數刻度
plt.ylabel("Latency (ms)")
plt.xlabel("Block Height (SmallBank)")

# 添加圖例
handles = [plt.Line2D([0], [0], color=color, lw=4) for color in colors]
plt.legend(handles, methods, title="Methods", loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=3)

# 顯示圖表
plt.tight_layout()
plt.show()

