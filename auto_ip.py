import os
import random
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def set_static_ip(adapter, network="192.168.2", mask="255.255.255.0", gateway=""):
    """Đặt IP tĩnh random trong dải, loại trừ .175"""
    while True:
        last_octet = random.randint(2, 254)
        if last_octet != 175:   # loại trừ 192.168.2.175
            break
    ip = f"{network}.{last_octet}"
    
    # Thực thi lệnh netsh để đổi IP
    cmd = f'netsh interface ip set address name="{adapter}" static {ip} {mask} {gateway}'
    os.system(cmd)
    print(f"✅ Đã đổi IP của {adapter} thành: {ip}")

if __name__ == "__main__":
    # Kiểm tra và yêu cầu quyền admin
    run_as_admin()
    print("✅ Đang chạy với quyền Administrator")
    
    # Gọi hàm set_static_ip với tham số mong muốn
    adapter = "Ethernet"  # Tên adapter mạng của bạn
    set_static_ip(adapter)


def set_dhcp(adapter):
    """Reset về DHCP (IP động)"""
    cmd_ip = f'netsh interface ip set address name="{adapter}" dhcp'
    cmd_dns = f'netsh interface ip set dns name="{adapter}" dhcp'
    os.system(cmd_ip)
    os.system(cmd_dns)
    print(f"♻️ Đã reset {adapter} về DHCP (IP động)")


if __name__ == "__main__":
    # ⚠️ Đổi tên card mạng tại đây: "Ethernet" hoặc "Wi-Fi"
    adapter_name = "Ethernet"

    print("=== Tool đổi IP ===")
    print("1. Dùng máy in")
    print("2. Dùng Telegram")
    choice = input("Chọn (1/2): ")

    if choice == "1":
        set_static_ip(adapter_name)
    elif choice == "2":
        set_dhcp(adapter_name)
    else:
        print("❌ Lựa chọn không hợp lệ")
