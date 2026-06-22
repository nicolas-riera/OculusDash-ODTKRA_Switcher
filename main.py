import os
import sys
import shutil
import ctypes
import subprocess
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_and_stop_service(service_name):
    try:
        query = subprocess.run(["sc", "query", service_name], capture_output=True, text=True, check=True)
        if "RUNNING" in query.stdout:
            print(f"[INFO] {service_name} is running. Attempting to stop it...")
            subprocess.run(["sc", "stop", service_name], capture_output=True, text=True, check=True)
            
            for _ in range(10):
                time.sleep(1)
                check = subprocess.run(["sc", "query", service_name], capture_output=True, text=True, check=True)
                if "STOPPED" in check.stdout:
                    print(f"[SUCCESS] {service_name} has been stopped.")
                    return True
            print(f"[ERROR] Timed out waiting for {service_name} to stop.")
            return False
        else:
            return True
    except subprocess.CalledProcessError:
        print(f"[WARNING] Could not query or stop {service_name}. It might not be installed.")
        return True

def main():
    if not is_admin():
        print("[ERROR] This script must be run as Administrator.")
        input("\nYou can now close the program.")
        sys.exit(1)

    if not check_and_stop_service("OVRService"):
        print("[ERROR] Cannot proceed while OVRService is running.")
        input("\nYou can now close the program.")
        sys.exit(1)

    target_dir = r"C:\Program Files\Meta Horizon\Support\oculus-dash\dash\bin"
    dash_path = os.path.join(target_dir, "OculusDash.exe")
    bak_path = os.path.join(target_dir, "OculusDash_bak.exe")

    if hasattr(sys, '_MEIPASS'):
        odtkra_source = os.path.join(sys._MEIPASS, "ODTKRA.exe")
    else:
        odtkra_source = "ODTKRA.exe"

    if not os.path.exists(dash_path):
        print(f"[ERROR] OculusDash.exe not found in {target_dir}")
        input("\nYou can now close the program.")
        sys.exit(1)

    file_size = os.path.getsize(dash_path)
    threshold = 10 * 1024 * 1024

    if file_size > threshold:
        print("[INFO] Original OculusDash detected. Starting backup and swap process...")
        try:
            shutil.copy2(dash_path, bak_path)
            print("[SUCCESS] Backup created successfully (OculusDash_bak.exe).")
            
            if not os.path.exists(odtkra_source):
                print(f"[ERROR] Source ODTKRA.exe not found at {odtkra_source}")
                input("\nYou can now close the program.")
                sys.exit(1)
                
            shutil.copy2(odtkra_source, dash_path)
            print("[SUCCESS] ODTKRA.exe successfully installed as OculusDash.exe.")
            input("\nYou can now close the program.")
        except Exception as e:
            print(f"[ERROR] An error occurred during the swap: {e}")
            input("\nYou can now close the program.")
            sys.exit(1)
    else:
        print("[INFO] ODTKRA detected. Restoring original OculusDash...")
        if not os.path.exists(bak_path):
            print("[ERROR] Backup file (OculusDash_bak.exe) not found. Cannot restore.")
            input("\nYou can now close the program.")
            sys.exit(1)
        try:
            os.remove(dash_path)
            os.rename(bak_path, dash_path)
            print("[SUCCESS] Original OculusDash.exe successfully restored.")
            input("\nYou can now close the program.")
        except Exception as e:
            print(f"[ERROR] An error occurred during the restoration: {e}")
            input("\nYou can now close the program.")
            sys.exit(1)

if __name__ == "__main__":
    main()