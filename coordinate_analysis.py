import pandas as pd
import numpy as np

# 嘗試不同編碼碼讀取CSV檔案
encodings_to_try = ['utf-8', 'big5', 'gbk', 'cp950', 'latin1']

for encoding in encodings_to_try:
    try:
        df = pd.read_csv('避難收容處所點位檔案v9.csv', encoding=encoding)
        print(f"成功使用 {encoding} 編碼讀取檔案")
        break
    except Exception as e:
        print(f"使用 {encoding} 編碼失敗: {e}")
        continue
else:
    # 如果所有編碼都失敗，嘗試忽略錯誤
    df = pd.read_csv('避難收容處所點位檔案v9.csv', encoding='utf-8', errors='ignore')
    print("使用 UTF-8 編碼並忽略錯誤讀取檔案")

# 分析經緯度座標
print("=== 座標資料分析報告 ===")
print(f"總資料筆數: {len(df)}")
print(f"經度欄位名稱: {df.columns[4]} ({df.columns[4] in df.columns})")
print(f"緯度欄位名稱: {df.columns[5]} ({df.columns[5] in df.columns})")

# 檢查經緯度資料
longitude_col = df.columns[4]  # 經度
latitude_col = df.columns[5]   # 緯度

# 基本統計
print(f"\n=== 經度 (Longitude) 分析 ===")
print(f"非空值筆數: {df[longitude_col].notna().sum()}")
print(f"空值筆數: {df[longitude_col].isna().sum()}")
if df[longitude_col].notna().sum() > 0:
    print(f"最小值: {df[longitude_col].min()}")
    print(f"最大值: {df[longitude_col].max()}")
    print(f"平均值: {df[longitude_col].mean()}")

print(f"\n=== 緯度 (Latitude) 分析 ===")
print(f"非空值筆數: {df[latitude_col].notna().sum()}")
print(f"空值筆數: {df[latitude_col].isna().sum()}")
if df[latitude_col].notna().sum() > 0:
    print(f"最小值: {df[latitude_col].min()}")
    print(f"最大值: {df[latitude_col].max()}")
    print(f"平均值: {df[latitude_col].mean()}")

# 檢查異常值
print(f"\n=== 異常值檢查 ===")

# 台灣地區合理的經緯度範圍
# 經度: 119-123 (包含金門、馬祖)
# 緯度: 21-26

invalid_longitude = df[(df[longitude_col].notna()) & 
                       ((df[longitude_col] < 119) | (df[longitude_col] > 123))]
print(f"經度異常值筆數: {len(invalid_longitude)}")

invalid_latitude = df[(df[latitude_col].notna()) & 
                     ((df[latitude_col] < 21) | (df[latitude_col] > 26))]
print(f"緯度異常值筆數: {len(invalid_latitude)}")

# 檢查小數點位數
print(f"\n=== 小數點位數分析 ===")
def count_decimal_places(x):
    if pd.isna(x):
        return 0
    s = str(float(x))
    if '.' in s:
        return len(s.split('.')[1].rstrip('0'))
    return 0

longitude_decimals = df[longitude_col].apply(count_decimal_places)
latitude_decimals = df[latitude_col].apply(count_decimal_places)

print("經度小數點位數分布:")
print(longitude_decimals.value_counts().sort_index())
print("\n緯度小數點位數分布:")
print(latitude_decimals.value_counts().sort_index())

# 檢查重複座標
print(f"\n=== 重複座標檢查 ===")
coordinates = df[df[longitude_col].notna() & df[latitude_col].notna()]
duplicates = coordinates[coordinates.duplicated(subset=[longitude_col, latitude_col], keep=False)]
print(f"重複座標筆數: {len(duplicates)}")

# 儲存詳細分析結果
analysis_results = {
    'total_records': len(df),
    'longitude_missing': df[longitude_col].isna().sum(),
    'latitude_missing': df[latitude_col].isna().sum(),
    'invalid_longitude': len(invalid_longitude),
    'invalid_latitude': len(invalid_latitude),
    'duplicate_coordinates': len(duplicates),
    'longitude_decimal_places': longitude_decimals.value_counts().to_dict(),
    'latitude_decimal_places': latitude_decimals.value_counts().to_dict()
}

print(f"\n=== 分析完成 ===")
print("詳細結果已儲存至 analysis_results 變數")