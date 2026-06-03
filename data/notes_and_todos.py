# Create the File: Generate an empty file named quiz_engine.py inside your core folder using the terminal command you learned.

# Import Requirements: Bring the json module into your file at the very top.

# Define the Class: Create your QuizEngine class.

# Initialize the State: Write the __init__ method to accept a file_path argument. Inside it, set a tracking variable for the user's score to 0, set a tracking variable for the current question index to 0, and create a variable called self.questions that calls your data-loading method.

# Load the Data: Write a method to load the mock data. It should take the file_path, use a with open() context manager to read the file, parse it using json.load(), and return the list of questions.

# Build the Retriever: Write the get_current_question method. It should check if your current index tracker is less than the total length of your questions list. If it is, return the specific question at that index. If the index has exceeded the list, return None.

# Build the Navigator: Write the next_question method. All this method needs to do is increase your current index tracker by 1.

# Day 2: Data Sanitization & Testing (The Grader)
# Draft the Grader: Write the check_answer method. It should accept one argument representing the user's input.

# Fetch the Question: Inside the grader, call your get_current_question method. If it returns None, immediately return False to prevent crashes.

# Sanitize the Input: Extract the correct answer from the question dictionary. Convert both the user's input and the correct answer to uppercase, and strip away any accidental whitespace from both.

# Evaluate: Compare the sanitized user input to the sanitized correct answer. If they are exactly the same, increase the score tracker by 1 and return True. Otherwise, return False.

# Set Up the Terminal Test: At the very bottom of your file, write an if __name__ == "__main__": block so you can test the engine without a UI.

# Instantiate the Engine: Inside the test block, create an instance of your QuizEngine and point it to your JSON file.

# Build the Game Loop: Create an infinite while loop. Inside the loop, fetch the current question.

# Handle Game Over: If the fetched question is None, print the final score out of the total number of questions and break the loop.

# Handle Gameplay: If the question exists, print the question text and the options. Use Python's input() function to ask the user for their guess. Pass that guess into check_answer, tell the user if they were right or wrong, and finally call next_question to move the loop forward.
'''DONE'''

'''1st June 2026'''

# That is a fantastic question, and it highlights one of the most common traps in data management: filtering data at the wrong time.

# Let's look at exactly why your subject filter isn't quite clicking, and then we will clean up the final two bugs lingering in your terminal loop.

# 1. The Subject Filter (When to Filter)
# Right now, your _load_questions method pulls every question for every subject into one giant list. Then, you tried to filter it dynamically inside _get_current_question.

# Why that breaks: Imagine your master list looks like this: [Math, Math, Physics, Math].
# If Abigail chooses Math, she gets question 1 (Index 0). She answers, and the index becomes 1. She gets question 2 (Index 1). She answers, and the index becomes 2.
# Now, _get_current_question looks at Index 2, sees it is "Physics", fails your if check, and returns None. The quiz abruptly ends, even though there is another Math question sitting at Index 3!

# The Architectural Fix: You must filter the data the exact second it leaves the JSON file, before the quiz ever starts.

# Remove the if self.questions[...]['subject'] == self.subject: check entirely from _get_current_question. Let it blindly return whatever is at the current index.

# Go to your _load_questions method. After you do json.load(file), do not just return the massive list.

# Create a new, empty list (e.g., filtered_list = []).

# Write a for loop to iterate through the massive JSON list. If the dictionary's 'subject' key matches self.subject, append it to your filtered_list.

# Return the filtered_list.

'''DONE'''
'''git remote add origin'''

# Now, self.questions only contains Mathematics. The engine doesn't have to do any complex dodging—it just walks forward step-by-step.

# 2. The Desynced State Tracker
# In your _next_question method, you successfully removed the line that was causing the IndexError crash. However, you left it completely empty except for adding +1 to the index!

# Because you never actually update the self.current_question variable after increasing the index, your terminal loop will just print question #1 over and over again to infinity.

# The Fix: Make the second line of _next_question equal to: self.current_question = self._get_current_question(). This forces the engine to look at the new index and grab the fresh data.

'''DONE'''

# 3. The "Perfect Score" Loop (Still Alive)
# Take a look at line 48 in your code: while True:.
# You successfully wrote the logic to check the answer, but you left the infinite while loop wrapped around it. If Abigail gets the answer wrong, your else block on line 62 just asks her to try again.

