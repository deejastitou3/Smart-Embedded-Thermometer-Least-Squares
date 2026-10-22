#  Smart Embedded Thermometer with Statistical Filtering

An intelligent thermal supervision system that bridges low-level embedded hardware with high-level software. The system acquires analog temperature data via an Arduino UNO, applies a **Least Squares Linear Regression** algorithm directly on the microcontroller to filter sensor noise, and visualizes the filtered data in real-time on a Python Tkinter dashboard.

![C++](https://img.shields.io/badge/C%2B%2B-Arduino-blue)
![Python](https://img.shields.io/badge/Python-Tkinter-yellow)
![Arduino](https://img.shields.io/badge/Hardware-Arduino_UNO-00979D)
![Math](https://img.shields.io/badge/Algorithm-Least_Squares-orange)

## About the Project
Analog sensors like the LM35 are highly susceptible to electrical noise and ADC quantization errors. Instead of using a simple moving average, this project implements a statistical filtering approach. By taking 20 consecutive samples and applying linear regression, the system identifies the measurement that best fits the thermal trend, effectively eliminating outliers and providing a highly stable reading.

##  Key Features
- **Statistical Noise Filtering:** Implements Least Squares Linear Regression ($y = ax + b$) on the ATmega328P microcontroller to select the most statistically representative measurement.
- **Hardware-Software Co-design:** Seamless real-time communication between C++ embedded firmware and a Python PC application via USB Serial (9600 baud).
- **Real-Time Supervision GUI:** A multithreaded Tkinter dashboard that updates dynamically without blocking the UI.
- **Visual Alert System:** Automatic color-coded UI changes (Pastel Green to Coral Red) when the temperature exceeds a critical threshold (35°C).

##  System Architecture
The system is divided into three main blocks:
1. **Acquisition Block:** Arduino UNO reads the LM35 analog sensor (10-bit ADC).
2. **Processing Block:** The microcontroller executes the Least Squares algorithm to filter the 20-sample dataset.
3. **Supervision Block:** Python application receives the filtered data via PySerial and renders the GUI.

##  Tech Stack
- **Embedded:** C++ (Arduino IDE), ATmega328P, 10-bit ADC.
- **Software:** Python 3, Tkinter, PySerial, Threading.
- **Math:** Linear Regression, Least Squares Method.

##  Project Structure
Smart-Embedded-Thermometer-Least-Squares/
├── thermometer.ino      # Arduino C++ firmware
├── supervision.py       # Python Tkinter dashboard
└── requirements.txt     # Python dependencies
├── thermometer.ino      # Arduino C++ firmware
├── supervision.py       # Python Tkinter dashboard
└── requirements.txt     # Python dependencies

## Installation & Usage
1. Hardware Setup
Connect the LM35 output pin to Arduino Analog Pin A0.
(Optional) Connect a push button to Pin 2 to trigger measurements, and a buzzer to Pin 8.
2. Upload Firmware
Open thermometer.ino in the Arduino IDE.
Select your board (Arduino UNO) and port.
Upload the code.
3. Run the Supervision Dashboard
# Install dependencies
pip install pyserial
# Run the Python GUI (Make sure to update the COM port in the script if necessary)
python supervision.py
