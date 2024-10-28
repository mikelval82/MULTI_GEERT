# MULTI_GEERT

## Overview
The `MULTI_GEERT` module is a graphical user interface (GUI) application designed for real-time monitoring and recording of EEG (electroencephalogram) data from multiple devices. By leveraging the Lab Streaming Layer (LSL) protocol, this application can synchronize and visualize EEG data from various devices within a single interface. This flexibility allows researchers to perform simultaneous data recording and analysis from different EEG sources, facilitating real-time processing for advanced analyses like coherence evaluation and multi-participant sentiment analysis.

## Motivation
Collecting and analyzing EEG data from different devices can be challenging due to differences in hardware and software platforms. The `MULTI_GEERT` application addresses this issue by unifying EEG data from independent devices, regardless of type, into one synchronized interface. This enables researchers to seamlessly monitor and process EEG data in real-time, supporting applications like coherence analysis and collaborative research environments involving multiple subjects.

## Key Features
- **Parallel EEG Monitoring**: Visualize and record EEG data from multiple devices in parallel, enabling real-time monitoring of multiple sources.
- **Real-Time Processing**: Supports coherence evaluation, spectrogram visualization, and frequency analysis for live data analysis.
- **User-Friendly Interface**: Allows easy configuration of signal sources and parameters for a customizable user experience.
- **Flexible Recording and Streaming Options**: Offers options to activate, record, and stream EEG signals with settings like Butterworth filter, window size, and frequency range adjustments.
  
## Modules

### EEG Generator Module
The `EEG_generator.py` module generates synthetic EEG data for testing, simulating real-time EEG data streams when physical devices are unavailable. This can be useful for testing system stability and response under controlled conditions. Users can create various types of signals, such as sinusoidal or square waves, and stream them over the LSL protocol.

#### Features
- **Signal Generation**: Supports synthetic signal generation, including sinusoidal and square waveforms.
- **Real-Time Streaming**: Streams generated data using LSL, suitable for testing and demonstrations.
- **Customizable Parameters**: Offers settings for signal type, frequency, amplitude, sampling rate, and channel count.

#### Usage
To generate and stream synthetic EEG data:
```bash
python EEG_generator.py [signal_type] [stream_name] [phase]
```

- `signal_type`: Type of signal (`sinusoidal` or `square`).
- `stream_name`: Name of the simulated signal stream.
- `phase`: Phase of the signal in radians (default is 0).

Example:
```bash
python EEG_generator.py sinusoidal sim_1 0
```

This command generates a sinusoidal signal named `sim_1` with a phase of 0 radians and streams it using LSL.

## Installation
To install the required dependencies, use the following command:
```bash
pip install -r requirements.txt
```

## Usage
To launch the main `MULTI_GEERT` application:
```bash
python MULTI_GEERT.py
```

## Contributing
1. Fork this repository.
2. Create a new branch for your feature (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push your branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License.

## Contact
For any questions or feedback, please contact [mvalcal1@upv.edu.es].