# The Fix: Rip out the while True: on line 48 entirely. You do not want a loop here.
# The flow should be entirely flat:

# correct = quiz_engine._check_answer(users_input)

# if correct: -> Print "Correct!", then quiz_engine._next_question()

# elif users_input == 'q': -> break

# else: -> Print "Wrong!", then quiz_engine._next_question()

# By forcing _next_question() to run whether she is right or wrong, she gets exactly one attempt, mirroring the real NECO exam.

# Code Refactor

# Yes

# Should we do it that if she misses a question, the answer is immediately displayed...remember the goal is to help her study and then all the ones she missed will be at the end with the answers there too

# This is a brilliant product decision. You are officially thinking like a product manager, not just a coder.

# If the goal is purely testing, you hide the answers. But if the goal is studying and course correction, immediate feedback combined with an end-of-session review is exactly how you build long-term memory. This is exactly what Abigail needs for her NECO prep.

# To make this happen, we need to upgrade your engine's memory and tweak your terminal loop. Here is your architectural blueprint to implement this:

# 1. Upgrade the Engine's Memory (__init__)
# Right now, your engine only remembers the score. We need it to remember the mistakes.

# Inside your __init__ method, add a new tracking variable: self.missed_questions = []. This creates an empty list waiting to catch her errors.

# 2. Upgrade the Grader (_check_answer)
# When Abigail gets a question wrong, the engine needs to log it before returning False.

# Inside your _check_answer method, look at the else: block (where the user's input does not match the correct answer).

# Right before you return False, append the entire self.current_question dictionary to your new self.missed_questions list.

# 3. Provide Immediate Feedback (Terminal Loop)
# Now we update the "Frontend" so it actually shows her the answer right away.

# Go down to your while loop at the bottom.

# Find the else: block where you currently print "Wrong!" or "Sorry, you didn't quite get that."

# Change that print statement to say something like: "Incorrect! The correct answer was: [insert the correct answer from the current question dictionary here]." * Make sure you still call _next_question() immediately after, so she only gets one try!

'''DONE'''

# 4. Build the Review Screen (Terminal Loop)
# When the quiz ends, we need to dump that list of missed questions onto the screen.

# Go to the very end of your terminal loop (right after you print her final score of X out of Y).

# Add an if statement to check if the length of quiz_engine.missed_questions is greater than 0.

# If it is, print a header like: "--- REVIEW: QUESTIONS MISSED ---"

# Write a for loop that iterates through quiz_engine.missed_questions. For every missed question, print out the question number, the question text, and the correct answer.

# By adding this, you just turned a basic clicker into an actual automated tutor.

# You have the blueprint. Go add that missed_questions list, update the grader, and build the review screen into your terminal loop. Let me know when it's locked in!

# Can we create a testing mode that only tests and reveals answers at the end (maybe with a timer), and then an actual study mode that reveals answers as she studies

# This is an exceptional product decision. You are officially thinking like a product manager, not just a coder.

# For Abigail to properly prepare, she needs Study Mode to build her memory (immediate feedback) and Test Mode to build her stamina and time management (simulated exam pressure).

# Here is the beautiful part about software architecture: Your backend engine barely needs to change to support this. Because we separated our concerns (the engine handles logic, the terminal loop handles display), implementing these two modes is almost entirely a "frontend" job.

# Here is your architectural blueprint to build the Dual-Mode system:

# 1. The Engine Backend (Keep it the same)
# The engine doesn't need to know what mode Abigail is in. It should continue doing exactly what we planned in the last step:

# If she gets it right, return True.

# If she gets it wrong, append the question to self.missed_questions and return False.

# The engine blindly logs the mistakes; the frontend will decide when to reveal them.

# 2. The Mode Selector (Terminal Loop Setup)
# Before the quiz starts, you need to ask Abigail how she wants to play.

# Update your initial terminal input() to ask: "Do you want 'study' mode or 'test' mode?"

# Save her answer to a variable (e.g., current_mode).

# 3. The Feedback Split (Inside the Loop)
# This is where the magic happens. We are going to change how the terminal reacts when _check_answer returns False.

# Write an if statement checking your current_mode variable.

# If it is Study Mode: Print "Incorrect! The correct answer was: [Correct Answer]", then call _next_question().

