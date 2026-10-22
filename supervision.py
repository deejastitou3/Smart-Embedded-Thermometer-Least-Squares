import tkinter as tk
import serial
import threading
import time

# --- Configuration ---
# IMPORTANT: Change this to your actual Arduino COM port 
# (e.g., 'COM3' or 'COM4' on Windows, '/dev/ttyUSB0' or '/dev/cu.usbmodem...' on Mac/Linux)
SERIAL_PORT = 'COM4' 
BAUD_RATE = 9600
THRESHOLD_TEMP = 35.0

class MagicThermometer:
    def __init__(self, root):
        self.root = root
        self.root.title("Magic Thermometer - Smart Supervision")
        self.root.geometry("450x350")
        self.root.configure(bg="#FFF0F5") # Lavender Blush pastel background
        
        self.temp_var = tk.StringVar(value="--.- °C")
        self.status_var = tk.StringVar(value="Status: Connecting...")
        
        self.setup_ui()
        self.start_serial_listener()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="🌡️ Magic Thermometer", 
                               font=("Helvetica", 20, "bold"), bg="#FFF0F5", fg="#333")
        title_label.pack(pady=20)
        
        # Temperature Display (Large and dynamic)
        self.temp_label = tk.Label(self.root, textvariable=self.temp_var, 
                                   font=("Helvetica", 48, "bold"), bg="#FFF0F5", fg="#7BED9F")
        self.temp_label.pack(pady=10)
        
        # Status Label
        status_label = tk.Label(self.root, textvariable=self.status_var, 
                                font=("Helvetica", 12), bg="#FFF0F5", fg="#666")
        status_label.pack(pady=10)
        
        # Threshold Info
        info_label = tk.Label(self.root, text=f"Alert Threshold: {THRESHOLD_TEMP}°C", 
                              font=("Helvetica", 10), bg="#FFF0F5", fg="#999")
        info_label.pack(side=tk.BOTTOM, pady=10)

    def start_serial_listener(self):
        """Starts a background thread to listen to the serial port without blocking the GUI."""
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(2) # Wait for Arduino to reset and establish connection
            self.status_var.set("Status: Connected & Listening")
            threading.Thread(target=self.listen_serial, daemon=True).start()
        except serial.SerialException:
            self.status_var.set(f"Error: Could not open {SERIAL_PORT}. Check port settings.")

    def listen_serial(self):
        """Continuously reads data from the serial port in the background."""
        while True:
            try:
                if self.ser.in_waiting > 0:
                    raw_data = self.ser.readline()
                    data = raw_data.decode('utf-8', errors='ignore').strip()
                    
                    if data:
                        try:
                            temp = float(data)
                            # Schedule UI update safely in the main thread
                            self.root.after(0, self.update_ui, temp)
                        except ValueError:
                            pass # Ignore non-float data (e.g., empty lines)
            except Exception:
                pass
            time.sleep(0.1)

    def update_ui(self, temp):
        """Updates the GUI with the new temperature and handles color alerts."""
        self.temp_var.set(f"{temp:.2f} °C")
        
        if temp > THRESHOLD_TEMP:
            self.temp_label.config(fg="#FF6B6B") # Coral Red for alert
            self.status_var.set("Status: ⚠️ HIGH TEMPERATURE ALERT!")
            self.status_var.config(fg="#FF6B6B")
        else:
            self.temp_label.config(fg="#7BED9F") # Pastel Green for normal
            self.status_var.set("Status: Normal Operation")
            self.status_var.config(fg="#666")

if __name__ == "__main__":
    root = tk.Tk()
    app = MagicThermometer(root)
    root.mainloop()