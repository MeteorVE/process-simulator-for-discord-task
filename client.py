# client.py
import socket
import threading
import time
import msvcrt
import os
import sys

SERVER = ("127.0.0.1", 5050)
CLIENT_NAME = os.path.basename(sys.argv[0])
RUN_SECONDS = 16 * 60  # 16 minutes
running = True


def listen_server(sock):
    global running
    while running:
        try:
            data = sock.recv(1024)
            if not data:
                print("【Client】主控斷線，自動關閉")
                running = False
                break
            if data.decode() == "KILL":
                print("【Client】收到主控關閉指令")
                running = False
        except Exception:
            print("【Client】連線異常，自動關閉")
            running = False
            break

def main():
    print(f"【Client】啟動成功：{CLIENT_NAME}")
    print("【Client】按【空白鍵】可關閉此 Client（或 16 分鐘自動結束）")


    sock = socket.socket()
    sock.connect(SERVER)
    pid = os.getpid()
    sock.sendall(f"HELLO:{CLIENT_NAME}:{pid}".encode())

    threading.Thread(target=listen_server, args=(sock,), daemon=True).start()

    start = time.time()
    while running:
        if time.time() - start >= RUN_SECONDS:
            print("【Client】時間到，自動結束")
            break
        if msvcrt.kbhit():
            if msvcrt.getch() == b' ':
                print("【Client】使用者手動關閉")
                break
        time.sleep(0.1)

    try:
        sock.sendall(f"EXIT:{CLIENT_NAME}".encode())
    except Exception:
        pass
    sock.close()

if __name__ == "__main__":
    main()
