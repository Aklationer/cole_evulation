import os
import json
import matplotlib.pyplot as plt
import re

def calculate_elapsed(directory):
    elapsed_times = {}
    
    # 確認資料夾存在
    if not os.path.exists(directory):
        print(f"資料夾 {directory} 不存在！")
        return elapsed_times

    # 遍歷資料夾中的檔案
    for filename in os.listdir(directory):
        if filename.endswith(".json"):  # 僅處理 JSON 檔案
            file_path = os.path.join(directory, filename)
            total_elapsed = 0
            
            # 逐行讀取 JSON
            try:
                with open(file_path, "r") as file:
                    for line in file:
                        data = json.loads(line.strip())  # 解析每行為 JSON 格式
                        total_elapsed += data.get("elapse", 0)  # 累加 `elapse`
                # 提取記憶體大小和基準名稱
                match = re.match(r"(\d+G)-([a-zA-Z0-9_]+)-", filename)
                if match:
                    key = f"{match.group(1)}-{match.group(2)}"
                else:
                    key = filename  # 無法匹配時，使用完整檔案名
                elapsed_times[key] = total_elapsed
            except Exception as e:
                print(f"處理檔案 {filename} 時發生錯誤：{e}")

    return elapsed_times

# 設定資料夾路徑
directory = "./"  # 替換成你的資料夾路徑

# 計算各檔案的 `elapsed` 總和
result = calculate_elapsed(directory)

# 如果有結果，繪製條形圖
if result:
    filenames = list(result.keys())
    elapsed_times = list(result.values())
    
    # 繪製條形圖
    plt.figure(figsize=(10, 6))
    plt.bar(filenames, elapsed_times, alpha=0.7, color='skyblue')
    plt.title("Elapsed Time by Memory Size and Benchmark", fontsize=14)
    plt.xlabel("Memory Size and Benchmark", fontsize=12)
    plt.ylabel("Elapsed Time", fontsize=12)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.tight_layout()

    # 顯示圖表
    plt.show()
else:
    print("未找到任何 JSON 檔案或所有檔案處理失敗！")
