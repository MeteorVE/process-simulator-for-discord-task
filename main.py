# main.py
import socket
import threading
import subprocess
import time
from pathlib import Path
import tkinter as tk
from tkinter import ttk

ROOT = Path(__file__).parent
CLIENTS_DIR = ROOT / "clients"
PORT = 5050

clients = {}
running = True


def handle_client(conn):
    global clients
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode()
            if msg.startswith("HELLO"):
                # HELLO:Name:PID
                parts = msg.split(":")
                name = parts[1]
                pid = int(parts[2]) if len(parts) > 2 else 0
                
                print(f"【Main】收到連線: {name} (PID: {pid})")
                
                clients[name] = {"conn": conn, "pid": pid}
                update_list()
            elif msg.startswith("EXIT"):
                name = msg.split(":")[1]
                clients.pop(name, None)
                update_list()
                break
        except Exception as e:
            # print(f"【Debug】Connection Error: {e}")
            break

def server():
    s = socket.socket()
    s.bind(("127.0.0.1", PORT))
    s.listen()
    while running:
        conn, _ = s.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

try:
    from config import GAME_PATHS
except ImportError:
    GAME_PATHS = []

launched_processes = []

def build_and_launch():
    # Check if all game paths exist
    missing = [path for path in GAME_PATHS if not Path(path).exists()]
    
    if missing:
        print(f"【Main】發現缺少的執行檔，開始重新編譯與部署...")
        subprocess.run(["python", "build_clients.py"], check=True)
    
    if not GAME_PATHS:
         print("【Main】沒有設定 GAME_PATHS，無法啟動")
         return

    for path_str in GAME_PATHS:
        exe = Path(path_str)
        if exe.exists():
            print(f"【Main】啟動: {exe}")
            try:
                proc = subprocess.Popen([str(exe)], cwd=exe.parent, creationflags=subprocess.CREATE_NEW_CONSOLE)
                launched_processes.append(proc)
            except Exception as e:
                print(f"【Main】啟動失敗 {exe}: {e}")
            time.sleep(0.2)
        else:
            print(f"【Main】找不到檔案: {exe}")

def kill_all():
    global running
    print("【Main】正在關閉所有 Clients...")
    
    pids_to_kill = set()
    
    # 1. Collect PIDs from connected clients (including orphans)
    for name, info in list(clients.items()):
        try:
            info["conn"].sendall(b"KILL")
        except:
            pass
        if info["pid"] > 0:
            pids_to_kill.add(info["pid"])
            
    # 2. Collect PIDs from launched processes (if valid)
    for proc in launched_processes:
        if proc.pid:
            pids_to_kill.add(proc.pid)
            
    # 3. Force kill via taskkill /T (Tree kill)
    for pid in pids_to_kill:
        try:
            print(f"【Main】強制終止 PID: {pid}")
            # Use taskkill /F /T to kill process tree (handle PyInstaller wrapper)
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        except Exception as e:
            print(f"【Main】終止失敗 PID {pid}: {e}")
    
    clients.clear()
    launched_processes.clear()
    update_list()
    
    running = False
    try:
        root.destroy()
    except Exception:
        pass

def update_list():
    try:
        listbox.delete(0, tk.END)
        for name in clients:
            listbox.insert(tk.END, f"{name} ({clients[name]['pid']})")
    except Exception:
        pass

threading.Thread(target=server, daemon=True).start()

root = tk.Tk()
root.title("Process Simulator - Main Controller")

ttk.Label(root, text="Client 狀態（即時）").pack(pady=5)
listbox = tk.Listbox(root, width=40, height=8)
listbox.pack(padx=10, pady=5)

ttk.Button(root, text="啟動 Clients", command=build_and_launch).pack(pady=5)
ttk.Button(root, text="關閉全部 Clients（空白鍵）", command=kill_all).pack(pady=5)

root.bind("<space>", lambda e: kill_all())
root.protocol("WM_DELETE_WINDOW", kill_all)  # Handle window close button

root.mainloop()
