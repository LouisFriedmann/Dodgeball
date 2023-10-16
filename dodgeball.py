# Dodgeball by @Louis Friedmann

# Import statements
import pygame
import math
import random
import timer

# Functions

# Function redraws images on the screen
def redraw_imgs(imgs):
    for img in imgs:
        screen.blit(img[IMG], (img[X], img[Y]))

# Function makes a visible image and resizes it
def make_img(img_file, width, height, x=0, y=0):
    loaded_img = pygame.image.load(img_file)
    real_img = pygame.transform.scale(loaded_img, (width, height))
    screen.blit(real_img, (x, y))
    all_imgs.append([real_img, width, height, x, y])
    return all_imgs[len(all_imgs) - 1]

# Function hides an image
def hide(img):
    if img in all_imgs:
        all_imgs.remove(img)
        redraw_imgs(all_imgs)

# Function shows an image
def show(img):
    if not img in all_imgs:
        all_imgs.append(img)
        screen.blit(img[IMG], (img[X], img[Y]))

# Function rotates an image (angle must be in degrees)
global img_copy
def rotate(img, angle):
    redraw_imgs(all_imgs)
    img_copy = img.copy()
    rotated_copy = img_copy
    rotated_copy[IMG] = pygame.transform.rotate(img[IMG].copy(), angle)
    screen.blit(rotated_copy[IMG], (img[X], img[Y]))

# Function moves an image if the arrow is not rotating
def move(img, dx, dy):
    if not is_arrow_img_rotating:
        img[X] += dx
        img[Y] += dy
        redraw_imgs(all_imgs)

# Function determines if an image is at the top border
def at_top_border(img):
    return img[Y] <= TOP_BORDER

# Function determines if an image is at the bottom border
def at_bottom_border(img):
    return img[Y] + img[HEIGHT] >= BOTTOM_BORDER

# Function determines if an image is at the left border
def at_left_border(img):
    return img[X] <= LEFT_BORDER

# Function determines if an image is at the right border
def at_right_border(img):
    return img[X] + img[WIDTH] >= RIGHT_BORDER

# Function determines if an image has gone past the middle
def at_middle(img):
    if (img == player_1_img):
        return img[X] + img[WIDTH] >= RIGHT_BORDER / 2
    if (img == player_2_img):
        return img[X] <= RIGHT_BORDER / 2

# Function determines if an image overlaps with another image
def overlaps(img_1, img_2):
     return (((img_1[X] + img_1[WIDTH] >= img_2[X] and img_1[X] + img_1[WIDTH] <= img_2[X] + img_2[WIDTH]) or (
             img_1[X] >= img_2[X] and img_1[X] <= img_2[X] + img_2[WIDTH])) and (
         (img_1[Y] + img_1[HEIGHT] >= img_2[Y] and img_1[Y] + img_1[HEIGHT] <= img_2[Y] + img_2[HEIGHT]) and (
         img_1[Y] >= img_2[Y] and img_1[Y] <= img_2[Y] + img_2[HEIGHT]))) or (
         ((img_2[X] + img_2[WIDTH] >= img_1[X] and img_2[X] + img_2[WIDTH] <= img_1[X] + img_1[WIDTH]) or (
             img_2[X] >= img_1[X] and img_2[X] <= img_1[X] + img_1[WIDTH])) and (
         (img_2[Y] + img_2[HEIGHT] >= img_1[Y] and img_2[Y] + img_2[HEIGHT] <= img_1[Y] + img_1[HEIGHT]) and (
         img_2[Y] >= img_1[Y] and img_2[Y] <= img_1[Y] + img_1[HEIGHT])))

# Function displays a message on the screen in any color at any x and y coordinate
def display_message(text, color, size, x, y):
    font = pygame.font.SysFont(None, int(size))
    screen.blit(font.render(str(text), True, color), (x, y))