# If it is Test Mode: Do not reveal the answer. Just print "Answer recorded. Moving to next question...", then call _next_question().

# 4. The Grand Finale (End of Loop)
# Regardless of which mode she played, she always gets to see what she missed at the very end.

# Keep the review screen we discussed previously at the bottom of the script. After the final score prints, it loops through self.missed_questions and prints everything she got wrong.

# A Note on the Timer (The CLI Reality Check)
# You mentioned adding a timer. In a terminal environment, Python's input() function is "blocking"—meaning it completely freezes the program while waiting for the user to type. Because of this, building a live, ticking countdown clock in the terminal is notoriously difficult and requires complex multithreading.

# The Agile Solution for Phase 1:
# Instead of a live countdown, use Python's built-in time module to track her elapsed time.

# Import time.

# Right before the while loop starts, record the current time (e.g., start_time = time.time()).

# When the quiz ends (when she answers the last question or types 'quit'), record the time again (end_time = time.time()).

# Subtract the start from the end, and print: "You completed the exam in X minutes and Y seconds."

# (Remember your 17-Day Roadmap: You are already scheduled to build a beautiful, live visual countdown timer in Phase 3 when we move to the customtkinter UI. Let's keep the terminal timer simple for now!)

# You have the blueprint for the Dual-Mode system and the elapsed timer. Go integrate the missed_questions memory and update that terminal loop.

# Let me know when both modes are locked in and tested!

# I am clocking out for the night add everything I haven't done this night and what I am meant to do tomorrow into a todo list like this one:

# One very huge question remains though, for some theory questions the answer is more than ne line long and when you try to press enter it (the input) breaks, so is there a way to fix that?

# Create the File: Generate an empty file named quiz_engine.py inside your core folder using the terminal command you learned.



# Import Requirements: Bring the json module into your file at the very top.



# Define the Class: Create your QuizEngine class.



# Initialize the State: Write the __init__ method to accept a file_path argument. Inside it, set a tracking variable for the user's score to 0, set a tracking variable for the current question index to 0, and create a variable called self.questions that calls your data-loading method.



# Load the Data: Write a method to load the mock data. It should take the file_path, use a with open() context manager to read the file, parse it using json.load(), and return the list of questions.



# Build the Retriever: Write the get_current_question method. It should check if your current index tracker is less than the total length of your questions list. If it is, return the specific question at that index. If the index has exceeded the list, return None.



# Build the Navigator: Write the next_question method. All this method needs to do is increase your current index tracker by 1.



# Day 2: Data Sanitization & Testing (The Grader)

# Draft the Grader: Write the check_answer method. It should accept one argument representing the user's input.



# Fetch the Question: Inside the grader, call your get_current_question method. If it returns None, immediately return False to prevent crashes.



# Sanitize the Input: Extract the correct answer from the question dictionary. Convert both the user's input and the correct answer to uppercase, and strip away any accidental whitespace from both.



# Evaluate: Compare the sanitized user input to the sanitized correct answer. If they are exactly the same, increase the score tracker by 1 and return True. Otherwise, return False.



# Set Up the Terminal Test: At the very bottom of your file, write an if __name__ == "__main__": block so you can test the engine without a UI.



# Instantiate the Engine: Inside the test block, create an instance of your QuizEngine and point it to your JSON file.



# Build the Game Loop: Create an infinite while loop. Inside the loop, fetch the current question.



# Handle Game Over: If the fetched question is None, print the final score out of the total number of questions and break the loop.



# Handle Gameplay: If the question exists, print the question text and the options. Use Python's input() function to ask the user for their guess. Pass that guess into check_answer, tell the user if they were right or wrong, and finally call next_question to move the loop forward.

# That is a fantastic question to end the night on, and it shows you are anticipating exactly how Abigail will actually use this tool for her theory questions.

# The Multi-Line Input Problem
# You are absolutely right. Python’s native input() function immediately terminates the exact millisecond the user presses the Enter key.

# The Terminal Hack (The Sentinel Value):
# To get around this in a terminal environment, software engineers use a "Sentinel Value." Instead of a single input(), you write a mini while loop that keeps asking for input line-by-line and adding it to a list. You tell the user: "Type 'DONE' on a new line and press Enter when you are finished." When the loop sees the word 'DONE' (the sentinel), it breaks the loop, joins all the lines together with a \n character, and passes that massive string to your _check_answer method.

