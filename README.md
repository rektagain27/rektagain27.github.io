# CR2 to JPG Converter

## Overview
This is a simple Python script that provides a graphical user interface (GUI) for converting Canon CR2 raw image files to JPEG format. The script utilizes the Tkinter library for the GUI and the Pillow library for image processing.

## Features
- Select the input folder containing CR2 files.
- Choose the output folder for the converted JPEG files.
- Option to replace original CR2 files with the converted JPEG files.
- Display thumbnails of the images being processed.
- Start and stop the conversion process.

## Usage
### Running the Script
1. **Install Python:**
   - Install Python 3.x from the [Python Official Website](https://www.python.org/downloads/).

2. **Install Required Libraries:**
   - Open a command prompt or terminal and run the following command:
     ```bash
     pip install Pillow
     ```

3. **Run the Script:**
   - Navigate to the directory containing the script in the command prompt or terminal.
   - Execute the script using the following command:
     ```bash
     python your_script_name.py
     ```
     Replace `your_script_name.py` with the actual name of your script.

### Running the Executable (Windows)
1. **Download the Executable:**
   - Go to the [Releases](https://github.com/rektagain27/CR2-JPG-Converter/releases/tag/Production) section of this repository.
   - Download the latest release and unzip the files.

2. **Run the Executable:**
   - Double-click the `CR2_JPG.exe` file in the unzipped folder.
   - The GUI should open, and you can use the converter as described in the "Usage" section.

## Building an Executable
To create a standalone executable file, you can use tools like PyInstaller or cx_Freeze. See the [PyInstaller Documentation](https://pyinstaller.readthedocs.io/en/stable/) for details.

## Notes
- The script provides a simple GUI for converting CR2 files to JPG format.
- Make sure to back up important CR2 files before using the "Replace Original CR2 Files" option. I am warning you now that there is no way to retrieve files that are replaced by this program. I have attempted reasonably to make sure that it works for my purposes. Before you begin batch work on your own files, please try it on a small subset of your files and ensure that it does what you want it to.
- This script is for educational purposes and may require adjustments for specific use cases.

## License
This script is licensed under the [MIT License](LICENSE).
