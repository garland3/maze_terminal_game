import curses
import traceback
from make_maze import convert_array_to_maze, create_maze
# add logging
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename="mylog.log")



class Player:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

class MazeGame:
    def __init__(self, maze):
        self.maze = maze
        self.player = None
    
    def create_player(self, start):
        self.player = Player(start[0], start[1], "P")
    
    def move_player(self, direction):
        if direction == "up":
            if self.maze[self.player.y-1][self.player.x] != "#":
                self.player.y -= 1
        elif direction == "down":
            if self.maze[self.player.y+1][self.player.x] != "#":
                self.player.y += 1
        elif direction == "left":
            if self.maze[self.player.y][self.player.x-1] != "#":
                self.player.x -= 1
        elif direction == "right":
            if self.maze[self.player.y][self.player.x+1] != "#":
                self.player.x += 1
    
    def is_game_over(self):
        return self.maze[self.player.y][self.player.x] == "$"
    
    def display_game(self, screen):
        screen.clear()
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if i == self.player.y and j == self.player.x:
                    screen.addstr(i, j, self.player.symbol)
                else:
                    try:
                        screen.addstr(i, j, self.maze[i][j])
                    except:
                        # print("Error:")
                        logging.debug("ERROR with addstr, i, j, maze[i][j]", i, j, self.maze[i][j])
                        # raise Exception("Error with addstr")
    
    def play(self):
        # Initialize curses
        screen = curses.initscr()
        curses.cbreak()
        screen.keypad(True)
        char_move_map = {
            curses.KEY_UP: "up",
            curses.KEY_DOWN: "down",
            curses.KEY_LEFT: "left",
            curses.KEY_RIGHT: "right",
            27: "quit", # 27 is the escape key
            113: "quit" # 113 is the q key
        }
        inverse_char_move_map = {v: k for k, v in char_move_map.items()}
        try:
            # Create the player
            maze_array, start, _ = create_maze(31, 21)
            self.create_player(start)
            
            # Convert maze array to maze string
            self.maze = convert_array_to_maze(maze_array, verbose=True)
            
            # Display the game state
            self.display_game(screen)

            while True:
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

if __name__ == "__main__":
    game = MazeGame(None)
    game.play()