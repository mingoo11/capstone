import psutil
import subprocess
import ctypes
import os

def proc_monitor():
    process_list = ["SnippingTool.exe", "ALCapture.exe", "picpick.exe", "bdcam.exe", "GomCam.exe"]

    # 실행 중인 모든 프로세스 목록 가져오기
    processes = psutil.process_iter()

    # 각 프로세스에 대한 정보 출력
    for process in processes:
        if process.name() in process_list:
            print("PID:", process.pid)
            print("이름:", process.name())
            print("blacklist process")
            print("==========================")
            subprocess.call(["taskkill", "/F", "/PID", str(process.pid)])
            ctypes.windll.user32.MessageBoxW(None, f"{process.name()}는 실행할 수 없는 프로그램입니다.", '경고', 0x30)