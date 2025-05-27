## Use Case Diagram Description
Handle (Functional{number})

# User
An actor that handles the functions in the GUI,
The user can handle the state of the system
1. Turn On/Off (F14)
2. Select different modes (F11)
3. Choose audio source (F4, F5)

# Audio Input
An actor that handles input from a microphone
The microphone handles the live audio input after the user selects an audio source
1. Input from microphone (F9, F10)

# LED Controller
This actor controls the LED and simply that (F3)

# System Computer
This actor handles functionality from inbedded systems
1. Pulling system audio from a file (F5)
2. Getting signals from a microphone connected to the computer (F2, F7, F12)

# GUI
Allows the user direct control over what the system will do
1. Shows values coming from the microphone (F15)
2. Allows the user to select a mode (F11)
3. Allows the user to select an audio source (F4, F5)



