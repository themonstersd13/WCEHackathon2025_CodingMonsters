# Multi-Video Processing with OpenCV

This project demonstrates how to process multiple videos simultaneously using OpenCV. The script applies background subtraction to detect moving objects in each video stream.

## Features
- Reads multiple video files.
- Applies background subtraction using OpenCV's `createBackgroundSubtractorMOG2`.
- Displays processed video frames with moving objects highlighted.

## Prerequisites
Ensure you have the following installed on your system:
- Python 3.x
- OpenCV
- NumPy

## Installation
1. **Install Python** (if not already installed)
   - Download and install Python from [python.org](https://www.python.org/).
   
2. **Clone the Repository**
   ```bash
   git clone https://github.com/avadhutmali/Secret_Invasion.git
   cd Secret_Invasion
   ```

3. **Install Required Dependencies**
   ```bash
   pip install opencv-python numpy
   ```
   If you need additional OpenCV functionalities, install:
   ```bash
   pip install opencv-contrib-python numpy
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

## License
This project is licensed under the MIT License.

## Contributing
Feel free to submit pull requests or report issues!

## Author
Coding Monster
