# iot-attendance

## 專案介紹

本專案為配合 ESP32 的 RFID 所開發的專案。此專案旨在提供一個高效能且易於使用的前後端服務，用於管理和記錄打卡數據。

## 安裝與使用

### 環境需求

- Python 3.12.7
- Poetry

### 安裝步驟

#### backend
```bash
    cd iot-attendance/backend
    poetry shell
    poetry install
```

#### frontend
```bash
    cd iot-attendance/frontend
    npm i
```
### 啟動專案

#### backend

1. 啟動 FastAPI 伺服器：
    ```sh
    python main.py
    ```

2. 伺服器啟動後，可透過以下網址訪問 API 文件（若啟用）：
    - Swagger UI: `http://localhost:8000/docs`
    - ReDoc: `http://localhost:8000/redoc`

#### frontend
1.須先前往 package.json 找到 script start 設定將內容修改成自己本地的檔案路徑
```bash
# pwd 指令列出當前路徑並進行替換
"scripts": {
    "start": "node-red --userDir /Users/hongchengxi/Documents/iot/iot-attendance/frontend"
},
```
2.替換完成後則可運行啟動
```bash
npm run start
```

## 主要功能

- 使用者管理
- 打卡記錄
- 每日摘要
- 權限管理
