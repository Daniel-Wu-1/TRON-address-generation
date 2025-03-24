import os
import sys
import time
import threading
import multiprocessing
from multiprocessing import Process, Event, Value, cpu_count
from tronpy.keys import PrivateKey

def generate_tron_address():
    private_key = PrivateKey(os.urandom(32))
    return private_key.public_key.to_base58check_address(), private_key.hex()

def save_result_to_file(address, private_key, prefix, suffix):
    file_path = "地址.txt"
    with open(file_path, "a") as file:
        file.write(f"前缀: {prefix}, 后缀: {suffix}\n")
        file.write(f"地址: {address}\n")
        file.write(f"私钥: {private_key}\n")
        file.write("=" * 40 + "\n")
    print(f"\n结果已保存到文件 {file_path}")

def find_vanity_address(prefix, suffix, stop_event, counter):
    while not stop_event.is_set():
        address, private_key = generate_tron_address()
        with counter.get_lock():
            counter.value += 1
        if address.startswith(prefix) and address.endswith(suffix):
            stop_event.set()
            save_result_to_file(address, private_key, prefix, suffix)
            print(f"\n找到靓号地址！\n地址: {address}\n私钥: {private_key}")
            return
    return

def monitor_progress(counter, stop_event):
    last_time = time.time()
    last_count = 0
    while not stop_event.is_set():
        time.sleep(0.5)
        now = time.time()
        with counter.get_lock():
            count = counter.value
        interval = now - last_time
        speed = (count - last_count) / (interval + 1e-9)
        print(f"\r已生成: {count} | 速度: {speed:.0f} 地址/秒", end="")
        last_time, last_count = now, count

def multithread_vanity_search(prefix, suffix):
    stop_event = Event()
    counter = Value('i', 0)
    max_processes = cpu_count()
    monitor_thread = threading.Thread(target=monitor_progress, args=(counter, stop_event), daemon=True)
    monitor_thread.start()
    processes = []
    for _ in range(max_processes):
        p = Process(target=find_vanity_address, args=(prefix, suffix, stop_event, counter))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    return counter.value

def get_user_choice():
    print("\n请选择接下来的操作:")
    print("1. 继续运行 (使用相同条件)")
    print("2. 更新生成条件")
    print("3. 退出程序")
    choice = input("请输入你的选择 (1/2/3): ").strip()
    return choice

def main():
    while True:
        print("(Telegram) by @jiutong9999")
        prefix = input("请输入地址的开头 (例如 TTTT): ").strip()
        while not prefix.startswith("T"):
            print("TRON 地址开头必须为 'T'，请重新输入。")
            prefix = input("请输入地址的开头 (例如 TTTT): ").strip()
        suffix = input("请输入地址的结尾 (例如 9999): ").strip()
        print("开始寻找靓号地址...")
        attempts = multithread_vanity_search(prefix, suffix)
        print(f"\n总生成地址数: {attempts}")
        choice = get_user_choice()
        if choice == "1":
            print("继续运行，使用相同条件...")
            continue
        elif choice == "2":
            print("更新生成条件...")
            continue
        elif choice == "3":
            print("程序退出。")
            break
        else:
            print("无效选择，程序退出。")
            break

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
