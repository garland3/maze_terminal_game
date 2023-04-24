import curses
import random
import traceback
# add logging
import logging
from config import settings
from make_maze import create_maze
from ai import EducationExpert

logging.basicConfig(level=logging.DEBUG,  filename="mylog.log", filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

MAZE_SYMBOLS = {
    0: " ",
    1: "#",
    2: "*",
    3: "$"
}

class Player:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

class MazeGame:
    def __init__(self, maze_array):
        self.maze_array = maze_array
        self.player = None
        self.maze_chars = [[MAZE_SYMBOLS[x] for x in row] for row in self.maze_array]
    
    def create_player(self, start):
        self.player = Player(start[0], start[1], "P")
    
    def move_player(self, direction):
        if direction == "up":
            if self.maze_array[self.player.y-1][self.player.x] != 1:
                self.player.y -= 1
        elif direction == "down":
            if self.maze_array[self.player.y+1][self.player.x] != 1:
                self.player.y += 1
        elif direction == "left":
            if self.maze_array[self.player.y][self.player.x-1] != 1:
                self.player.x -= 1
        elif direction == "right":
            if self.maze_array[self.player.y][self.player.x+1] != 1:
                self.player.x += 1
    
    def is_game_over(self):
        return self.maze_array[self.player.y][self.player.x] == 3
    
    def display_game(self, screen):
        screen.clear()
        for i in range(len(self.maze_chars)):
            for j in range(len(self.maze_chars[i])):
                if i == self.player.y and j == self.player.x:
                    screen.addstr(i, j, self.player.symbol)
                else:
                    try:
                        screen.addstr(i, j, self.maze_chars[i][j])
                    except:
                        # print("Error:")
                        logging.debug("ERROR with addstr, i, j, maze_chars[i][j]", i, j, self.maze_chars[i][j])
                        # raise Exception("Error with addstr")
    
    def ask_a_question(self, screen):
        # Display pre-text and clear screen
        pre_text = "Question time! You must answer correctly to continue."
        screen.clear()
        screen.addstr(0, 0, pre_text)

        # Generate a question and answer
        ee = EducationExpert()
        q, a = ee.make_QA(settings.grade_level, topic=settings.question_topic)
        q = q.strip().strip("\n")
        a = a.lower()

        # Display the question and instructions
        show_text = f"Question: {q}"
        logging.info(f"The question is: {show_text}")
        instructions = "Type your answer."

        # Ask the user to answer the question
        while True:
            # Clear the screen and display the question and instructions
            screen.clear()
            screen.addstr(0, 0, pre_text)
            screen.addstr(1, 0, show_text)
            num_lines = show_text.count("\n")
            screen.addstr(num_lines+2, 0, instructions)

            # Get the user's answer and check if it's correct
            user_input = chr( screen.getch()).lower()
            # user_input = ''.join(c for c in user_input if)
            if  user_input.isalnum()==False:
                # just ignore it by continuing 
                continue
            if user_input == a:
                logging.info("Correct!")
                break
            else:
                logging.info(f"Incorrect. Answer was '{a}'. User input was '{user_input}'.")
                screen.addstr(num_lines+4, 0, "Incorrect. Try again.")

        
    
    def play(self):
        char_move_map = {
            curses.KEY_UP: "up",
            curses.KEY_DOWN: "down",
            curses.KEY_LEFT: "left",
            curses.KEY_RIGHT: "right",
            27: "quit", # 27 is the escape key
            113: "quit" # 113 is the q key
        }
        
        # Initialize curses
        screen = curses.initscr()
        curses.cbreak()
        screen.keypad(True)
        
        try:
            # Create the player
            start = None
            for i in range(len(self.maze_array)):
                for j in range(len(self.maze_array[i])):
                    if self.maze_array[i][j] == 2:
                        start = (j, i)
                        break
                if start is not None:
                    logging.info("Found start at {}".format(start))
                    break
            self.create_player(start)
            
            # Display the game state
            self.display_game(screen)

            cnt_sine_last_question = 0
            while True:
                # with probability 5%, ask a question
                if random.random() <settings.question_probability and cnt_sine_last_question > settings.moves_before_new_question_can_be_asked:
                    self.ask_a_question(screen)
                    self.display_game(screen)
                    cnt_sine_last_question = 0
                else:
                    cnt_sine_last_question += 1
                
                    # Wait for user
                
                # Wait for user input          
                char = screen.getch()
                # get text name of key
                if char in char_move_map:                    
                    name = char_move_map[char]
                    if name == "quit":
                        break
                    self.move_player(name)
                # Display the updated game state
                self.display_game(screen)
                # check if the game is over
                if self.is_game_over():
                    print("You win!")
                    break
        except Exception as e:
            logging.debug("ERROR: {}".format(e))
            logging.debug("Traceback: {}".format(traceback.format_exc()))
            # print(e)
            # print(traceback.format_exc())
        finally:
            # Clean up curses
            curses.nocbreak()
            screen.keypad(False)
            curses.echo()
            curses.endwin()
            logging.info("Finally called")

def main():
    print("Starting maze game...")
    width = settings.width
    height = settings.height
    
    maze_array, _, _ = create_maze(width, height)
    game = MazeGame(maze_array)
    print("Welcome to the maze game! Use the arrow keys to move. Press q to quit.")
    game.play()
    print("Thanks for playing!")
    
if   __name__ == "__main__":
    main()