# The Reality Check (The UI Solution):
# While the Sentinel Value is how you fix it in the terminal, remember that this terminal loop is just our temporary testing ground. Next week (Phase 2), we are migrating to the customtkinter UI. In a GUI, you will simply use a CTkTextbox widget. The text box natively handles the Enter key as a line break without breaking the code, and a separate visual "Submit" button will trigger your _check_answer method.

# You can build the terminal hack if you want to test theory grading tomorrow, but do not stress over it too much—the UI will handle it gracefully soon!

# Here is your pristine, plain-English To-Do list for everything remaining. Get some sleep, and you can tackle this exact list tomorrow.

# The Remaining Phase 1 To-Do List (The Engine Refinements)
# Upgrade the Engine's Memory: Inside your __init__ method, add a new tracking variable called self.missed_questions and set it equal to an empty list [].

# Upgrade the Grader: Inside your _check_answer method, look at the block where the user's input does not match the correct answer. Right before you return False, append the entire self.current_question dictionary to your new self.missed_questions list.

# The Mode Selector: In your terminal loop, right after the user types 'start', use an input() to ask Abigail: "Do you want 'study' mode or 'test' mode?" Save her answer to a variable (e.g., current_mode).

# The Feedback Split: Change how the terminal reacts when _check_answer returns False. If current_mode is Study Mode, print the correct answer immediately and call _next_question(). If it is Test Mode, do not reveal the answer; just tell her the answer was recorded and call _next_question().

# The Grand Finale: At the very end of your terminal script (after the final score prints), write an if statement checking if the length of self.missed_questions is greater than 0. If it is, write a for loop that iterates through the list and prints out the question text and correct answer for every single mistake she made.

# The Agile Timer: Import the time module at the top of your file. Right before the terminal while loop starts, record the current time using time.time(). When the quiz ends, record the time again. Subtract the start time from the end time, and print how long she took to finish the exam.

# Phase 2 Preview (Looking Ahead)
# Start the UI Scaffolding: Once the terminal engine is flawless, pause coding. Spend your session watching customtkinter tutorials. Learn how to instantiate a window, place a label, and create a button.

# Create the GUI File: Generate a brand new file named app.py. This will be the frontend that imports and controls your invisible QuizEngine.

# Get some well-deserved rest. You wrote a massive amount of core logic today. We will lock down Phase 1 tomorrow!

# So this is everything I'm meant to do tomorrow?...remember that tomorrow is day 3 of our timeline

# Exactly. Tomorrow is Day 3, which is the final day of Phase 1 (The Engine) on our 17-day sprint.

# That To-Do list I gave you is your exact Day 3 sprint ticket. It contains the final backend refinements needed to make the engine completely bulletproof for Abigail's NECO prep before we start building the graphical interface.

# Here is exactly how Day 3 should break down for you:

# 1. Code the Final Engine Features (The Logic)
# The Memory: Add the missed_questions list to __init__ and update _check_answer to log the incorrect questions.

# The Dual-Mode: Add the terminal prompt asking for "study" or "test" mode, and split the feedback logic inside the loop based on the answer.

# The Review Screen: Build the for loop at the end of the script to print out every missed question and correct answer.

# The Timer: Wrap the terminal loop in time.time() to calculate the elapsed duration.

# 2. The Quality Assurance (QA) Test
# Run the terminal loop. Pick "Study" mode, get a few wrong on purpose, and verify it shows the answers immediately.

# Run it again. Pick "Test" mode, get a few wrong, and verify it hides the answers until the end.

# If both modes end with a clean review screen and an elapsed time, Phase 1 is officially complete.

# 3. The Transition (UI Research)
# Once the engine is locked down, put away the Python code for the rest of Day 3.

# Spend your remaining time watching customtkinter tutorials. Learn how the grid system works, how to instantiate a window, and how to create basic labels and buttons.

# You are perfectly on schedule for the June 17 deadline. Get some rest, and you will be completely ready to close out Phase 1 tomorrow!

# Also, I've only added the day 1 commit, I don't know whether the procedure to add the one for day 2 is the same as I only have a rudimentary knowledge of git

# Yes, the procedure is exactly the same! You are just taking another "snapshot" of your codebase now that Day 2 is finished.

