import tkinter
import random

# Design a 25*25 tile window, each tile is 25 pixels
ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

# Create game window
window = tkinter.Tk()
window.title('Snake')
# Set window width and height unchangeable
window.resizable(False, False)
# Add window style
canvas = tkinter.Canvas(window, bg='black', width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
# Adds canvas widget to window
canvas.pack()
# Update window immediately
window.update()

# Center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))
# Format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

restart_button = None
after_id = None

# Store x and y position of food and snake
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def initialize_game():

    global snake, food, snake_body, velocityX, velocityY, game_over, score, restart_button, after_id

    # Initialize snake and food position
    snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE) 
    food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)

    snake_body = []
    velocityX = 0
    velocityY = 0
    game_over = False
    score = 0

    # Remove button once restart the game
    if restart_button:
        restart_button.destroy()
        restart_button = None
    # Cancel the scheduled draw() function call to prevent multiple draw() loops from running simultaneously
    if after_id:
        window.after_cancel(after_id)
        after_id = None

initialize_game()

def change_direction(e):

    global velocityX, velocityY

    # The snake can't go to the opposite direction
    if e.keysym == "Up" and velocityY != 1:
        velocityX = 0
        velocityY = -1
    elif e.keysym == "Down" and velocityY != -1:
        velocityX = 0
        velocityY = 1
    elif e.keysym == "Left" and velocityX != 1:
        velocityX = -1
        velocityY = 0
    elif e.keysym == "Right" and velocityX != -1:
        velocityX = 1
        velocityY = 0

def move():

    global snake, food, snake_body, game_over, score

    if game_over:
        return
    
    # Game over if collision with border
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return
    
    # Game over if collision with snake body
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    # Collision with food,food appends to snake body
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))
        #   New food shows up in random position
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    # Update snake body
    # Iterate over the snake_body list in reverse order.
    for i in range(len(snake_body) - 1, -1, -1):
        # Get the current segment of the snake's body
        tile = snake_body[i]
        # Update the position of the first segment to the current position of the snake's head
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        # Otherwise,update the position of the current segment to the previous segment
        else:
            prev_tile = snake_body[i - 1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
            
    # Update the position of the snake's head based on its current velocity
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE



def draw():
    global snake, food, snake_body, game_over, score, restart_button, after_id

    move()

    canvas.delete('all')

    # Draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='red')

    # Draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill='lime green')

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill='lime green')

    if game_over:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font='Arial 20', text=f"Game Over: {score}", fill='white')
        if restart_button is None:
            restart_button = tkinter.Button(window, text="Restart", font='Arial',padx=0,pady=0,borderwidth=0, highlightthickness=0,command=restart_game)
            restart_button.place(x=WINDOW_WIDTH / 2 - 40, y=WINDOW_HEIGHT / 2 + 20)
    else:
        canvas.create_text(30, 20, font='Arial 10', text=f"Score: {score}", fill='white')
    
    after_id = window.after(150, draw)  # Set speed to 150ms

draw()

def restart_game():
    initialize_game()
    draw()

# Use KeyRelease to invoke the game
window.bind('<KeyRelease>', change_direction)
window.mainloop()
