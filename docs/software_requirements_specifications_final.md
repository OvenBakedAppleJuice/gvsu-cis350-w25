# Overview

The purpose of this document is to highlight the functionalities, behaviors, and capabilities of Jotter, a text editor application. Jotter aims to provide users with a simple, efficient, and user-friendly text editor that balances functionality and ease of use.


# Software Requirements

This section outlines the essential requirements for the software application, encompassing both functional and non-functional aspects necessary for successful development, deployment, and usage.

## Functional Requirements

### Text Editing

| ID  | Requirement     | 
| :-------------: | :----------: | 
| FR1 | The user shall be able to create a new text document |
| FR2 | The user shall be able to edit the text document. |
| FR3 | The user shall be able to format text (bold, italic, underline, strikethrough). |
| FR4 | The user shall be able to change text alignment (left, center, right, justify). |
| FR5 | The user shall be able to create ordered and unordered lists. | 
| FR6 | The user shall be able to insert and remove hyperlinks. | 
| FR7 | The user shall be able to change the font size. | 
| FR8 | The user shall be able to change text color and highlight color. | 


### File Operations

| ID  | Requirement     | 
| :-------------: | :----------: | 
| FR9 | The user shall be able to save their text document locally. | 
| FR10 | The user shall be able to save the document in different formats (txt, pdf, md, docx). | 
| FR11 | The user shall be able to load an existing text document. | 
| FR12 | The user shall be able to override an existing file or create a new file if it already exists. | 
| FR13 | The user shall be able to choose the location to save their files. | 


### Undo/Redo

| ID  | Requirement     | 
| :-------------: | :----------: | 
| FR14 | The user shall be able to undo the last action. | 
| FR15 | The user shall be able to redo the last undone action. | 
| FR16 | The user shall be able to perform multiple undos and redos in a row. | 
| FR17 | The application shall ignore undo or redo commands when no such actions are available. | 
| FR18 | The application shall preserve undo/redo history during the current editing session until the file is closed or reset. | 


### User Interface
| ID  | Requirement     | 
| :-------------: | :----------: | 
| FR19 | The user shall be able to interact with the application through a graphical user interface (GUI). | 
| FR20 | The user shall be able to use a toolbar to access text formatting and file operation features. | 
| FR21 | The user shall be able to use a modal to save files and choose the save location. | 


## Non-Functional Requirements

### Performance

| ID  | Requirement     | 
| :-------------: | :----------: | 
| NFR1 | The application shall load and save files within 2 seconds. | 
| NFR2 | The application shall handle text documents up to 10,000 words without performance degradation. | 
| NFR3 | The application shall remain responsive under high memory or CPU usage. | 
| NFR4 | The application shall initialize the user interface within 3 seconds after launch. | 
| NFR5 | The application shall execute formatting operations (e.g., bold, italic, underline) instantly within 1 second of the formatting button being pressed. | 


### Usability

| ID  | Requirement     | 
| :-------------: | :----------: | 
| NFR6 | The application shall have an intuitive and user-friendly interface.| 
| NFR7 | The application shall provide tooltips for all toolbar buttons.| 
| NFR8 | The application shall be able to be used in light and dark mode themes.| 
| NFR9 | The application shall be able to indicate when formatting is active.|
| NFR10 | The application shall be able to be show all active formatting when respective text is selected. | 


### Compatibility

| ID  | Requirement     | 
| :-------------: | :----------: | 
| NFR11 | The application shall be responsive and work on different screen sizes (desktop, tablet, mobile).| 
| NFR12 | The application shall be compatible with modern web browsers (Chrome, Firefox, Safari, Edge).| 
| NFR13 | The application shall be compatible with most popular Oerating Systems (Mac, Windows, Linux) | 
| NFR14 | The application shall maintain consistent functionality and appearance across different device orientations (portrait and landscape). |
| NFR15 | The application shall function reliably in environments with varying internet speeds, including slower or unstable connections. |



# Software Artifacts

This section outlines the key deliverables and artifacts produced throughout the software development lifecycle.

[Use Case Diagram](../artifacts/use_case_diagram/Text-Editor_Use-Case.drawio.png)

[Sequence Diagrams](../artifacts/sequence%20_diagram/)

[Class Diagram](../artifacts/class_diagram/ClassDiagram.png)



