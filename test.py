import time
import win32api
import win32con
import keymanager
import threading

def press_key(key_code):
    """Simulate a key press."""
    win32api.keybd_event(key_code, 0, 0, 0)
    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)

def benchmark_key_press():
    """Benchmark pressing the 'F' key 15 times."""
    key_code = 0x46  # Virtual key code for 'F'
    iterations = 15

    start_time = time.time()

    for _ in range(iterations):
        press_key(key_code)

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Time taken to press 'F' {iterations} times: {elapsed_time:.6f} seconds")

def benchmark_keymanager_press():
    key_mgr = keymanager.key_manager(is_homed=True, last_page=0)
    start_time = time.time()
    key_mgr.goto_page(15)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken to press times: {elapsed_time:.6f} seconds")

def benchmark_key_press_threads():
    """Benchmark pressing the 'F' key 15 times using threads."""
    key_code = 0x46  # Virtual key code for 'F'
    iterations = 15

    def thread_task():
        press_key(key_code)

    start_time = time.time()

    threads = [threading.Thread(target=thread_task) for _ in range(150)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Time taken to press 'F' {iterations} times using threads: {elapsed_time:.6f} seconds")

if __name__ == "__main__":
    benchmark_key_press()
    benchmark_keymanager_press()
    benchmark_key_press_threads()