# Main section
if __name__ == "__main__":
    pygame.init()

    # List to store all images
    all_imgs = []

    # Constants
    RIGHT_BORDER = 600
    BOTTOM_BORDER = 400
    TOP_BORDER = 0
    LEFT_BORDER = 0
    DELAY = 100
    IMG = 0
    WIDTH = 1
    HEIGHT = 2
    X = 3
    Y = 4
    MAX_SPEED = 30
    CATCH_TIME_LIMIT = 2
    CATCHING_DELAY = 5
    GREEN = (0, 255, 0)
    WINNING_SCORE = 3

    # Make screen and caption
    screen = pygame.display.set_mode((RIGHT_BORDER, BOTTOM_BORDER))
    pygame.display.set_caption("Dodgeball")

    # Make new timer objects
    hesitating_timer = timer.Timer()
    hesitating_timer.reset()
    p1_catching_timer = timer.Timer()
    p2_catching_timer = timer.Timer()
    p1_catching_delay_timer = timer.Timer()
    p2_catching_delay_timer = timer.Timer()

    # Make the images for the game
    floor_img = make_img('dodgeball_floor.png', RIGHT_BORDER, BOTTOM_BORDER, 0, 0)
    dodgeball_img = make_img('the_dodgeball.png', 25, 25, RIGHT_BORDER / 2 - 12.5, BOTTOM_BORDER / 2 - 12.5)
    player_1_img = make_img('player_1.png', 75, 75, RIGHT_BORDER / 4 - 37.5, BOTTOM_BORDER / 2 - 37.5)
    player_2_img = make_img('player_2.png', 75, 75, RIGHT_BORDER * (3 / 4) - 37.5, BOTTOM_BORDER / 2 - 37.5)
    arrow_img = make_img('arrow.png', 50, 50)
    grey_rectangle_1 = make_img('grey_rectangle.png', 150, 75, LEFT_BORDER, BOTTOM_BORDER - 75)
    green_rectangle_1 = make_img('green_rectangle.png', grey_rectangle_1[WIDTH], 20, grey_rectangle_1[X] -
                                 grey_rectangle_1[WIDTH], grey_rectangle_1[Y] + grey_rectangle_1[HEIGHT] / 2)
    grey_rectangle_2 = make_img('grey_rectangle.png', grey_rectangle_1[WIDTH], grey_rectangle_1[HEIGHT],
                                RIGHT_BORDER - grey_rectangle_1[WIDTH], grey_rectangle_1[Y])
    green_rectangle_2 = make_img('green_rectangle.png', green_rectangle_1[WIDTH], green_rectangle_1[HEIGHT],
                                 RIGHT_BORDER, green_rectangle_1[Y])

    # Make sound objects
    hit = pygame.mixer.Sound('hit.mp3')

    # Main game loop
    player_1_distance = 10
    player_2_distance = 10
    hide(arrow_img)
    hide(grey_rectangle_1)
    hide(grey_rectangle_2)
    angle = 0
    is_arrow_img_rotating = False
    has_arrow_rotated = False
    ball_speed = 0
    green_rect_speed_1 = 0
    green_rect_speed_2 = 0
    ball_dx = 0
    ball_dy = 0
    starting_green_1_x = green_rectangle_1[X]
    starting_green_2_x = green_rectangle_2[X]
    rect_1_moving_right = True
    rect_2_moving_right = False
    is_thrown_p1 = False
    is_thrown_p2 = False
    ball_to_middle = False
    rand_num = random.random() * 10
    p1_enable_catching = True
    p2_enable_catching = True
    p1_catching_time = 0
    p2_catching_time = 0
    slow_down_ball = False
    ball_slowdown_percent = 0
    p1_score = 0
    p2_score = 0
    game_over = False
    while not game_over:
        # Quit if the user wants to
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Player movement and dodgeball movement with player
        if pygame.key.get_pressed()[pygame.K_w] and not at_top_border(player_1_img):
            move(player_1_img, 0, -player_1_distance)
            if player_1_picked_up:
                move(dodgeball_img, 0, -player_1_distance)
        if pygame.key.get_pressed()[pygame.K_s] and not at_bottom_border(player_1_img):
            move(player_1_img, 0, player_1_distance)
            if player_1_picked_up:
                move(dodgeball_img, 0, player_1_distance)
        if pygame.key.get_pressed()[pygame.K_a] and not at_left_border(player_1_img):
            move(player_1_img, -player_1_distance, 0)
            if player_1_picked_up:
                move(dodgeball_img, -player_1_distance, 0)
        if pygame.key.get_pressed()[pygame.K_d] and not at_middle(player_1_img):
            move(player_1_img, player_1_distance, 0)
            if player_1_picked_up:
                move(dodgeball_img, player_1_distance, 0)
        if pygame.key.get_pressed()[pygame.K_UP] and not at_top_border(player_2_img):
            move(player_2_img, 0, -player_2_distance)
            if player_2_picked_up:
                move(dodgeball_img, 0, -player_2_distance)
        if pygame.key.get_pressed()[pygame.K_DOWN] and not at_bottom_border(player_2_img):
            move(player_2_img, 0, player_2_distance)
            if player_2_picked_up:
                move(dodgeball_img, 0, player_2_distance)
        if pygame.key.get_pressed()[pygame.K_LEFT] and not at_middle(player_2_img):
            move(player_2_img, -player_2_distance, 0)
            if player_2_picked_up:
                move(dodgeball_img, -player_2_distance, 0)
        if pygame.key.get_pressed()[pygame.K_RIGHT] and not at_right_border(player_2_img):
            move(player_2_img, player_2_distance, 0)
            if player_2_picked_up:
                move(dodgeball_img, player_2_distance, 0)

        # Picking up a dodgeball
        player_1_picked_up = False
        player_2_picked_up = False
        if overlaps(dodgeball_img, player_1_img) and pygame.key.get_pressed()[pygame.K_q]:
            player_1_picked_up = True
        if overlaps(dodgeball_img, player_2_img) and pygame.key.get_pressed()[pygame.K_p]:
            player_2_picked_up = True

        # Rotate the arrow
        if player_1_picked_up and pygame.key.get_pressed()[pygame.K_z]:
            if not is_arrow_img_rotating:
                angle = 0
                x = 0
            arrow_img[X] = dodgeball_img[X] + dodgeball_img[WIDTH] / 2
            arrow_img[Y] = dodgeball_img[Y] - dodgeball_img[HEIGHT] / 2
            rotate(arrow_img, angle)
            is_arrow_img_rotating = True
            has_arrow_rotated = True
            angle = -4 * abs(x - 45) + 180
            x += 1
            x %= 90
        if player_2_picked_up and pygame.key.get_pressed()[pygame.K_l]:
            if not is_arrow_img_rotating:
                angle = 0
                x = 0
            arrow_img[X] = dodgeball_img[X] - arrow_img[WIDTH] + dodgeball_img[WIDTH] / 2
            arrow_img[Y] = dodgeball_img[Y] - dodgeball_img[HEIGHT] / 2
            rotate(arrow_img, angle)
            is_arrow_img_rotating = True
            has_arrow_rotated = True
            angle = 4 * abs(x - 45) + 180
            x += 1
            x %= 90
        if not pygame.key.get_pressed()[pygame.K_z] and not pygame.key.get_pressed()[pygame.K_l]:
            is_arrow_img_rotating = False

        # After the arrow is rotated, the ball is thrown in the direction the arrow was pointed
        if not is_arrow_img_rotating and has_arrow_rotated:
            if green_rectangle_1[X] + green_rect_speed_1 + green_rectangle_1[WIDTH] > grey_rectangle_1[X] + (
            grey_rectangle_1[WIDTH]) and rect_1_moving_right:
                green_rect_speed_1 *= -1
                rect_1_moving_right = False
            if green_rectangle_1[X] + green_rect_speed_1 + green_rectangle_1[WIDTH] < grey_rectangle_1[X] and (
            not rect_1_moving_right):
                green_rect_speed_1 *= -1
                rect_1_moving_right = True
            if green_rectangle_2[X] + green_rect_speed_2 > grey_rectangle_2[X] + grey_rectangle_2[WIDTH] and (
            rect_2_moving_right):
                green_rect_speed_2 *= -1
                rect_2_moving_right = False
            if green_rectangle_2[X] + green_rect_speed_2 < grey_rectangle_2[X] and not rect_2_moving_right:
                green_rect_speed_2 *= -1
                rect_2_moving_right = True
            if overlaps(dodgeball_img, player_1_img) and not is_thrown_p2 and not is_thrown_p1:
                show(grey_rectangle_1)
                hide(green_rectangle_1)
                show(green_rectangle_1)
                if rect_1_moving_right:
                    green_rect_speed_1 = 20
            if overlaps(dodgeball_img, player_2_img) and not is_thrown_p1 and not is_thrown_p2:
                show(grey_rectangle_2)
                hide(green_rectangle_2)
                show(green_rectangle_2)
                if not rect_2_moving_right:
                    green_rect_speed_2 = -20
            move(green_rectangle_1, green_rect_speed_1, 0)
            move(green_rectangle_2, green_rect_speed_2, 0)
            if pygame.key.get_pressed()[pygame.K_x] and not is_thrown_p2 and not is_thrown_p1 and overlaps(player_1_img, dodgeball_img):
                ball_speed = (green_rectangle_1[X] + green_rectangle_1[WIDTH]) / grey_rectangle_1[WIDTH] * MAX_SPEED
                ball_slowdown_percent = 0
                green_rect_speed_1 = 0
                green_rectangle_1[X] = starting_green_1_x
                hide(green_rectangle_1)
                hide(grey_rectangle_1)
                ball_dx = math.sin(math.radians(angle)) * ball_speed
                ball_dy = math.cos(math.radians(angle)) * ball_speed
                is_thrown_p1 = True
                player_1_picked_up = False
            if pygame.key.get_pressed()[pygame.K_m] and not is_thrown_p1 and not is_thrown_p2 and overlaps(player_2_img, dodgeball_img):
                ball_speed = (RIGHT_BORDER - green_rectangle_2[X]) / green_rectangle_2[WIDTH] * MAX_SPEED
                ball_slowdown_percent = 0
                green_rect_speed_2 = 0
                green_rectangle_2[X] = starting_green_2_x
                hide(green_rectangle_2)
                hide(grey_rectangle_2)
                ball_dx = math.sin(math.radians(angle)) * ball_speed
                ball_dy = math.cos(math.radians(angle)) * ball_speed
                is_thrown_p2 = True
                player_2_picked_up = False

            # Ball and border collisions, deal with slowing down ball, then move the dodgeball
            if at_top_border(dodgeball_img) or at_bottom_border(dodgeball_img):
                ball_dy *= -1
                hit.play()
            if at_right_border(dodgeball_img) or at_left_border(dodgeball_img):
                ball_dx *= -1
                slow_down_ball = True
                hit.play()
            if slow_down_ball:
                ball_slowdown_percent += 10
                if ball_slowdown_percent >= 100:
                    slow_down_ball = False
            move(dodgeball_img, ball_dx * (1 - ball_slowdown_percent / 100), ball_dy * (1 - ball_slowdown_percent / 100))

            # Getting hit by a dodgeball, then reset (occurs once per actually being hit)
            if overlaps(dodgeball_img, player_1_img) and is_thrown_p2:
                if ball_slowdown_percent != 100:
                    hit.play()
                # Catching
                p1_is_caught = False
                if p1_enable_catching and pygame.key.get_pressed()[pygame.K_e] and ball_slowdown_percent != 100:
                    p1_is_caught = True
                if ball_slowdown_percent != 100 and not p1_is_caught:
                    p2_score += 1
                    hide(dodgeball_img)
                    hesitating_timer.start()
                    ball_to_middle = True
                if p1_is_caught:
                    p1_score += 1
                is_arrow_img_rotating = False
                has_arrow_rotated = False
                ball_speed = 0
                green_rect_speed_1 = 0
                green_rect_speed_2 = 0
                ball_dx = 0
                ball_dy = 0
                rect_1_moving_right = True
                rect_2_moving_right = False
                is_thrown_p1 = False
                is_thrown_p2 = False
            if overlaps(dodgeball_img, player_2_img) and is_thrown_p1:
                if ball_slowdown_percent != 100:
                    hit.play()
                # Catching
                p2_is_caught = False
                if p2_enable_catching and pygame.key.get_pressed()[pygame.K_RSHIFT] and ball_slowdown_percent != 100:
                    p2_is_caught = True
                if ball_slowdown_percent != 100 and not p2_is_caught:
                    p1_score += 1
                    hide(dodgeball_img)
                    hesitating_timer.start()
                    ball_to_middle = True
                elif p2_is_caught:
                    p2_score += 1

                is_arrow_img_rotating = False
                has_arrow_rotated = False
                ball_speed = 0
                green_rect_speed_1 = 0
                green_rect_speed_2 = 0
                ball_dx = 0
                ball_dy = 0
                rect_1_moving_right = True
                rect_2_moving_right = False
                is_thrown_p1 = False
                is_thrown_p2 = False
        if ball_to_middle and hesitating_timer.elapsed_time() >= rand_num and ball_slowdown_percent != 100:
            hesitating_timer.reset()
            dodgeball_img[X] = RIGHT_BORDER / 2 - dodgeball_img[WIDTH] / 2
            dodgeball_img[Y] = random.randint(TOP_BORDER, BOTTOM_BORDER - dodgeball_img[HEIGHT])
            show(dodgeball_img)
            rand_num = random.random() * 10
            ball_to_middle = False

        # Catching a dodgeball
        if pygame.key.get_pressed()[pygame.K_e] and p1_catching_timer.elapsed_time() == 0:
            p1_catching_timer.start()
        p1_catching_time = p1_catching_timer.elapsed_time()
        if p1_catching_time >= CATCH_TIME_LIMIT:
            p1_enable_catching = False
            p1_catching_timer.reset()
            p1_catching_delay_timer.start()
        if not p1_enable_catching and p1_catching_delay_timer.elapsed_time() >= CATCHING_DELAY:
            p1_enable_catching = True
            p1_catching_delay_timer.reset()

        if pygame.key.get_pressed()[pygame.K_RSHIFT] and p2_catching_timer.elapsed_time() == 0:
            p2_catching_timer.start()
        p2_catching_time = p2_catching_timer.elapsed_time()
        if p2_catching_time >= CATCH_TIME_LIMIT:
            p2_enable_catching = False
            p2_catching_timer.reset()
            p2_catching_delay_timer.start()
        if p2_catching_delay_timer.elapsed_time() >= CATCHING_DELAY and not p2_enable_catching:
            p2_enable_catching = True
            p2_catching_delay_timer.reset()

        # Display scores
        display_message(f"Player 1: {p1_score}", GREEN, RIGHT_BORDER / 16, RIGHT_BORDER / 4, BOTTOM_BORDER / 30)
        display_message(f"Player 2: {p2_score}", GREEN, RIGHT_BORDER / 16, RIGHT_BORDER / 2, BOTTOM_BORDER / 30)

        # Determining winners
        if p1_score >= WINNING_SCORE:
            display_message(f"Player 1 wins", GREEN, RIGHT_BORDER / 8, RIGHT_BORDER / 4, BOTTOM_BORDER / 2 - RIGHT_BORDER / 16)
            game_over = True
        if p2_score >= WINNING_SCORE:
            display_message(f"Player 2 wins", GREEN, RIGHT_BORDER / 8, RIGHT_BORDER / 4, BOTTOM_BORDER / 2 - RIGHT_BORDER / 16)
            game_over = True

        # Time delay and updating the screen
        pygame.time.delay(DELAY)
        pygame.display.update()
    pygame.time.delay(5000)
    pygame.quit()

