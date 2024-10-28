# MULTI_GEERT

## Overview
The `MULTI_GEERT` module is a part of a graphical user interface (GUI) application for monitoring and recording EEG (electroencephalogram) data. It provides real-time visualization, data handling, and user interface elements to interact with EEG data sources in parallel. The application is designed to visualize EEG data from multiple devices in a single interface, enabling researchers to monitor and record EEG data from different sources simultaneously.

## Motivation
EEG data is often collected using different devices and software, making it challenging to visualize and analyze data from multiple sources.
The main contribution of the `MULTI_GEERT` project is its ability to handle and visualize EEG data from independent devices regardless of their type. This is achieved through the use of the Lab Streaming Layer (LSL) protocol, which synchronizes data acquired from different devices. The `MULTI_GEERT` application manages all this data to visualize it in monitors.

## Parallel EEG Monitoring
The `MULTI_GEERT` application provides a user-friendly interface for monitoring and recording EEG data from multiple devices in parallel. It allows users to visualize EEG data from different sources in a single interface, enabling researchers to monitor and record EEG data from multiple devices simultaneously. The application supports real-time visualization of EEG data, including spectrogram and frequency monitoring, as well as data handling features such as streaming and recording of EEG data, buffer management, and file operations. The `MULTI_GEERT` application is designed to be flexible and extensible, allowing users to customize the interface and add new features as needed.

**Real-Time Parallel EEG data processing**:
  - The application supports real-time processing of EEG data from multiple devices in parallel.

## Monitor Features
- **User Interface Elements**:
  - Text Inputs for setting filter order and window size.
  - Combo Boxes for selecting frequency range, filtering method, and channels.
  - Radio Buttons for toggling between different modes (e.g., spectrogram mode).
  - Buttons for adding markers and quitting the application.
  - Sliders for adjusting the scale and space of the EEG display.
  - Scroll Bars for vertical scrolling of the EEG display.

- **Data Handling**:
  - Streaming and recording of EEG data.
  - Buffer management for storing EEG data.
  - File operations for creating, appending, and closing files.
  - Annotations and markers for EEG data.

- **Visualization**:
  - Timer-based visualization for periodic updates of EEG and frequency monitors.
  - Spectrogram and frequency monitoring.

- **Event Handling**:
  - Signal connections for updating parameters, adding markers, and handling file operations.
  - Custom event handlers for annotations and file saving.

- **Mode Selection**:
  - Spectrogram mode for different visualization modes.

- **File Dialogs**:
  - Save and open file dialogs.

## Installation
To install the required dependencies, run:
```bash
pip install -r requirements.txt
```

## Usage
To run the application, execute:
```bash
python MULTI_GEERT.py
```

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License
This project is licensed under the MIT License.

## Contact
For any questions or feedback, please contact [mvalcal1@upv.edu.es].
