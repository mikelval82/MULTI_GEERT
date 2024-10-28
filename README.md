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

### EEG Generator Module

The `EEG_generator.py` module is responsible for generating synthetic EEG data for testing purposes. This is useful for simulating EEG data streams when real EEG devices are not available or for testing the system under controlled conditions. The module can generate different types of synthetic signals, such as sinusoidal or square waves, and stream this data using the Lab Streaming Layer (LSL) protocol.

#### Features
- **Signal Generation**: Create synthetic EEG signals, including sinusoidal or square waves.
- **Real-Time Streaming**: Stream the generated data in real-time using the LSL protocol.
- **Customizable Parameters**: Adjust signal type, frequency, amplitude, sampling rate, and number of channels.

#### Usage
To generate and stream synthetic EEG data, execute the following command:

```bash
python EEG_generator.py [signal_type] [stream_name] [phase]
```

- `signal_type`: Type of signal to generate (`sinusoidal` or `square`).
- `stream_name`: Name of the stream of the simulated signal.
- `phase`: Phase of the signal in radians (default is 0).

Example:

```bash
python EEG_generator.py sinusoidal sim_1 0
```

This command will generate a sinusoidal EEG signal called sim_1 with a phase of 0 radians and stream it using the LSL protocol.

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
