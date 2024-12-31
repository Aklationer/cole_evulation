import matplotlib.pyplot as plt
import json
import os

# 手動輸入檔案名稱和對應標籤
files = {
    "$10^4$": {
        "MPT": "readwriteeven-mpt-1000k-fan4-ratio4-mem64-ts.json",
        "COLE": "readwriteeven-cole-1000k-fan4-ratio4-mem450000-ts.json",
        "COLE*": "readwriteeven-cole_star-1000k-fan4-ratio4-mem450000-ts.json",
    },
    "$10^5$": {
        "MPT": "readwriteeven-mpt-10000k-fan4-ratio4-mem64-ts.json",
        "COLE": "readwriteeven-cole-10000k-fan4-ratio4-mem450000-ts.json",
        "COLE*": "readwriteeven-cole_star-10000k-fan4-ratio4-mem450000-ts.json",
    },
}

# 資料目錄
directory = "./"

# 讀取數據的函數
def read_data(file_path):
    with open(file_path, "r") as f:
        data = [json.loads(line) for line in f]  # 每行解析 JSON
    elapse_values = [entry["elapse"] / 1_000_000 for entry in data]  # 轉換為 ms
    return elapse_values

# 收集所有檔案的數據
boxplot_data = {}
for block_height, methods in files.items():
    boxplot_data[block_height] = {}
    for method, file_name in methods.items():
        file_path = os.path.join(directory, file_name)
        boxplot_data[block_height][method] = read_data(file_path)

# 繪製 Box Plot
def plot_boxplot(boxplot_data):
    block_heights = list(boxplot_data.keys())  # 提取區塊高度
    methods = list(next(iter(boxplot_data.values())).keys())  # 提取方法名稱

    # 準備 Box Plot 數據
    plot_data = []
    colors = {"MPT": "purple", "COLE": "green", "COLE*": "blue"}  # 顏色對應
    positions = []
    group_centers = []
    labels = []
    pos_offset = 0

    # 將數據組織為 Box Plot 格式
    for block_height in block_heights:
        group_start = pos_offset
        for method in methods:
            plot_data.append(boxplot_data[block_height][method])
            positions.append(pos_offset)
            pos_offset += 1
        group_centers.append((group_start + pos_offset - 1) / 2)  # 計算組中心
        labels.append(block_height)  # 添加區塊高度標籤

    # 繪製 Box Plot
    plt.figure(figsize=(10, 6))
    boxprops = dict(linestyle='-', linewidth=1.5, color='black')
    medianprops = dict(linestyle='-', linewidth=2, color='red')
    bplot = plt.boxplot(
        plot_data,
        positions=positions,
        patch_artist=True,
        boxprops=boxprops,
        medianprops=medianprops,
    )

    # 填充 Box 顏色
    for patch, method in zip(bplot['boxes'], methods * len(block_heights)):
        patch.set_facecolor(colors[method])

    # 添加圖例
    legend_handles = [
        plt.Line2D([0], [0], color=color, lw=4, label=method)
        for method, color in colors.items()
    ]
    plt.legend(
        handles=legend_handles,
        title="Methods",
        loc="lower center",
        bbox_to_anchor=(0.5, -0.2),
        ncol=3,
        frameon=True,
    )

    # 設置 x 軸標籤（標籤放置在每組數據中心）
    plt.xticks(group_centers, labels)
    plt.yscale("log")  # y 軸對數刻度
    plt.xlabel("Block Height (KVStore)")
    plt.ylabel("Latency (ms)")
    plt.grid(axis="y", linestyle="--", linewidth=0.5)

    # 顯示圖表
    plt.tight_layout()
    plt.show()

# 繪製 Box Plot
plot_boxplot(boxplot_data)

