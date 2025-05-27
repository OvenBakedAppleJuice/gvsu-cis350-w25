# Overview

This document describes the functional and non-functional requirements of the semester project for BTripleJ in CIS350. The project is an audio visualizer with a microcontroller and LED display along with a Python GUI and python audio processing. The functional requirements describe the functionality of the entire system, and the non-functional requirements outline some of the ways it may be implemented.

# Functional Requirements

1. The system shall have a GUI that allows for controlling the audio visualizer. -JNS

2. The system shall have a GUI to select a port for Arduino. JGM

3. The system shall have a LED display for the audio visualization. -JNS

4. The system shall be able to use audio from a microphone. -JNS

5. The system shall be able to use audio from a file.-B

6. The system shall be able to send serial data to a microcontroller. JGM

7. The system shall parse pitch and volume from serial data. JGM

8. The system shall find the frequencies from a given audio input. -B

9. The system shall find the amplitude from a given audio input. - B

10. The system shall have documentation to explain how to use it. -JNS

11. The system shall support different visualizations modes -JD

12. The system shall notify the user if a serial port is unavailable. JGM

13. The system shall power the LED reliably - JD

14. The system shall allow the user to easily turn on/off the system itself. - JD

15. The system shall display audio values to show proper usage of the sound system - JD



# Non-Functional Requirements

1. The system may use an Arduino microcontroller - B

2. The system may use the FastLED library - B

3. The system may use python PyAudio, an API for PortAudio, to get audio input. -JNS

4. The system may use the Tkinter library for the GUI. -JNS

5. The system may use python multithreading to collect audio while processing it.-JNS

6. The system may process data in 200 milliseconds. JGM

7. The system may filter out bad inputs on the microcontroller input JGM

8. The system may be able to perform with both Mac and Windows. JGM

9. The system may use prebuilt python packages. - JD

10. The system may have a simple, intuitive, GUI - B

11. The system may use python numpy to process data more quickly. -JNS

12. The system may operate continuously without crashing - JD

13. The system may set a max and minimal brightness for the LEDs -JGM

14. The system may be durable for prolonged use - JD

15. The system may use different color LEDs to denote different frequencies. - B

16. The system may be modular for and well-documented to allow for future updates - JD

