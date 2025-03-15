# Smart Traffic Signal Management

This project demonstrates how to process multiple videos simultaneously using OpenCV. The script applies background subtraction to detect moving objects in each video stream. Controls traffic signals with the help of an Arduino Uno.

## Features
- Reads multiple video files.
- Applies background subtraction using OpenCV's `createBackgroundSubtractorMOG2`.
- Displays processed video frames with moving objects highlighted.
- Controls traffic signals with the help of an Arduino Uno.

## Prerequisites
Ensure you have the following installed on your system:
- Python 3.x
- OpenCV
- NumPy
- Pyserial

## Installation
1. **Install Python** (if not already installed)
   - Download and install Python from [python.org](https://www.python.org/).
   
2. **Clone the Repository**
   ```bash
   git clone https://github.com/themonstersd13/WCEHackathon2025_CodingMonsters
   ```

3. **Install Required Dependencies**
   ```bash
   pip install opencv-python numpy
   ```
   If you need additional OpenCV functionalities, install:
   ```bash
   pip install opencv-contrib-python numpy
   ```

## Download YOLOv3 weights
```bash
curl -O https://pjreddie.com/media/files/yolov3.weights
```

## Download YOLOv3 configuration file
```bash
curl -O https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg
```

## Download COCO class names file
```bash
curl -O https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names
```

## Usage
1. Place your video files in the project directory.
2. Modify the script to include your video file names.
3. Run the script:
   ```bash
   python multi_video_processing.py
   ```

## Code Structure
- `multi_video_processing.py` - Main script for video processing.
- `videos/` - Directory where video files should be placed.

## Example Output
The script will open multiple windows, each showing the processed video frames.

## Troubleshooting
- Ensure that the video file names match those in the script.
- Install missing dependencies if you encounter errors.
- Try running the script with a different Python version (preferably Python 3.8+).

## Serial Data Transfer from File to Arduino

### Overview
This Python script reads car count data from a text file (`carsCount.txt`) and sends it to an Arduino via a serial connection. The script ensures that new data is only sent after receiving an acknowledgment (`DONE`) from the Arduino.

### Requirements
- Python 3
- `pyserial` library
- Arduino board
- A connected serial port (e.g., `/dev/ttyACM0` for Linux, `COM3` for Windows)
- `carsCount.txt` file with car count data

### Installation
1. Install Python 3 if not already installed.
2. Install the `pyserial` library using:
   ```sh
   pip install pyserial
   ```
3. Connect the Arduino to your system via USB.
4. Ensure the correct serial port is specified in the script (`/dev/ttyACM0` for Linux or `COMx` for Windows).

### Usage
1. Create a text file named `carsCount.txt` in the same directory as the script.
2. Add numeric values to the file representing the car count.
3. Run the script using:
   ```sh
   python number.py
   ```
4. The script will:
   - Read the latest car count from `carsCount.txt`
   - Send it to the Arduino over the serial port
   - Wait for an acknowledgment (`DONE`) from the Arduino before sending new data
   - Repeat this process continuously

### Troubleshooting
- **Permission Issues**: If you get permission errors on Linux, run:
  ```sh
  sudo chmod 666 /dev/ttyACM0
  ```
- **No Response from Arduino**: Ensure the correct port is used and the Arduino is running the corresponding script.
- **File Not Found**: Ensure `carsCount.txt` exists in the same directory as the script.
- **Sandbox Issue**: If you get a sandbox error, use the following option:
  ```sh
  --no-sandbox
  ```

## Real-Time Traffic Countdown Visualization

### Overview
`countDown.py` is a script that visualizes a real-time traffic light countdown in the terminal. It reads data from a serial connection and updates the display to show traffic light status for multiple roads.

### Features
- Reads serial data from an Arduino.
- Displays a real-time traffic light status with countdown timers.
- Automatically reverts the lights to red (`🔴`) after the countdown ends.
- Ensures smooth real-time updates without blocking operations.

### Installation
1. Install Python 3 if not already installed.
2. Install `pyserial` using:
   ```bash
   pip install pyserial
   ```
3. Connect the Arduino to your system via USB.

### Usage
1. Ensure the Arduino is running a compatible sketch that sends countdown data.
2. Run the script using:
   ```bash
   python countDown.py
   ```
3. The script will display:
   ```
   === Real-Time Traffic Status (HH:MM:SS) ===
   Road 1: 🟢 10s
   Road 2: 🔴 0s
   Road 3: 🔴 0s
   Road 4: 🔴 0s
   ======================================
   ```

### Notes
- Ensure that the correct serial port is set (`/dev/ttyACM0` for Linux, `COMx` for Windows).
- If no data appears, check your Arduino connection and serial permissions.
- The script continuously updates the display and reverts lights to red when the countdown ends.

## Project Developers
- Avadhut Mali
- Saurabh Doiphode
- Yash Savalkar
- Ritesh Jagtap

