# B Triple J

Team members:
Blake, Joey, Josh, Jason

## Introduction

The goal is to create a Python script for analysing audio from either a microphone or computer input. The script will find the pitch of the audio played and send it to a microcontroller over a communication line, most likely UART. The microcontroller will then light up respective LEDs in response to the pitch and volume. There will be different options for the LED output, changing how the LEDs react to different frequencies.

# Feature List

The general idea is to create an audio visualizer with two major components. There will be a Python-Tkinter based application that collects and processes audio from the computer or microphone. There will also be an arduino connected to the computer over USB and controlled by the python application. The arduino will control a physical LED strip or panel using the FastLED library.

In the python application there will be a Microphone mode, Computer Audio mode, and potentially a Synth Keyboard mode. The audio input will be able to be selected to change mode. There will be multiple audio visualization modes that can be selected. The application will allow you to select the USB device as in windows COM port numbers change around. This communicates to an Arduino that uses FastLed. 

Depending on time one possible extra feature is a Synth Keyboard mode. One of our members has previously created a python-based synth keyboard. This could be added to the gui as another mode depending on time constraints for the project.

# Anticipated Technologies

(What technologies are needed to build this project)
This project uses some arduino technology including an Arduino Uno and an LED strip or panel to display the Audio Visualization. It then uses a variety of python libraries and an Audio API to create the application.
- Arduino Uno
- WS2812B (NeoPixels) or SK9822 (DotStars) LED Strip or Panel (link)
- FastLED Arduino Library 
- (Wokwi Demo:  https://wokwi.com/projects/289631971594732040) 
- Arduino IDE
- Windows Computer
- Microphone
- Python IDE: VS Code will be primarily used.
- Tkinter: For creating simple GUI. https://www.geeksforgeeks.org/python-gui-tkinter/ 
- Custom Tkinter: https://customtkinter.tomschimansky.com/
- PyAudio: PortAudio API is for getting microphone or computer audio. https://pypi.org/project/PyAudio/ 
- Numpy, threading, queue: These are libraries needed to stream audio data in real time.
- PySerial: ThisAPI is used to communicate with the arduino over UART.


# Method/Approach

(What is your estimated "plan of attack" for developing this project)
Project Setup and Proposal (May 13 to 16)
 We began by outlining the project objectives, required components, and timeline. A brief team meeting and documentation were completed, and we submitted the project proposal. This serves as our roadmap.


Design Phase (May 15 to 21)
 Simultaneously, we will work on UI design, UML and state diagrams, and set up the initial codebase. This ensures the design aligns across both the software (Python GUI and audio processing) and hardware (Arduino LED visualizers). Deliverables for this phase include interface mockups, diagrams detailing system behavior, and the framework for the code.


Design Completion Checkpoint (May 20)
 A formal review will occur to confirm the design is locked and development can proceed. We'll make any last-minute design adjustments during this checkpoint.


Implementation Phase (May 20 to 28)
 Both hardware (Arduino LED Visualizers) and software (GUI and audio processing) development occur in parallel. We aim to fully integrate the systems for synchronized audio-responsive behavior.


Implementation Completion Checkpoint (May 27)
 At this checkpoint, all functional components should be working together. We will demo a basic, integrated version of the system to verify progress.


Testing and Validation (May 27 to June 2)
 We'll conduct functionality tests, edge case handling, and performance checks. This includes unit testing code modules, verifying signal processing accuracy, and ensuring LEDs respond correctly to audio input.


Final Testing Checkpoint (June 1)
 This checkpoint confirms the system meets all intended goals. Final refinements will be made based on test results, and documentation will be finalized.


# Estimated Timeline

(Figure out what your major milestones for this project will be, including how long you anticipate it may take to reach that point)
The project will have 4 major milestones, one of which is already completed. We are using the Agile-Scrum Method.


# Anticipated Problems

Anticipated Problems
(Describe any problems you foresee that you will need to overcome)
1. Taking inputs from the microphone and computer audio.
2. Processing Audio data.
3. Sending serial data to Arduino .
4. Unit test for microphone inputs.
5. Unit test for C code.


Remember this is a living document is expected to be changed as you make progress on your project.
