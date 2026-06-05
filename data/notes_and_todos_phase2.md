# **Day 1: Thursday (Tonight) - The Foundation & Deployment**
## Your sole focus tonight is stabilizing the backend and securing your codebase in the cloud.

[ ] Fix the while loop condition that is crashing the Day 2 terminal engine.

[ ] Test the engine locally to ensure a quiz can be completed from start to finish without errors.

[ ] Run git add . and git commit -m "Fixed loop bug, completed Day 2 core logic".

[ ] Link your local repository to GitHub (git remote add origin...) and push the code (git push -u origin main).

[ ] Send the GitHub repository link to your brother to clear the deadline.

# **Day 2: Friday - Asset Sourcing & App Initialization**
## Setting up the visual building blocks and the invisible architecture.

[ ] Create an assets folder inside your project directory.

[ ] Download Google Material Icons (Study, Exam, Settings) in PNG format (light and dark versions) into the assets folder.

[ ] In app.py, define your global typography scale using ctk.CTkFont (H1, H2, Body, Subtext).

[ ] Initialize the customtkinter app window and configure its base resolution (e.g., app.geometry("1000x700")).

[ ] Configure the master .grid() layout for the main window so it resizes dynamically.

# **Day 3: Saturday - Screen 1 (The Dashboard)**
## Building the game lobby where she will set up her sessions.

[ ] Create the master CTkFrame for the dashboard.

[ ] Build the Mode Selection row: Add two large CTkButtons for Study and Exam mode using your CTkImage icons.

[ ] Build the Subject Selection grid: Create the nested frame and place the subject buttons inside.

[ ] Build the Year Selection grid directly below the subjects.

[ ] Add the "Start Session" CTA button at the bottom and create a Tkinter variable (ctk.StringVar()) to track her selections.

# **Day 4: Sunday - Screen 2 (The Active Quiz UI)**
## Constructing the distraction-free testing environment.

[ ] Create the second master CTkFrame for the quiz interface.

[ ] Build the Top Bar: Add the Question Counter label (left) and the Timer label (right).

[ ] Build the Content Area: Add a large, padded CTkLabel for the main question text.

[ ] Build the Input Area: Create CTkRadioButton widgets for multiple-choice options.

[ ] Build the Footer: Add the "Previous", "Next", and "Submit Exam" buttons.

# **Day 5: Monday - Screen 3 (The Review & Results UI)**
## Designing the feedback loop so she can actually learn from her mistakes.

[ ] Create the third master CTkFrame for the review screen.

[ ] Add a massive header label for the final Score Percentage.

[ ] Implement a CTkScrollableFrame in the center of the screen.

[ ] Create a placeholder layout inside the scrollable frame for missed questions (Question, Guessed Answer, Correct Answer, Explanation).

[ ] Add a "Return to Dashboard" button at the bottom.

# **Day 6: Tuesday - Navigation & State Management**
## Writing the logic that allows the user to click between the three screens.

[ ] Write a show_frame() function that hides the current screen and grids the requested screen.

[ ] Link the "Start Session" button on the Dashboard to transition to the Quiz UI.

[ ] Link the "Submit Exam" button on the Quiz UI to transition to the Review UI.

[ ] Link the "Return to Dashboard" button to transition back to the Start screen and clear all variables.

# **Day 7: Wednesday - The Great Integration**
## Wiring your beautiful frontend to your rugged backend engine.

[ ] Import your QuizEngine class into app.py.

[ ] Link the Dashboard selections (Subject, Year) so they pass the correct JSON file path into the QuizEngine when "Start Session" is clicked.

[ ] Program the "Next" button on the Quiz UI to pull the next question from the engine and dynamically update the UI text labels.

[] Program the "Submit Exam" button to pull the final grade and missed questions list from the engine, injecting that data into the Review UI's scrollable frame.