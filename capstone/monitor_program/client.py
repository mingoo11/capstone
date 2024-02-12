import monitor_module

def monitor():
    monitor_module.start_watchdog()

if __name__ == "__main__":
    monitor()
    