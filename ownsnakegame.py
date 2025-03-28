from tkinter import *
from tkinter import messagebox
import random

WIDTH = 500
HEIGHT = 500
GRID_SIZE = 20
BACKGROUND_COLOR = 'black'
FOOD_COLOR = 'red'
SNAKE_COLOR = 'green'
GAME_SPEED = 200  # Set to a lower value for a faster game


class SnakeGame:
    def __init__(self, window):
        self.window = window
        self.window.title('Snake Game')
        self.window.geometry(f'{WIDTH}x{HEIGHT + 100}')
        self.window.iconphoto(True, PhotoImage(file='download.png'))

        # Menu
        self.menubar = Menu(self.window)
        self.window.config(menu=self.menubar)
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Game', menu=self.file_menu)

        # Menu options
        self.file_menu.add_command(label='Restart', command=self.restart)
        self.file_menu.add_command(label='Pause', command=self.pause)
        self.file_menu.add_command(label='Increase Level', command=self.increase_level)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Quit', command=self.close)

        # Canvas
        self.canvas = Canvas(self.window, width=WIDTH, height=HEIGHT, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        self.food = self.create_food()
        self.snake = [(100, 60), (80, 60), (60, 60)]
        self.direction = 'Right'
        self.score = 0
        self.running = True
        self.speed = GAME_SPEED

        self.label = Label(self.window, text=f'Score: {self.score}', font=('Arial', 15))
        self.label.pack()

        # Key bindings
        self.window.bind('<Up>', lambda event: self.change_direction('Up'))
        self.window.bind('<Down>', lambda event: self.change_direction('Down'))
        self.window.bind('<Left>', lambda event: self.change_direction('Left'))
        self.window.bind('<Right>', lambda event: self.change_direction('Right'))
        self.window.bind('<w>', lambda event: self.change_direction('Up'))
        self.window.bind('<s>', lambda event: self.change_direction('Down'))
        self.window.bind('<a>', lambda event: self.change_direction('Left'))
        self.window.bind('<d>', lambda event: self.change_direction('Right'))
        self.window.bind('<q>', self.close)
        self.window.bind('<p>', self.pause)

        self.update_game()

    def create_food(self):
        """Generates food at a random location."""
        x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        return x, y

    def change_direction(self, new_direction):
        """Changes snake direction but prevents 180° turns."""
        opposite_directions = {'Up': 'Down', 'Down': 'Up', 'Right': 'Left', 'Left': 'Right'}
        if new_direction != opposite_directions.get(self.direction):
            self.direction = new_direction

    def close(self, event=None):
        """Closes the game."""
        self.running = False
        if messagebox.askokcancel(title='Quit Game', message='Do you want to quit?'):
            self.window.destroy()
        else:
            self.running = True
            self.update_game()

    def pause(self, event=None):
        """Pauses the game when the menu or key is pressed."""
        self.running = False
        if messagebox.askokcancel(title='Pause Game', message='Continue game?'):
            self.running = True
            self.update_game()

    def restart(self):
        """Restarts the game."""
        if messagebox.askyesno(title='Restart Game', message='Do you want to restart?'):
            self.snake = [(100, 60), (80, 60), (60, 60)]
            self.direction = 'Right'
            self.score = 0
            self.label.config(text=f'Score: {self.score}')
            self.running = True
            self.speed = GAME_SPEED
            self.update_game()
        else:
            self.running = True
            self.update_game()

    def increase_level(self):
        """Increases game speed to make it harder."""
        if self.speed > 50:  # Prevent the game from becoming too fast
            self.speed -= 10
        messagebox.showinfo('Level Up!', 'Game speed increased!')

    def move_snake(self):
        """Moves the snake forward and handles collisions."""
        snake_head_x, snake_head_y = self.snake[0]

        # Move in the correct direction
        if self.direction == 'Up':
            snake_head_y -= GRID_SIZE
        elif self.direction == 'Down':
            snake_head_y += GRID_SIZE
        elif self.direction == 'Left':
            snake_head_x -= GRID_SIZE
        elif self.direction == 'Right':
            snake_head_x += GRID_SIZE

        new_snake_head = (snake_head_x, snake_head_y)

        # Check collision with walls or itself
        if (new_snake_head in self.snake or
                snake_head_x < 0 or snake_head_x >= WIDTH or
                snake_head_y < 0 or snake_head_y >= HEIGHT):
            self.running = False
            self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text='Game Over', fill='white', font=('Arial', 30))
            return

        self.snake.insert(0, new_snake_head)

        # Check if food is eaten
        if new_snake_head == self.food:
            self.food = self.create_food()
            self.score += 5
            self.label.config(text=f'Score: {self.score}')
        else:
            self.snake.pop()

    def update_game(self):
        """Continuously updates the game while running."""
        if self.running:
            self.move_snake()
            self.canvas.delete('all')

            # Draw food
            x, y = self.food
            self.canvas.create_rectangle(x, y, x + GRID_SIZE, y + GRID_SIZE, fill=FOOD_COLOR, outline='')

            # Draw snake
            for segment in self.snake:
                snake_x, snake_y = segment
                self.canvas.create_rectangle(snake_x, snake_y, snake_x + GRID_SIZE, snake_y + GRID_SIZE, fill=SNAKE_COLOR, outline='')

            # Stop if the game is over
            if not self.running:
                self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text='Game Over', fill='white', font=('Arial', 30))
                return

            self.window.after(self.speed, self.update_game)


if __name__ == '__main__':
    root = Tk()
    game = SnakeGame(root)
    root.mainloop()
