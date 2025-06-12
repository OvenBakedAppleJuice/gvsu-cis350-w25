## High Level Project Tasks
This is a list of our high level tasks that need to be completed before finalizing the project.
Each task will contain a small description of what is to be done, if it is completed, expected time of completion, and who is resposible for the task.

## Tasks that remain: 

# Get the data to the arduino completely
- Some data is sent through properly but things like levels of frequencies are not
- Color input also needs to be adapted into the comms to the arduino
- Sensitivty should be adapted within python then sent to arduino, not computed in the ardiuno itself

Expected time to complete: 
End of this week, 6/13
Assigned to: __Joey__

# Find and fix all remaining bugs in the GUI
- There are probably minor bugs laying out that havent been found
- User testing could be an option for this

Expected time to complete: 
End of this week or next, 6/15 (preferably after the data communications is worked out)
Assigned to: __Josh and Joey__

# Get started on our next check-in
- Plans for our next check-in should be discussed very soon
- In need of a burn-down or up chart before final project turn in

Expected time to complete: 
Monday or Tuesday, After we pick our check-in date
Assigned to: __ALL__

# Any hidden issues with Ardiuno should be resolved
- There are some current comm issues on python end
- There could be issues on Ardiuno end, needs testing
- Verify both LED strings works the same
- 
Expected time to complete: 
End of Wednesday, preferably before all comm issues are solved
Assigned to: __Jason and Blake__ 

# Confirm whether we need an installer for the final product
- The GUI currently contains packages that need to be installed prior to running the program
- Find out if we need this before 6/12~

Expected time to complete: 
Should be asked during our check-in date
Assigned to: __Josh and Joey__

# Apply selected audio input to real input
- Currently the GUI allows you to pick from a list of the users current inputs but does not actually do anything
- Implement this audio input index into the usage of getting the audio data/values

Expected time to complete: 
Should be completed our check-in date
Assigned to: __Joey__

## Completed Tasks

# Setup Color mode and value output via HSV for ardiuno - Completed
- Make a color selector in the play_pause section
- Be able to grab the color value via HSV or translate a said value to HSV

Expected time to complete: 
2 days at most, suggest looking at premade color selectors
Assigned to: __Josh__

# Take pattern input and determine if requency or volume  - Completed
- Take Serial Input and find out the lenght

Expected time to complete: 
3 days at most
Assigned to: __Jason__

# Ardiuno needs to be able to take a color input - Completed
- Add a way, possibly another value that takes input for color

Expected time to complete: 
3 days at most, look into 1 value inputs for colors
Assigned to: __Jason__

# Add usage of the audio file selected to be able to work within the system - Completed
- Added a simple mp3 player inside the system for selected mp3 files
- Added play/pause, restart, change volume

Expected time to complete: 
Week at most, preferably 2-3 days
Assigned to: __Josh__

# Add ability to grab an audio file and import it to use for the audio input - Completed
- Be able to open the file explorer and grab an audio file
- Create a way to use said audio for audio input

Expected time to complete: 
Preferably 1 day
Assigned to: __Josh__

# Add user ability to select from a list of their audio inputs to use - Completed
- User should be able to select from all their audio inputs

Expected time to complete: 
1 day
Assigned to: __Josh__

# Generate Frequency on LEDs  - Completed
- Take Serial Input and have correct leds light up

Expected time to complete: 
3 days at most
Assigned to: __Jason__

# Generate Volume Bars on LEDs  - Completed
- Take Serial Input and have correct leds light up

Expected time to complete: 
3 days at most
Assigned to: __Jason__

# Read Serial Data and print to console  - Completed
- understand how to collect data 
- how to count number of inputs

Expected time to complete: 
3 days at most
Assigned to: __Jason__

# Create a button that allows the user to control the systems ability to grab audio data - Completed
- Simple start and stop button to stop data from flowing

Expected time to complete: 
2 days at most
Assigned to: __Josh__

# Create a visualizer/graph to show real input from the audio - Completed
- Create a graph that shows the frequency levels and their amplitude to each
- This would greatly help the user see real live input

Expected time to complete: 
4 days at most
Assigned to: __Joey__

# Get LED strip working with FASTled Libray  - Completed
- use example code to verfiy LEDs work 

Expected time to complete: 
3 days at most
Assigned to: __Jason__

# Wire LED to Arduino  - Completed
- use example code to verfiy LEDs work 

Expected time to complete: 
3 days at most
Assigned to: __Jason__

# Agree on the GUI layout - Completed
- Select a way to create a GUI
- Formulize a design/layout that we both understand and can work towards at the same time without conflicts

Expected time to complete: 
1 day
Assigned to: __Josh and Joey__

# Be able to get any data communication to the Ardiuno - Completed
- We need to ensure before starting most of our work that we can even properly communicate with the ardiuno

Expected time to complete: 
1 week
Assigned to: __Joey, Blake, and Jason__