import json
import time
import sys

#Add a wrong asnwers quiz review for missed questions

class QuizEngine:
    '''A 'test' class for the app to quiz users on questions from the questions path'''
    def __init__(self, questions_path: str, subject: str):
        self.questions_path: str = questions_path
        self.subject = subject.lower()
        #Wouldn't it be better to ask the user for the subject they want to do instead of passing the subject as an argument?...I can do that in the game loop now that I think about it
        self.users_score = 0
        '''Tracks the user's score'''
        self.current_question_index = 0
        '''A counter to track the current question in the questions list'''
        self.questions: list = self._load_questions()
        '''List that stores the unfiltered questions from the data source'''
        self.filtered_questions: list = self._load_filtered_questions()
        '''List that stores the questions in the specified subject'''
        self.current_question = self._get_current_question()
        '''The question at the current_question_index. If current_question is None, all the questions have been exhausted'''
        self.missed_questions = []
        '''A list to store all missed questions'''
    def _load_questions(self):
        '''Loads the questions (in the subject chosen) from the data source (currently a json file with testing data)'''
        with open(self.questions_path, 'r') as file:
            self.unfiltered_questions: list = json.load(file)
            '''The unfiltered questions from the data source'''
        return self.unfiltered_questions
    
    def _load_filtered_questions(self):
        self.filtered_questions: list = [question for question in self.unfiltered_questions if str(question['subject']).lower() == self.subject]
        return self.filtered_questions
    
    def _get_current_question(self):
        '''Returns the question (at the current index in the questions list) to be answered while there are still questions left to be answered. If all the questions have been answered, this function returns None'''
        if self.current_question_index < len(self.filtered_questions):
            return self.filtered_questions[self.current_question_index]
        # I can't remember why but I know not to use else statements in fuction definitions, since function definitions terminate at the first return statement encountered
        # It's called a guard clause or early exit statement and is use to make functions more concise, readable, and less redundant
        return None
    
    def _next_question(self):
        '''Increments the current question index (and updates the current question). Should be called after every attempt'''
        self.current_question_index += 1
        self.current_question = self._get_current_question() #Updates the current question
    
    def _check_answer(self, users_input: str):
        self.current_question = self._get_current_question()
        if not self.current_question:
            # Why aren't I  returning a message saying all the available questions have been attempted instead of returning False
            # Answer - Separation of concerns (displaying messages to the user is a front end concern). The backend (i.e) the quiz engine should only be concerned with logic.
            return False
        self.answer = self.current_question['correct_answer']
        if self.current_question["type"] == 'OBJ':
            for answer in self.answer:     
                if users_input.strip().lower() == str(answer).strip().lower(): # Casted to string in case the answer is an integer
                    self.users_score += 1
                    return True
            else:
                quiz_engine.missed_questions.append(self.current_question)
                return False
        elif self.current_question["type"] == 'THEORY':
            if users_input.strip().lower() == self.answer.strip().lower():
                return True
            else:
                quiz_engine.missed_questions.append(self.current_question)
                return False
        
with open(r'data\mock_data.json', 'r') as file:
    test_questions = json.load(file)

subjects_list = list(set([str(test_questions[number]['subject']).title() for number in range(len(test_questions))]))
subjects = ''
for subject in subjects_list:
    if subject != subjects_list[-1]:
        subjects += subject + ', '
    else:
        subjects += subject