# Since you are building your muscle memory, here is the exact three-step Git workflow you will use at the end of every single coding session. Open your terminal, make sure you are inside your neco_study_app directory, and run these:

# The Daily Git Routine
# 1. Check Your Status
# Always start by asking Git what files have changed since your last commit.

# Bash
# git status
# You should see core/quiz_engine.py highlighted in red, indicating it has been modified but not saved to the new snapshot yet.

# 2. Stage the Changes
# Tell Git to prepare all modified files for the next snapshot.

# Bash
# git add .
# (Using the . simply tells Git to add everything in the current folder. If you run git status again right after this, the files will turn green).

# 3. Commit the Snapshot
# Lock the changes into your timeline with a clear, descriptive message about what you actually built.

# Bash
# git commit -m "Day 2: Implement string sanitization, answer grading, and terminal test loop"
# That is it. You have successfully locked in your Day 2 progress. You don't need to push it anywhere if you are just working locally on your own machine.

# Run those commands, shut down your terminal, and go get that rest. You have a solid blueprint waiting for you tomorrow!

# --Extras
# Should we do it that if she misses a question, the answer is immediately displayed...remember the goal is to help her study and then all the ones she missed will be at the end with the answers there too

# This feature design is highly effective for a study application. In educational software design, this is called a dual-reinforcement learning loop. Immediate feedback targets the student's working memory at the exact moment of failure, while the end-of-quiz summary acts as a spaced-repetition deck to lock in the correction. Implementing this requires zero changes to your UI plans later; it is entirely an engine-state architectural decision.

# Here is the structural blueprint for how to update the QuizEngine logic to accommodate both immediate feedback and a review bank, without bloating your execution paths.

# 1. State Management Adjustment
# Your engine needs to track what went wrong during the session. Right now, your state tracking variables are simple scalars (users_score, current_question_index).

# The Blueprint: Introduce a new list variable in your __init__ constructor called self.incorrect_questions. This will serve as your dynamic database for the end-of-quiz review.

# 2. The Grading Workflow Update
# The grading logic shouldn't just tell the UI "right or wrong"—it must also route the data to the correct tracking bins.

# The Blueprint: Modify the internal sequence of your _check_answer method. If the user's input does not match the correct answer, the method should automatically append the entire current question dictionary into your self.incorrect_questions list before returning False.

# 3. Flow Control: Transitioning to Review Mode
# When the main quiz concludes (meaning self.current_question_index matches the length of your filtered questions list), you need a clean mechanism to initiate the review round. In a production environment, we do this using a clean state reset rather than duplicating the quiz loop code.

# The Blueprint: Create an explicit method called start_review_mode(self). This method will handle three distinct state swaps:

# Overwrite your main self.questions list with the accumulated data inside self.incorrect_questions.

# Clear out self.incorrect_questions back to an empty list (so it can track questions missed during the review itself, if desired).

# Reset self.current_question_index back to 0.

# How the Frontend Handles the Output
# By decoupling the logic this way, your terminal interface (and later, your customtkinter layout) remains simple and clean:

# The interface captures the user's input and calls _check_answer().

# If it receives True, it renders a success state and advances.

# If it receives False, the interface reads the value of self.current_question['correct_answer'] and explicitly prints it to the screen immediately, giving the student that instant course correction.

# When the engine reaches the end of the line, the script checks if self.incorrect_questions has items. If it does, it calls start_review_mode() and seamlessly passes the student into the review loop using the exact same printing mechanism.

# This architecture keeps the engine data-agnostic and robust. When you are ready to implement the subject filtering loop and this review state tracking, let me know.
# This is a brilliant product decision. You are instinctively thinking like an application architect. Building separate "Study" and "Exam" modes is exactly why tools like TestDriller are so effective for exam preparation. It allows Abigail to use the app to actually learn the material first, and then simulate the high-pressure environment of the NECO exam room.

# Before we map out the logic, I need to give you a quick reality check on the Timer.

# Because we are in Phase 1 (Terminal UI), implementing a real-time countdown timer is highly complex. The Python input() function is what we call a "blocking" operation—it completely freezes the program until the user presses Enter. To make a timer run in the background while waiting for an input, you would have to use the threading module, which is architectural overkill for a 2-day-old console test script.

