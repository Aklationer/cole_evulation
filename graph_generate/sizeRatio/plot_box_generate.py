import matplotlib.pyplot as plt
import json

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

# 資料目錄路徑
directory = "./"

# 修正的數據讀取函數
def read_data(file_path):
    data = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                json_data = json.loads(line)  # 每行解析為 JSON
                elapse_ms = json_data["elapse"] / 1_000_000  # 將 elapse 轉換為毫秒
                data.append(elapse_ms)
    return data

# 整理數據
size_ratios = sorted(files.keys())  # 獲取所有 Size Ratio
cole_data = []       # COLE 數據
cole_star_data = []  # COLE* 數據

# 從檔案中讀取數據
for ratio in size_ratios:
    cole_file = f"{directory}/{files[ratio]['cole']}"
    cole_star_file = f"{directory}/{files[ratio]['cole_star']}"
    cole_data.append(read_data(cole_file))
    cole_star_data.append(read_data(cole_star_file))

# 合併數據為繪圖所需格式
all_data = []
for cole, cole_star in zip(cole_data, cole_star_data):
    all_data.append(cole)        # COLE 的數據
    all_data.append(cole_star)   # COLE* 的數據

# 設置 Box Plot 的位置
positions = []
group_offset = 2  # 每組 COLE 和 COLE* 的間距
for i in range(len(size_ratios)):
    base = i * group_offset * 2
    positions.append(base + 1)  # COLE 的位置
    positions.append(base + 2)  # COLE* 的位置

# 繪製 Box Plot
plt.figure(figsize=(10, 6))
boxprops = plt.boxplot(
    all_data,
    positions=positions,
    patch_artist=True,
    widths=0.6,
)

# 設置顏色
colors = ["purple", "green"]  # COLE 和 COLE* 的顏色
for patch, color in zip(boxprops["boxes"], colors * len(size_ratios)):
    patch.set_facecolor(color)

# 設置 x 軸標籤和位置
xtick_positions = [(positions[i * 2] + positions[i * 2 + 1]) / 2 for i in range(len(size_ratios))]
plt.xticks(xtick_positions, size_ratios)
plt.xlabel("Size Ratio")
plt.ylabel("Latency (ms)")
plt.yscale("log")  # 設置對數刻度

# 添加圖例
handles = [plt.Line2D([0], [0], color=color, lw=4) for color in colors]
plt.legend(handles, ["COLE", "COLE*"], title="Methods", loc="upper right")

# 顯示圖表
plt.grid(axis="y", linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.show()