if __name__ == '__main__':
    subject = input(f'Enter the subject you want to attempt' + f'(Currently available subjects are: {subjects}): ')
    while True:
        if subject.title() not in subjects:
            subject = input('Enter an available subject: ')
            continue
        elif subject.lower().strip() == 'q' or subject.lower().strip() == 'quit':
            sys.exit()
        else:
            break
    quiz_engine = QuizEngine(r'data\mock_data.json', subject)
    print("This is a beta test engine to check whether the logic works properly.")
    command = input("Enter 'start' or 's' to start and 'q' or 'quit' at any point to quit: ")
    command = command.strip().lower()
    while True:
        if command == 'start' or command == 's':
            print("Available quiz modes are study (which isn't timed and more casual) and exam mode (which simulates exam conditions).")
            quiz_mode = input("Choose a quiz mode before we proceed: ")
            while True:
                if quiz_mode.lower().strip() == 'study' or quiz_mode.lower().strip() == 'study mode':
                    break
                elif quiz_mode.lower().strip() == 'exam' or quiz_mode.lower().strip() == 'exam mode':
                    break
                elif quiz_mode.lower().strip() == 'q' or quiz_mode.lower().strip() == 'quit':
                    sys.exit()
                else:
                    quiz_mode = input("The quiz mode you entered isn't supported. Enter an available quiz mode: ")
                    continue
            print("I will give you random (test) NECO questions for you to answer (to confirm that the quiz engine works properly).")
            print("\nNote: For theory questions, you have to enter the command 'DONE' and the enter key when you are through writing to lock in your answer.\n")
            start = time.time()
            while quiz_engine.current_question:
                # While there is still a question that hasn't been answered yet
                print(f"{quiz_engine.current_question['subject']}: {quiz_engine.current_question['year']} {'Objective' if quiz_engine.current_question['type'] == 'OBJ' else 'Theory'}")
                print(f"{quiz_engine.current_question['question_number']}. {quiz_engine.current_question['question_text']}")
                if quiz_engine.current_question['options']:
                    for option in quiz_engine.current_question['options']:
                        print(f'\t{option}')
                if quiz_engine.current_question['type'] == "OBJ":
                    users_input = input('Enter your answer here: ')
                elif quiz_engine.current_question['type'] == 'THEORY':
                    print("This is a theory question. Type your answer below. When you are completely finished, type 'DONE' on a new line to submit.")
                    print("Enter your answer here: ", end='')
                    answer_lines = []
                    while True:
                        line = input()
                        if line.lower().strip() == 'done':
                            break
                        elif line.lower().strip() == 'q' or line.lower().strip() == 'quit':
                            sys.exit()
                        else:
                            answer_lines.append(line)
                    if len(users_input) != 1:
                        users_input = '\n'.join(answer_lines)
                    elif len(users_input) == 1:
                        users_input = answer_lines[0]
                users_input = users_input.strip().lower()
                if users_input == 'q' or users_input == 'quit':
                    print(f"Congratulations you got {quiz_engine.users_score} questions out of the {len(quiz_engine.filtered_questions)} available.")
                    print("Thanks for learning with me!")
                    sys.exit()
                correct = quiz_engine._check_answer(users_input)
                if correct:
                    if quiz_mode.lower().strip() == 'study' or quiz_mode.lower().strip() == 'study mode':
                        if quiz_engine.current_question['type'] == 'OBJ':
                            print(f"Correct! The answer is indeed: {quiz_engine.current_question['correct_answer'][0] if quiz_engine.current_question['correct_answer'] else ''}{': ' + quiz_engine.current_question['correct_answer'][1] if len(quiz_engine.current_question['correct_answer']) > 1 else ''}\n")
                        elif quiz_engine.current_question['type'] == 'THEORY':
                            print(f"Correct! The answer is indeed: {quiz_engine.current_question['correct_answer']}\n")
                        quiz_engine._next_question()
                        continue
                    elif quiz_mode.lower().strip() == 'exam' or quiz_mode.lower().split() == 'exam mode':
                        print('Answer recorded. ' + f'{'Moving on to the next question. \n' if quiz_engine.current_question_index < len(quiz_engine.filtered_questions) else ''}')
                        quiz_engine._next_question()
                        continue
                elif not correct:
                    if quiz_mode.lower().strip() == 'study' or quiz_mode.lower().strip() == 'study mode':
                        if quiz_engine.current_question['type'] == 'OBJ':
                            print(f"Incorrect. The correct answer is: {quiz_engine.current_question['correct_answer'][0] if quiz_engine.current_question['correct_answer'] else ''}{': ' + quiz_engine.current_question['correct_answer'][1] if len(quiz_engine.current_question['correct_answer']) > 1 else ''}\n")
                        elif quiz_engine.current_question['type'] == 'THEORY':
                            print(f"Incorrect. The correct answer is: {quiz_engine.current_question['correct_answer']}\n")
                        quiz_engine._next_question()
                        continue
                    elif quiz_mode.lower().strip() == 'exam' or quiz_mode.lower().split() == 'exam mode':
                        print("Answer recorded. " + f"{'Moving on to the next question. \n' if quiz_engine.current_question_index < len(quiz_engine.filtered_questions) else ''}")
                        quiz_engine._next_question()
                        continue
            # Add a review if in exam mode
            print(f"Congratulations you got {quiz_engine.users_score} questions out of the {len(quiz_engine.filtered_questions)} available, and you have finished all of the {len(quiz_engine.filtered_questions)} questions available.")
            end = time.time() 
            total_time = end - start
            minutes_used, seconds_used = divmod(total_time, 60)
            minutes_used, seconds_used = int(minutes_used), int(seconds_used)
            if minutes_used == 0:
                minutes_used = ''
            if seconds_used == 0:
                seconds_used = ''
            #print(f"You spent {str(minutes_used)}" + f'{' minutes and ' if minutes_used != '1' else ' minute ' if minutes_used != 0 else ''}' + f'{seconds_used if seconds_used != '0' else ''}' + f'{'seconds on' if seconds_used != '1' else 'seconds on' if seconds_used != 0 else ''}' + " this test.")
            #Make it print the time properly when the minutes_used or seconds_used is 0 and 1
            sys.exit()
        elif command.lower().strip() == 'q' or command.lower().strip() == 'quit':
            sys.exit()