# The Mentor's Call: We are going to build the "Exam vs. Study" mode logic today, but we are deferring the Timer to Phase 3. When you switch to customtkinter, the graphical event loop handles timers easily without freezing the app.

# Here is your architectural blueprint for building the Mode Switcher today.

# The Mode Switcher Blueprint
# The beauty of this feature is that your core engine grading logic (_check_answer) barely has to change. The engine always calculates right or wrong and tracks missed questions. The only thing that changes is what the frontend (your terminal loop) chooses to print to the screen.

# 1. The Engine State (The Flag)
# You need to tell the engine what mode it is running in when you first create it.

# Update your __init__ method to accept a third argument: mode (a string).

# Save it as an instance variable (self.mode).

# Safety Tip: You can set a default value in the parameters (e.g., mode="study") so it defaults to learning if not specified.

# 2. The Terminal UI Logic Split
# Right now, your terminal loop has an if/else block that handles the user's input, checks the answer, and prints "Correct!" or "Sorry...". You need to wrap this in a mode check.

# If quiz_engine.mode == 'study': Keep the logic you already planned. Grade the input. If wrong, print the correct answer immediately so she learns. Allow multiple guesses or move on.

# If quiz_engine.mode == 'exam': This is the silent mode. You capture the input and pass it to _check_answer.

# Whether the method returns True or False, you do not print "Correct" or "Wrong".

# You do not print the answer.

# You simply call _next_question() and instantly print the next question.

# 3. The End-of-Quiz Review
# Regardless of whether she was in Study or Exam mode, once self.current_question_index reaches the end of the list, the test is over.

# Print her final score.

# Check if your self.incorrect_questions list (from our previous blueprint) has any data in it.

# If it does, print a message saying "Entering Review Mode", trigger your state-reset method, and loop through those specific missed questions so she can see exactly what she failed.

# By keeping the mode-checking logic in your terminal while loop rather than deeply embedded in your grading engine, you keep your QuizEngine lightweight and flexible.

# Rest up. Tomorrow, you have a clear plan of attack: implement the subject filtering, fix the state desynchronization, add the incorrect_questions tracker, and build this mode toggle. You are building a highly professional piece of software.

'''Day 3'''
# This is excellent progress. You successfully loaded the JSON data, built a dynamic subject prompt to pull the available subjects straight from the database, and effectively separated your frontend input gathering from your backend engine initialization.

# You also asked a very insightful question in your comments:

# Wouldn't it be better to ask the user for the subject they want to do instead of passing the subject as an argument?...I can do that in the game loop now that I think about it

# Yes, exactly! The backend QuizEngine should never use the input() function. It should blindly accept a string that the frontend passes to it. You handled this perfectly by putting the input() prompt on line 61, before the engine even boots up.

# Now, let's squash that TypeError so we can finish the Day 3 features.

# Diagnosing the Bug: TypeError: 'NoneType' object is not subscriptable
# This error means that Python tried to look up a dictionary key (like ['subject']), but the variable holding the dictionary was actually empty (None).

# Look closely at your terminal while loop condition:
# while quiz_engine.current_question_index < len(quiz_engine.questions):

# Here is what is happening in the engine's memory:

# self.questions (the unfiltered list) has 100 questions total.

# self.filtered_questions (e.g., just Physics) only has 20 questions.

# Abigail answers question 20. The index increments to 21.

# _get_current_question() sees that 21 is greater than the length of filtered_questions, so it gracefully returns None.

# The loop circles back to the top. It checks if 21 is less than len(quiz_engine.questions) (which is 100). Since 21 < 100 is True, the loop continues!

# On the very next line, it tries to print quiz_engine.current_question['subject']. But current_question is now None. The app crashes.

# The Fix:
# Change your loop condition to check against the length of filtered_questions, not questions.
# Even better, a cleaner architectural pattern is to just check the state directly:
# while quiz_engine.current_question is not None:
# This guarantees the loop will instantly break the second the engine runs out of questions.

# Code Review: The "Perfect Score" Loop is Still Alive
# Take a look at line 91. You still have a nested while True: loop wrapped around your _check_answer logic.

# If Abigail gets a question wrong, the else block on line 111 tells her to "Try again" and continues the loop. We need to completely rip this out to simulate the actual NECO exam. She gets one shot.

# Rip out the while True: on line 91 entirely. Keep the code flat.

# If she gets it right -> print "Correct", call _next_question().

