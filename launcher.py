import os
import sys
import time
import webbrowser
import threading
import uvicorn

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def start_browser():
    time.sleep(1.5)
    url = "http://127.0.0.1:8000"
    print(f"打开浏览器访问: {url}")
    webbrowser.open(url)

if __name__ == "__main__":
    print("启动 SiliconFlow TTS Studio...")

    threading.Thread(target=start_browser, daemon=True).start()

    try:
        uvicorn.run("src.api:app", host="127.0.0.1", port=8000, reload=False, log_level="info")
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"\n服务器错误: {e}")
        input("按回车键退出...")