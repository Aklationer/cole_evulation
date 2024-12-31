import matplotlib.pyplot as plt
import numpy as np

# 數據
block_sizes = ["$10^1$", "$10^2$", "$10^3$", "$10^4$", "$10^5$"]  # 區塊大小（x 軸標籤）
indexes = ["MPT", "LIPP", "CMI", "COLE", "COLE*"]  # 索引方法
storage_data = [
    [405232, 7411853, 113951792, 1544608262, 19965233586],  # MPT
    [1622254, 34675210, 9999999999999, 9999999999999, 9999999999999],  # LIPP
    [635412, 9871084, 131518424, 1818835939, 1818835939],   # CMI
    [154844, 1583148, 15789156, 126538962, 1179840783],     # COLE
    [154880, 1583184, 15789192, 239229949, 1652310313]      # COLE*
]

# 將 storage_data 轉換為 MB
storage_data_mb = [[value / 1_000_000 for value in row] for row in storage_data]

# 設置條形圖參數
x = np.arange(len(block_sizes))  # x 軸位置
bar_width = 0.2  # 每個條形的寬度
hatch_patterns = ["/", "\\", "x", "-", "|"]  # 圖案樣式列表

# 建立圖表
plt.figure(figsize=(10, 6))

# 為每個索引方法繪製條形
for i, (index, storage) in enumerate(zip(indexes, storage_data_mb)):
    plt.bar(
        x + i * bar_width,  # 條形位置
        storage,  # 條形高度
        bar_width,  # 條形寬度
        label=index,  # 標籤
        hatch=hatch_patterns[i % len(hatch_patterns)],  # 設置圖案
        edgecolor="black"  # 條形邊框顏色
    )

# 設置 x 軸標籤
plt.xticks(x + bar_width * (len(indexes) - 1) / 2, block_sizes)
plt.yscale("log")  # y 軸對數刻度
plt.xlabel("Block Height")
plt.ylabel("Storage Size (MB)")
plt.title("Storage Size vs. Block Height")

# 添加圖例
plt.legend(title="Indexes", loc="upper left")

# 美化圖表
plt.grid(axis="y", linestyle="--", linewidth=0.5)
plt.tight_layout()

# 顯示圖表
plt.show()