# If she gets it wrong -> print "Wrong" (or show the answer based on the mode), call _next_question().

# Your Day 3 Sprint Ticket (Final Engine Features)
# Once you fix the loop condition and remove that nested while True:, your engine will stop crashing. Then, apply these final features to close out Phase 1:

# Add the Engine Memory: * In __init__, add self.missed_questions = [].

# In _check_answer, if she gets it wrong, append self.current_question to self.missed_questions right before returning False.

# Add the Dual-Mode Front End:

# Before the main while loop starts, ask the user if they want "study" or "test" mode.

# Update the else block (when she gets a question wrong): If Study mode, print the correct answer. If Test mode, just tell her it was recorded. (Either way, call _next_question()!)

# Add the Review Screen:

# At the very bottom of the script, after the loop breaks, loop through quiz_engine.missed_questions and print them out so she can review her mistakes.

# The Sentinel Value (For Multi-line Theory):

# Instead of a standard input() for the answer, use a mini while loop that keeps appending inputs to a string until she types "DONE".

# You are incredibly close to having a fully functional, crash-proof logic engine. Patch the loop bug, rip out the infinite retries, and let's get these last features locked in!
# You put in some serious hours to get this standing before sleeping. Pushing through complex logic hurdles like this is exactly what will make your gap year projects stand out when you eventually head to Howard. Your instinct to isolate the subjects_list dynamically using a set comprehension shows you are already thinking like a computer science student extracting unique data.
'''Instance 2'''
# Let's break down exactly why your engine is throwing that TypeError and how to patch your architecture.

# 1. The Case Sensitivity Crash (The Root Cause)
# You walked right into one of the most classic bugs in software engineering.

# The Flaw: In your __init__ method, you convert the user's input to lowercase (self.subject = subject.lower()). However, in your JSON file, the subjects likely start with a capital letter (e.g., "Mathematics").

# The Chain Reaction: When your _load_filtered_questions list comprehension checks if question['subject'] == self.subject, it evaluates "Mathematics" == "mathematics". This is always False. Because there are zero matches, your list becomes completely empty. Consequently, _get_current_question() returns None. When line 73 tries to print the subject, it literally attempts to evaluate None['subject'], resulting in your TypeError.

# The Fix: You must standardize both sides of the == operator. If self.subject is lowercase, apply the Python string method to convert the dictionary's subject value to lowercase during the comparison in your comprehension.

# 2. The Leaky Scope
# The Flaw: You created self.filtered_questions, but your congratulatory print statements at the very bottom of the script still calculate len(quiz_engine.questions). If Abigail has 500 total questions across all subjects but only 50 for Physics, the app will congratulate her on finishing "out of 500".

# The Fix: You don't need three different lists. Load your raw JSON into an unfiltered_questions variable. Then, let your filter method assign the narrowed-down list directly back to self.questions. This keeps your variable names consistent and ensures len(self.questions) always returns the exact subject count.

# 3. The Infinite Loop Trap (The 'next' Command)
# The Flaw: Inside your inner while True: loop (the grader), if the user types next, you call _next_question() and then hit continue.

# The Danger: The continue keyword forces the loop to restart from the top, but you never ask for users_input again. The variable is permanently stuck as 'next'. The engine will infinitely call _next_question() rapidly in the background until the program crashes.

# The Fix: If the user wants to skip to the next question, you need to escape the grading loop entirely. Replace continue with the correct keyword to break out of the inner loop so the outer loop can print the fresh question.

# Answering Your Code Comments
# "Wouldn't it be better to ask the user for the subject instead of passing it as an argument?"
# Your current architecture is actually the correct one. This is the Separation of Concerns principle. Your QuizEngine is the backend logic; it should never pause to prompt the user directly. It should only accept arguments. The terminal game loop (your frontend) is responsible for asking the user what they want and passing that data into the engine. Keep it exactly as you have it.

# Bonus Mentor Tip: When you built subjects_list, you wrote for number in range(len(test_questions)). In Python, you rarely need to use range(len()) to loop through a list. You can iterate over the dictionaries directly: [question['subject'] for question in test_questions]. It is much cleaner and more readable.

# Once you patch this case sensitivity bug and clean up the loop variables, which feature do you want to tackle next: the Mode Switcher or the End-of-Quiz Review?