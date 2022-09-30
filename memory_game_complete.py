import pygame
from random import  *

# setup for the level
def setup(level):
    global display_time

    # How long will the numbers be displayed?
    display_time = 5 - (level // 3)
    display_time = max(display_time, 1)

    # How many will the numbers be displayed?
    number_count = (level // 3) + 5
    number_count = min(number_count, 20) # If > 20, "number_count = 20"

    # Randomly arrange the numbers in Grid on display screen
    shuffle_grid(number_count)

#s Shuffle the number
def shuffle_grid(number_count):

    rows = 5
    columns = 9

    cell_size = 130 # horizontal& vertical size for each Grid cell 
    button_size = 110 # button size in Grid cell
    screen_left_margin = 55 # left margin in full display
    screen_top_margin = 20 # top margin in full display

    # [[0,0,0,0,0,0,0,0,0],
    #  [0,0,0,0,0,0,0,0,0],
    #  [0,0,0,0,0,0,0,0,0],
    #  [0,0,0,0,0,0,0,0,0],
    #  [0,0,0,0,0,0,0,0,0]]
    grid = [ [0 for col in range(columns)] for row in range(rows) ] # 5 x 9

    number = 1 # from the smallest number 1 to [number_count]
               # if number == 5: randomly place number up to 5

    while number <= number_count:
        row_idx = randrange(0, rows) # pick numbers randomly in 0,1,2,3,4 
        col_idx = randrange(0, columns) # pic numbers randomly in 0~8 

        if grid[row_idx][col_idx] == 0:
            grid[row_idx][col_idx] = number # put the arranged numbers in Grid cells
            number += 1

            # Get the x, y position based on the current Grid cell position
            center_x = screen_left_margin + (col_idx * cell_size) + (cell_size / 2)
            center_y = screen_top_margin + (row_idx * cell_size) + (cell_size / 2)

            # Create number buttons
            button = pygame.Rect(0, 0, button_size, button_size)
            button.center = (center_x, center_y)

            number_buttons.append(button)


    
    # check the random number placed
    print(grid)

         


# 시작화면 보여주기 show start display
def display_start_screen():
    # white circle butten,center = start_button.center, radius = 60, linde width = 5
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5)

    msg = game_font.render(f"{curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center = start_button.center)
    screen.blit(msg, msg_rect)


# show the game display
def display_game_screen():
    global hidden

    if not hidden: 
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> sec
        if elapsed_time > display_time:
            hidden = True 
    
    for idx, rect in enumerate(number_buttons, start= 1):
        if hidden: # Hide number buttons
            # darw button rectangle
            pygame.draw.rect(screen, GRAY, rect)
        else:
            # number text style
            cell_text = game_font.render(str(idx), True, WHITE)
            text_rect = cell_text.get_rect(center=rect.center)
            screen.blit(cell_text, text_rect)

    
# check buttons of position as 'pos'
def check_buttons(pos):
    global start, start_ticks
    
    if start: # When the game starts?
        check_number_buttons(pos)
    elif start_button.collidepoint(pos):
        start = True
        start_ticks = pygame.time.get_ticks() # Run the game, start timer (save the current time)
    
def check_number_buttons(pos):
    global start, hidden,curr_level

    for button in number_buttons:
        if button.collidepoint(pos):
            if button == number_buttons[0]: # User click the correct number
                print("Correct")
                del number_buttons[0] 
                if not hidden:
                    hidden = True # Hide number buttons

            else: # User click the wrong number
                game_over()
            break

    # If User got all the numbers right? -> Level up & go back to the start screen
    if len(number_buttons) == 0:
        start = False
        hidden = False
        curr_level += 1
        setup(curr_level)

# Game end, show msg 'your level is []'
def game_over():
    global running
    running = False

    msg = game_font.render(f"Your level is {curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center = (screen_width/2, screen_heigt/2))

    screen.fill(BLACK) 
    screen.blit(msg, msg_rect)

# Initialization
pygame.init()
screen_width = 1280 # horizontal size
screen_heigt =  720 # vertical size
screen = pygame.display.set_mode((screen_width,screen_heigt)) # as a Tuple
pygame.display.set_caption("Memonry Game") # display building
game_font =  pygame.font.Font(None, 120) #fond definition

# Start button
start_button = pygame.Rect(0, 0, 120, 120)
start_button.center = (120, screen_heigt - 120) # center = 120, adjusted to [screen - 120] for the center.

# Color
BLACK = (0, 0, 0) # RGB, color of black
WHITE = (255, 255, 255) # RGB, color of white
GRAY = (50, 50, 50)

number_buttons = [] # Buttons the User will press
curr_level = 1 # the current Level
display_time = None # Time to show numbers
start_ticks = None # Time to store current time

# Game start or not
start = False

# Number is hidden or not (or if User clicked 1 )
hidden = False

# Perform the game setup function before game start
setup(curr_level)

# Game Roof
running = True # Is this game running?
while running:
    click_pos = None

    # Event Roof (joystick, maus click, ...  etc)
    for event in pygame.event.get(): # What event occurred?
        if event.type == pygame.QUIT: # Is the window closing?
            running = False # Game end
        elif event.type == pygame.MOUSEBUTTONUP: # If User clicks the mouse
            click_pos = pygame.mouse.get_pos()
            print(click_pos)

    # Fill the screen with Black
    screen.fill(BLACK)
    
    if start: 
        display_game_screen() # Game screen display
    else:
        display_start_screen() # Start display 
    
    # If there is a coordinate value that User clicked (or if cliked sth)
    if click_pos:
        check_buttons(click_pos)

    # Update Display
    pygame.display.update()

# Show numbers aoubt 5 sec
pygame.time.delay(5000)

# Quit Game
pygame.quit()


