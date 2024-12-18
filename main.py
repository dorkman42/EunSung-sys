import socket
import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import threading

# Global variables
client_socket = None
is_receiving = False

# Column names for CSV based on protocol fields
CSV_FIELDS = [
    "Date", "Time", "STX", "COM1", "COM2", "Serial7", "Serial6", "Serial5", "Serial4", "Serial3", "Serial2", "Serial1",
    "복합악취1", "복합악취2", "복합악취3", "복합악취4", "복합악취5",
    "암모니아", "H2S", "TVOCs", "아세트알데하이드", "메틸메르캅탄", "포름알데하이드",
    "PM10", "PM10_1", "PM10_2", "PM10_3", "PM10_4",
    "PM2.5", "PM2.5_1", "PM2.5_2", "PM2.5_3", "PM2.5_4",
    "외기온도(부호)", "외기온도", "외기습도(부호)", "외기습도",
    "다이메틸설파이드", "다이메틸다이설파이드",
    "스타이렌", "뷰틸알데하이드", "톨루엔", "메틸에틸케톤", "메틸아이소뷰틸케톤", "뷰틸아세테이드",
    "i-뷰틸알코올", "아황산가스", "풍향[도]", "풍속[m/s]", "ETX"
]

# Function to receive and save data
def receive_and_save_data(ip, port, csv_path):
    global client_socket, is_receiving
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind((ip, port))
    print(f"Receiving data on {ip}:{port}")

    with open(csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(CSV_FIELDS)  # Write the column headers

        try:
            while is_receiving:
                data, _ = client_socket.recvfrom(1024)
                now = datetime.now()
                date = now.strftime("%Y-%m-%d")
                time = now.strftime("%H:%M:%S")
                parsed_data = parse_protocol_data(data.decode('utf-8'))

                # Save parsed data
                csv_writer.writerow([date, time] + parsed_data)
                print(f"Saved: {parsed_data}")
        except Exception as e:
            print(f"Reception stopped: {e}")
        finally:
            client_socket.close()

# Function to parse protocol data (0X2C as delimiter)
def parse_protocol_data(raw_data):
    fields = raw_data.split('0X2C')  # Split by 0X2C

    # Ensure each field is trimmed and assigned to its position
    parsed = [field.strip() for field in fields]

    # Pad with empty strings if fields are missing
    if len(parsed) < len(CSV_FIELDS) - 2:
        parsed += ["" for _ in range(len(CSV_FIELDS) - 2 - len(parsed))]

    # Ensure every field fits into its respective column
    return parsed[:len(CSV_FIELDS) - 2]

# GUI for receiving data
def run_reception_gui():
    global is_receiving

    def start_reception():
        global is_receiving
        if is_receiving:
            print("Already receiving.")
            return

        ip = ip_entry.get()
        port = int(port_entry.get())
        csv_path = file_path.get()
        if csv_path:
            is_receiving = True
            threading.Thread(target=receive_and_save_data, args=(ip, port, csv_path), daemon=True).start()

    def stop_reception():
        global is_receiving, client_socket
        is_receiving = False
        if client_socket:
            client_socket.close()
        print("Reception stopped.")

    def select_file():
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if path:
            file_path.set(path)

    root = tk.Tk()
    root.title("Reception Configuration")

    tk.Label(root, text="IP Address:").grid(row=0, column=0, padx=5, pady=5)
    ip_entry = tk.Entry(root)
    ip_entry.grid(row=0, column=1, padx=5, pady=5)
    ip_entry.insert(0, "127.0.0.1")

    tk.Label(root, text="Port:").grid(row=1, column=0, padx=5, pady=5)
    port_entry = tk.Entry(root)
    port_entry.grid(row=1, column=1, padx=5, pady=5)
    port_entry.insert(0, "12345")

    file_path = tk.StringVar()
    tk.Label(root, text="Save to:").grid(row=2, column=0, padx=5, pady=5)
    tk.Entry(root, textvariable=file_path).grid(row=2, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=select_file).grid(row=2, column=2, padx=5, pady=5)

    start_button = tk.Button(root, text="Connect", command=start_reception)
    start_button.grid(row=3, column=0, padx=5, pady=10)

    stop_button = tk.Button(root, text="Disconnect", command=stop_reception)
    stop_button.grid(row=3, column=1, padx=5, pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_reception_gui()
