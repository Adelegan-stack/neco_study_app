import json
import time
import sys

GREEN = '\033[92m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'
BLACK  = '\033[90m'

class QuizEngine:
    '''A 'test' class for the app to quiz users on questions from the questions path'''
    def __init__(self, questions_path: str, subject: str):
        self.name = 'QuizEngine Bot'
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
        self.users_response = {}
        '''A dictionary that stores answered questions as keys, and users' response as values.'''

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
        self.users_response[self.current_question['id']] = users_input #Apparently you can't use dictioaries as keys so I will use the ID to get the question
        if self.current_question["type"] == 'OBJ':
            for answer in self.answer:     
                if users_input.strip().lower() == str(answer).strip().lower(): # Casted to string in case the answer is an integer
                    self.users_score += 1
                    return True
            else:
                self.missed_questions.append(self.current_question)
                return False
        elif self.current_question["type"] == 'THEORY':
            if users_input.strip().lower() == self.answer.strip().lower():
                self.users_score += 1
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

name = 'QuizEngine Bot'
if __name__ == '__main__':
    subject = input(f'{BLACK}{BOLD}{name}: {GREEN}Enter the subject you want to attempt' + f'(Currently available subjects are: {subjects}): ')
    while True:
        if subject.lower().strip() == 'q' or subject.lower().strip() == 'quit':
            print(f'{RESET}')
            sys.exit()
        elif subject.title() not in subjects_list:
            subject = input(f'{BLACK}{BOLD}{name}: {RED}Enter an available subject: {GREEN}')
            continue
        elif subject.title() in subjects_list:
            break
    quiz_engine = QuizEngine(r'data\mock_data.json', subject)
    print(f"{BLACK}{BOLD}{name}: {GREEN}This is a beta test engine to check whether the logic works properly.") # TODO - Learn how to pad text with zeroes and other f - string tricks
    command = input(f"{BLACK}{BOLD}{name}: {GREEN}Enter 'start' or 's' to start and 'q' or 'quit' at any point to quit: ")
    command = command.strip().lower()
    while True:
        if command == 'start' or command == 's':
            print(f"{BLACK}{BOLD}{name}: {GREEN}Available quiz modes are study (which isn't timed and more casual) and exam mode (which simulates exam conditions).")
            quiz_mode = input(f"{BLACK}{BOLD}{name}: {GREEN}Choose a quiz mode before we proceed: ")
            while True:
                if quiz_mode.lower().strip() == 'study' or quiz_mode.lower().strip() == 'study mode':
                    break
                elif quiz_mode.lower().strip() == 'exam' or quiz_mode.lower().strip() == 'exam mode':
                    break
                elif quiz_mode.lower().strip() == 'q' or quiz_mode.lower().strip() == 'quit':
                    print(f'{RESET}')
                    sys.exit()
                else:
                    quiz_mode = input("The quiz mode you entered isn't supported. Enter an available quiz mode: ")
                    continue
            print(f"{BLACK}{BOLD}{name}: {GREEN}I will give you random (test) NECO questions for you to answer (to confirm that the quiz engine works properly).")
            print(f"\n{BLACK}{BOLD}NOTE: {GREEN}For theory questions, you have to enter the command 'DONE' and the enter key when you are through writing to lock in your answer.\n")
            start = time.time()
            while quiz_engine.current_question:
                # While there is still a question that hasn't been answered yet
                print(f"{quiz_engine.current_question['subject']}: {quiz_engine.current_question['year']} {'Objective' if quiz_engine.current_question['type'] == 'OBJ' else 'Theory'}")
                print(f"{quiz_engine.current_question['question_number']}. {quiz_engine.current_question['question_text']}")
                if quiz_engine.current_question['options']:
                    for option in quiz_engine.current_question['options']:
                        print(f'\t{option}')
                if quiz_engine.current_question['type'] == "OBJ":
                    users_input = input(f'{BLACK}{BOLD}{name}: {GREEN}Enter your answer here: ')
                elif quiz_engine.current_question['type'] == 'THEORY':
                    print(f"{BLACK}{BOLD}{name}: {GREEN}This is a theory question. Type your answer below. When you are completely finished, type 'DONE' on a new line to submit.")
                    print(f"{BLACK}{BOLD}{name}: {GREEN}Enter your answer here: ", end='')
                    answer_lines = []
                    while True:
                        line = input()
                        if line.lower().strip() == 'done':
                            break
                        elif line.lower().strip() == 'q' or line.lower().strip() == 'quit':
                            print(f'{RESET}')
                            sys.exit()
                        else:
                            answer_lines.append(line)
                    if len(answer_lines) != 1:
                        users_input = '\n'.join(answer_lines)
                    elif len(answer_lines) == 1:
                        users_input = answer_lines[0]
                users_input = users_input.strip().lower()
                correct = quiz_engine._check_answer(users_input)
                if users_input == 'q' or users_input == 'quit':
                    print(f"{BLACK}{BOLD}{name}: {GREEN}Congratulations you got {quiz_engine.users_score} questions out of the {len(quiz_engine.filtered_questions)} available.")
                    print(f"{BLACK}{BOLD}{name}: {GREEN}Thanks for learning with me!")
                    print(f'{RESET}')
                    sys.exit()
                if correct:
                    if quiz_mode.lower().strip() == 'study' or quiz_mode.lower().strip() == 'study mode':
                        if quiz_engine.current_question['type'] == 'OBJ':
                            print(f"{BLACK}{BOLD}{name}: {GREEN}Correct! The answer is indeed: {quiz_engine.current_question['correct_answer'][0] if quiz_engine.current_question['correct_answer'] else ''}{' (' + quiz_engine.current_question['correct_answer'][1] if len(quiz_engine.current_question['correct_answer']) > 1 else ''})\n")
                        elif quiz_engine.current_question['type'] == 'THEORY':
                            print(f"{BLACK}{BOLD}{name}: {GREEN}Correct! The answer is indeed: {quiz_engine.current_question['correct_answer']}\n")
                        quiz_engine._next_question()
                        continue
                    elif quiz_mode.lower().strip() == 'exam' or quiz_mode.lower().split() == 'exam mode':
                        print(f'{BLACK}{BOLD}{name}: {GREEN}Answer recorded. ' + f'{'Moving on to the next question. \n' if quiz_engine.current_question_index < len(quiz_engine.filtered_questions) else ''}')
                        quiz_engine._next_question()
                        continue
                elif not correct:
                    if quiz_mode.lower().strip() == 'study' or quiz_mode.lower().strip() == 'study mode':
                        if quiz_engine.current_question['type'] == 'OBJ':
                            print(f"{BLACK}{BOLD}{name}: {RED}{BOLD}Incorrect! {RESET}{GREEN}The correct answer is: {quiz_engine.current_question['correct_answer'][0] if quiz_engine.current_question['correct_answer'] else ''}{' (' + quiz_engine.current_question['correct_answer'][1] if len(quiz_engine.current_question['correct_answer']) > 1 else ''})\n")
                        elif quiz_engine.current_question['type'] == 'THEORY':
                            print(f"{BLACK}{BOLD}{name}: {RED}{BOLD}Incorrect! {RESET}{GREEN}The correct answer is: {quiz_engine.current_question['correct_answer']}\n")
                        quiz_engine._next_question()
                        continue
                    elif quiz_mode.lower().strip() == 'exam' or quiz_mode.lower().split() == 'exam mode':
                        print(f"{BLACK}{BOLD}{name}: {GREEN}Answer recorded. " + f"{'Moving on to the next question. \n' if quiz_engine.current_question_index < len(quiz_engine.filtered_questions) else ''}")
                        quiz_engine._next_question()
                        continue
            if quiz_engine.missed_questions:
                print()
                print('-' * 40 + f"{BOLD}{'MISSED QUESTIONS REVIEW':^35}{RESET}{GREEN}" + '-' * 40) #Learn how to center this with ^
                for question in quiz_engine.missed_questions:
                    if question['type'] == 'OBJ':
                        print(f"\n{question['subject']}: {question['year']} {'Objective' if question['type'] == 'OBJ' else 'Theory'}")
                        print(f"{question['question_number']}. {question['question_text']}")
                        for option in question['options']:
                            print(f'\t{option}') 
                        print(f"{BLACK}{BOLD}{name}: {GREEN}This was your answer: {quiz_engine.users_response[question['id']]}")
                        print(f"{BLACK}{BOLD}{name}: {GREEN}The correct answer is: {question['correct_answer'][0] if question['correct_answer'] else ''}{' (' + question['correct_answer'][1] if len(question['correct_answer']) > 1 else ''})\n")
                    elif question['type'] == 'THEORY':
                        print(f"\n{question['subject']}: {question['year']} {'Objective' if question['type'] == 'OBJ' else 'Theory'}")
                        print(f"{question['question_number']}. {question['question_text']}")
                        print(f"{BLACK}{BOLD}{name}: {GREEN}Your answer was: {quiz_engine.users_response[question['id']]}")
                        print(f'{BLACK}{BOLD}{name}: {GREEN}The correct answer is: {question['correct_answer']}')
            end = time.time() 
            print(f"\n{BLACK}{BOLD}{name}: {GREEN}Congratulations! you got {quiz_engine.users_score} questions out of the {len(quiz_engine.filtered_questions)} available, and you have finished all of the {len(quiz_engine.filtered_questions)} questions available.")
            print(f'{BLACK}{BOLD}{name}: {GREEN}Thanks for learning with me!')
            total_time = end - start
            minutes_used, seconds_used = divmod(total_time, 60)
            minutes_used, seconds_used = int(minutes_used), int(seconds_used)
            if minutes_used == 0:
                minutes = ''
            elif minutes_used == 1:
                minutes = '1 minute and '
            else:
                minutes = f'{minutes_used} minutes and '
            if seconds_used == 0:
                seconds = ''
            elif seconds_used == 1:
                seconds = '1 second'
            else:
                seconds = f'{seconds_used} seconds'
            print(f'{BLACK}{BOLD}{name}: {GREEN}Time spent: ' + minutes + seconds + '.')
            print()
            if quiz_engine.missed_questions:
                print(f"{BLACK}{BOLD}{name}: {RED}Please, scroll back up to check the missed questions' review.{RESET}")
            sys.exit()
        elif command.lower().strip() == 'q' or command.lower().strip() == 'quit':
            print(f'{RESET}')
            sys.exit()
        else:
            command = input(f"{BLACK}{BOLD}{name}: {RESET}{RED}I didnt quite get that (available commands are 's' or 'start' to start and 'q' or 'quit' to exit at any point in time): ")
            continue
# Write comments in class tomorrow