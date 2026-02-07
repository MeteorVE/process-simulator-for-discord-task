
# Process Simulator

這是一個用於模擬多個遊戲客戶端進程啟動與關閉的工具。主控端 (Main) 可以編譯、部署並管理多個 Client (模擬的遊戲執行檔)。

**此專案僅用於解 discord orb 任務。**

## 注意事項（重要）
- 本工具為 Windows-only：Client 使用 `msvcrt`，主控端使用 `taskkill` 與 `CREATE_NEW_CONSOLE`。
- `build_clients.py` 會把編譯出的 `client.exe` 複製/覆寫到 `config.py` 設定的 `GAME_PATHS` 位置。
- 若 `GAME_PATHS` 位於系統保護目錄（例如 `C:\Program Files`），執行時可能需要以系統管理員身分運行。
- 公開/分享程式碼時，請勿把 `build/`、`dist/`、`__pycache__/` 等產物一起上傳。

## 功能
- **自動部署**：自動編譯 Client 並複製到指定的遊戲路徑 (`config.py`)。
- **批量啟動**：一鍵開啟所有設定好的遊戲執行檔。
- **即時監控**：GUI 顯示目前連線的 Client 及其 PID。
- **一鍵關閉**：主控端按下空白鍵或關閉視窗，會自動終止所有相關 Client (包含強力刪除殘留進程)。

## 使用方式

### 1. 安裝依賴
確認已安裝 Python，並執行：
```bash
pip install -r requirements.txt
```

### 2. 設定路徑
修改 `config.py`，填入你希望模擬的遊戲執行檔路徑：
```python
GAME_PATHS = [
    r"C:\Path\To\Game1.exe",
    r"C:\Path\To\Game2.exe",
    # ...
]
```
**注意**：`build_clients.py` 會將 `client.exe` 複製到上述路徑（可能覆寫原檔）。若路徑位於系統保護目錄 (如 `C:\Program Files`)，執行時可能需要以 **系統管理員身分** 運行。

### 3. 執行
以系統管理員身分執行 Command Prompt 或 PowerShell，然後輸入：
```bash
python main.py
```

## 操作說明
- **Main 視窗**：
  - 點擊「啟動 Clients」：開始部署與啟動。
  - 按下「空白鍵」或關閉視窗：強制結束所有 Client。
- **Client 視窗**：
  - 每個 Client 會模擬執行 16 分鐘後自動結束。
  - 按下空白鍵可手動結束單一 Client。

## 分發給他人
若要將此工具分享給朋友，請打包以下檔案：
1. `main.py` (主控端程式)
2. `build_clients.py` (編譯與部署腳本)
3. `client.py` (Client 原始碼)
4. `config.py` (設定檔，請朋友修改為自己的路徑)
5. `requirements.txt` (依賴清單)
6. `README.md` (本說明文件)

**不需要打包**：
- `build/`, `dist/`, `__pycache__/` 資料夾 (會自動生成)
- `client.spec`
