import tkinter as tk
import random

# Game constants
WIDTH = 800
HEIGHT = 400
BALL_RADIUS = 15
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 80
BALL_SPEED = 3
PADDLE_SPEED = 5

# Game variables
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = BALL_SPEED
ball_dy = BALL_SPEED
paddle1_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
paddle2_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
paddle1_dy = 0
paddle2_dy = 0
score1 = 0
score2 = 0
is_paused = False
ball_speed_multiplier = 1.0

# Function to update the ball position
def update_ball():
    global ball_x, ball_y, ball_dx, ball_dy, score1, score2

    # Update ball position
    ball_x += int(ball_dx * ball_speed_multiplier)
    ball_y += int(ball_dy * ball_speed_multiplier)

    # Check collision with paddles
    if ball_x <= PADDLE_WIDTH and paddle1_y <= ball_y <= paddle1_y + PADDLE_HEIGHT:
        ball_dx = BALL_SPEED
    elif ball_x >= WIDTH - PADDLE_WIDTH - BALL_RADIUS and paddle2_y <= ball_y <= paddle2_y + PADDLE_HEIGHT:
        ball_dx = -BALL_SPEED

    # Check collision with walls
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_RADIUS:
        ball_dy *= -1

    # Check if ball missed the paddles
    if ball_x < 0:
        score2 += 1
        reset_ball()
    elif ball_x > WIDTH:
        score1 += 1
        reset_ball()

# Function to reset the ball position
def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = random.choice([-BALL_SPEED, BALL_SPEED])
    ball_dy = random.choice([-BALL_SPEED, BALL_SPEED])

# Function to update the paddle positions
def update_paddles():
    global paddle1_y, paddle2_y, paddle1_dy, paddle2_dy

    paddle1_y += paddle1_dy
    paddle2_y += paddle2_dy

    # Limit paddle movement within the screen
    if paddle1_y < 0:
        paddle1_y = 0
    elif paddle1_y > HEIGHT - PADDLE_HEIGHT:
        paddle1_y = HEIGHT - PADDLE_HEIGHT

    if paddle2_y < 0:
        paddle2_y = 0
    elif paddle2_y > HEIGHT - PADDLE_HEIGHT:
        paddle2_y = HEIGHT - PADDLE_HEIGHT

# Function to handle key press events
def on_key_press(event):
    global paddle1_dy, paddle2_dy, is_paused, ball_speed_multiplier

    if event.keysym == 'w':
        paddle1_dy = -PADDLE_SPEED
    elif event.keysym == 's':
        paddle1_dy = PADDLE_SPEED
    elif event.keysym == 'Up':
        paddle2_dy = -PADDLE_SPEED
    elif event.keysym == 'Down':
        paddle2_dy = PADDLE_SPEED
    elif event.keysym == 'p':
        is_paused = not is_paused
    elif event.keysym == 'Right':
        ball_speed_multiplier += 0.1
    elif event.keysym == 'Left':
        ball_speed_multiplier -= 0.1


# Function to handle key release events
def on_key_release(event):
    global paddle1_dy, paddle2_dy

    if event.keysym in ['w', 's']:
        paddle1_dy = 0
    elif event.keysym in ['Up', 'Down']:
        paddle2_dy = 0


# Function to update the game state
def update_game():
    if not is_paused:
        update_ball()
        update_paddles()
    canvas.delete("all")
    draw_objects()
    canvas.after(16, update_game)


# Function to draw the game objects on the canvas
def draw_objects():
    # Draw paddles
    canvas.create_rectangle(0, paddle1_y, PADDLE_WIDTH, paddle1_y + PADDLE_HEIGHT, fill="white")
    canvas.create_rectangle(WIDTH - PADDLE_WIDTH, paddle2_y, WIDTH, paddle2_y + PADDLE_HEIGHT, fill="white")

    # Draw ball
    canvas.create_oval(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, ball_x + BALL_RADIUS, ball_y + BALL_RADIUS,
                       fill="white")

    # Draw score
    canvas.create_text(WIDTH // 2 - 50, 50, text=f"Player 1: {score1}", fill="white")
    canvas.create_text(WIDTH // 2 + 50, 50, text=f"Player 2: {score2}", fill="white")


# Create the tkinter window
window = tk.Tk()
window.title("Ping Pong Game")

# Create the canvas for drawing
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Bind key events
window.bind("<KeyPress>", on_key_press)
window.bind("<KeyRelease>", on_key_release)

# Start the game
update_game()

# Start the tkinter event loop
window.mainloop()

