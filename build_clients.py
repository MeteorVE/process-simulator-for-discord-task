# build_clients.py
import subprocess
import shutil
from pathlib import Path
import sys

CLIENT_COUNT = 5
ROOT = Path(__file__).parent
DIST = ROOT / "dist"
CLIENTS_DIR = ROOT / "clients"


try:
    from config import GAME_PATHS
except ImportError:
    # If users forget or config.py is missing, define it locally or raise error
    GAME_PATHS = []
    print("【Builder】Warning: config.py not found or GAME_PATHS missing.")

def main():
    print("【Builder】開始編譯 client.exe")

    # Check if we have admin rights? Maybe not needed if user runs as admin.
    
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pyinstaller",      # ← 關鍵：全小寫
            "--onefile",
            "--clean",
            "client.py"
        ],
        cwd=ROOT,              # ← 保險起見，指定工作目錄
        check=True
    )

    exe = DIST / "client.exe"
    if not exe.exists():
        raise RuntimeError("client.exe 編譯失敗，找不到 dist/client.exe")

    if not GAME_PATHS:
        print("【Builder】沒有設定 GAME_PATHS，請檢查 config.py")
        return

    for path_str in GAME_PATHS:
        target_path = Path(path_str)
        
        # Ensure parent directory exists
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            print(f"【Builder】權限不足無法建立目錄: {target_path.parent}")
            continue
        except Exception as e:
            print(f"【Builder】建立目錄失敗: {e}")
            continue

        try:
            shutil.copy(exe, target_path)
            print(f"【Builder】已複製到: {target_path}")
        except PermissionError:
            print(f"【Builder】權限不足無法寫入: {target_path}")
        except Exception as e:
            print(f"【Builder】複製失敗: {e}")

    print("【Builder】完成")

if __name__ == "__main__":
    main()
