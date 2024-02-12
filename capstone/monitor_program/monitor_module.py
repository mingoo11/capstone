import os
import time
import keyboard
import socket
import hashlib
from _thread import *
import proc_monitor_module
import screenshot_monitor_module
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys

sys.path.append("C:\\Users\\user\\Desktop\\capstone\\capstone\\monitor_program_server")

from db import save_to_database



begin_hash = set()
compare_hash = set()

log_time = time.strftime('%Y-%m-%d %H-%M-%S')
monitor_path = input("please input monitoring path = ")
username = os.getlogin()

HOST = input("please input server IP = ")
PORT = 1234

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

message = f"start: {log_time}\n"
client_socket.send(message.encode())

def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        print("recive : ", repr(data.decode()))

start_new_thread(recv_data, (client_socket,))
print('>> Connect Server')

def get_file_hash(file_path):
    hasher = hashlib.sha256()

    with open(file_path, 'rb') as file:
        for block in iter(lambda: file.read(4096), b''):
            hasher.update(block)
    return hasher.hexdigest()


def begin_file_hash(directory_path):
    global begin_hash
    hash_string = ""

    for root, dirs, files in os.walk(directory_path):
        files.sort()

        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = get_file_hash(file_path)
            begin_hash.add(file_hash)
            hash_string += f'{file_name}: {file_hash}\n'  # 파일 이름과 해시 값을 함께 저장

    print("begin_hash:")
    print(hash_string)
    return begin_hash


def compare_file_hash(directory_path):
    global compare_hash

    for root, dirs, files in os.walk(directory_path):
        files.sort()

        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = get_file_hash(file_path)
            compare_hash.add(file_hash)
    print(f'compare_hash: {compare_hash}')
    return compare_hash

begin_file_hash(monitor_path)
message = f"origin_hash: {begin_hash}\n"
client_socket.send(message.encode())

######### monitoring logic #########
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):

        if event.is_directory:
            print(f"Directory created: {event.src_path}")
            message = f"User: {username} &&& Directory created path: {event.src_path} &&& Directory created time: {time.strftime('%Y-%m-%d %H-%M-%S')}\n"
            #client_socket.send(message.encode())
            save_to_database("created", "create_directory", message)
        else:
            print(f"File created: {event.src_path}")
            compare_file_hash(monitor_path)
            if begin_hash != compare_hash:
                message = f"User: {username} &&& File created: {event.src_path} &&& File created time: {time.strftime('%Y-%m-%d %H-%M-%S')}\n"
                #client_socket.send(message.encode())
                save_to_database("created", "create_file", message)
                message = f"compare_hash: {compare_hash}\n"
                #client_socket.send(message.encode())
                save_to_database("created", "compare_hash", message)
                begin_hash.clear()
                begin_hash.update(compare_hash)
                compare_hash.clear()

    def on_modified(self, event):
        global begin_hash, compare_hash

        if event.is_directory:
            print(f"Directory modified: {event.src_path}")
            message = f"User: {username} &&& Directory modified: {event.src_path} &&& Directory modified time: {time.strftime('%Y-%m-%d %H-%M-%S')}\n"
            #client_socket.send(message.encode())
            save_to_database("modified", "modified_directory", message)
        else:
            print(f"File modified: {event.src_path}")
            compare_file_hash(monitor_path)
            if begin_hash != compare_hash:
                message = f"User: {username} &&& File modified: {event.src_path} &&& File modified time: {time.strftime('%Y-%m-%d %H-%M-%S')}\n"
                #client_socket.send(message.encode())
                save_to_database("modified", "modified_file", message)
                message = f"compare_hash: {compare_hash}\n"
                #client_socket.send(message.encode())
                print (message)
                save_to_database("modified", "compare_hash", message)
                begin_hash.clear()
                begin_hash.update(compare_hash)
                compare_hash.clear()

    def on_deleted(self, event):
        if event.is_directory:
            print(f"Directory deleted: {event.src_path}")
            message = f"User: {username} &&& Directory deleted: {event.src_path} &&& Directory deleted time: {time.strftime('%Y-%m-%d %H-%M-%S')}\n"
            #client_socket.send(message.encode())
            save_to_database("deleted", "deleted_directory", message)
        else:
            print(f"File deleted: {event.src_path}")
            compare_file_hash(monitor_path)
            #if begin_hash != compare_hash:
            message = f"User: {username} &&& File deleted: {event.src_path} &&& File deleted time: {time.strftime('%Y-%m-%d %H-%M-%S')}\n"
            #client_socket.send(message.encode())
            save_to_database("deleted", "deleted_file", message)
            message = f"compare_hash: {compare_hash}\n"
            #client_socket.send(message.encode())
            save_to_database("deleted", "compare_hash", message)
            begin_hash.clear()
            begin_hash.update(compare_hash)
            compare_hash.clear()

def start_watchdog(monitor_path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, monitor_path, recursive=True)
    observer.start()

    try:
        while True:
            proc_monitor_module.proc_monitor()
            screenshot_monitor_module
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    client_socket.close()

start_watchdog(monitor_path)