# iot-attendance

## 專案介紹

本專案為配合 ESP32 的 RFID 以及 Node-RED 所開發的 FastAPI 後端專案。此專案旨在提供一個高效能且易於使用的後端服務，用於管理和記錄打卡數據。

## 安裝與使用

### 環境需求

- Python 3.12.7
- Poetry

### 安裝步驟

1. 克隆此專案到本地端：
    ```sh
    git clone <repository-url>
    ```
2. 進入專案目錄：
    ```sh
    cd iot-attendance
    ```
3. 使用 Poetry 安裝依賴：
    ```sh
    poetry install
    ```

### 啟動專案

1. 啟動 FastAPI 伺服器：
    ```sh
    python main.py
    ```

2. 伺服器啟動後，可透過以下網址訪問 API 文件（若啟用）：
    - Swagger UI: `http://localhost:8000/docs`
    - ReDoc: `http://localhost:8000/redoc`

## 主要功能

- 使用者管理
- 打卡記錄
- 每日摘要
- 權限管理
