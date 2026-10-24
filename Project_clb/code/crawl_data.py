
import requests
import pandas as pd

# 1. Khai báo URL API
url = "https://archive-api.open-meteo.com/v1/archive"

# 2. Các tham số truy vấn
params = {
    "latitude": 21.0285,
    "longitude": 105.8542,
    "start_date": "2015-01-01",
    "end_date": "2025-12-31",
    "daily": [
        "temperature_2m_mean",
        "relative_humidity_2m_mean",
        "pressure_msl_mean",
        "wind_speed_10m_max",
        "cloud_cover_mean",
        "precipitation_sum"
    ],
    "timezone": "Asia/Bangkok"
}

# 3. Gửi yêu cầu đến API
response = requests.get(url, params=params, timeout=30)
response.raise_for_status()

# 4. Chuyển phản hồi JSON thành DataFrame
data = response.json()
df = pd.DataFrame(data["daily"])

# 5. Đổi tên cột cho dễ đọc
df = df.rename(columns={
    "time": "date",
    "temperature_2m_mean": "temperature",
    "relative_humidity_2m_mean": "humidity",
    "pressure_msl_mean": "pressure",
    "wind_speed_10m_max": "wind_speed",
    "cloud_cover_mean": "cloud_cover",
    "precipitation_sum": "precipitation"
})

# 6. Xử lý dữ liệu thiếu
feature_cols = [
    "temperature", "humidity", "pressure",
    "wind_speed", "cloud_cover", "precipitation"
]
df[feature_cols] = df[feature_cols].apply(
    pd.to_numeric, errors="coerce"
)

df = df.dropna(subset=feature_cols)

# 7. Lưu thành CSV
df.to_csv("hanoi_weather.csv", index=False)

print(df.head())
print("Kích thước dữ liệu:", df.shape)
print("Đã lưu file hanoi_weather.csv")
