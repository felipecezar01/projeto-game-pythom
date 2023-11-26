import turtle
import math
import random
import pygame

# Initialize pygame
pygame.init()

# Set up the game window screen
window = turtle.Screen()
window.bgcolor("green")
window.title("Space Invaders - CopyAssignment")
window.bgpic("background.gif")

# Register the shape
turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for _ in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Define a variable to store the border value
border = 300

# Set the score to 0
score = 0

# Draw the pen
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("red")
score_pen.penup()
score_pen.setposition(-290, 280)
score_pen.write(f"SCORE: {score}", False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

playerspeed = 15

#AJUSTES01start!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Create a variable to store the level of difficulty
level = window.textinput("Escolha o nível", "Aperte E para Easy, M para Medio ou H para Hard: ").upper()
while level not in ["E", "M", "H"]:
    level = window.textinput("Input Inválido", "Por favor, aperte E para Easy, M para Medium ou H para Hard: ").upper()

# Choose a number of enemies based on the level
level_settings = {"E": (5, 1, 40), "M": (10, 2, 30), "H": (15, 4, 20)}
number_of_enemies, enemyspeed, bulletspeed = level_settings[level]
#AJUSTES01end!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#AJUSTES02start!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Create a list of enemies
enemies = [turtle.Turtle() for _ in range(number_of_enemies)]
for enemy in enemies:
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    enemy.setposition(random.randint(-230, 230), random.randint(150, 250))
#AJUSTES02end!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Create the player's bullet
bullet = turtle.Turtle()
bullet.shape("triangle")
bullet.color("white")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

#REMOVIDO CÓDIGO DESNECESSÁRIO (AJUSTE 03)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Define bullet state
bulletstate = "ready"


#AJUSTES04start!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Move the player left and right
def move_left():
    x = max(player.xcor() - playerspeed, -280)
    player.setx(x)

def move_right():
    x = min(player.xcor() + playerspeed, 280)
    player.setx(x)
#AJUSTES04end!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#AJUSTES05start!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Fire bullet
def fire_bullet():
    global bulletstate
    if bulletstate == "ready":
        bulletstate = "fire"
        bullet.setposition(player.xcor(), player.ycor() + 10)
        bullet.showturtle()
        gunshot_sound.play()
#AJUSTES05end!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Call listen() and onkey() functions inside the main loop
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

#AJUSTES06start!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Check collision between two turtles
def isCollision(t1, t2, collision_radius):
    distance = math.sqrt((t1.xcor() - t2.xcor())**2 + (t1.ycor() - t2.ycor())**2)
    return distance < collision_radius

#AJUSTES06end!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Load the gunshot sound
gunshot_sound = pygame.mixer.Sound("shootsong.wav")  # Replace "gunshot.wav" with the actual filename of your gunshot sound
explosion_sound = pygame.mixer.Sound("explosionsong.mp3")
game_over_sound = pygame.mixer.Sound("deadsong.mp3")

# Load the soundtrack
pygame.mixer.music.load("mainsong.mp3")  # Replace "soundtrack.mp3" with the actual filename of your soundtrack
pygame.mixer.music.play(-1)  # -1 means play in an infinite loop

# Game loop
Game_Over = False
missed_enemies = 0

while not Game_Over:
    for enemy in enemies:
        enemy.setx(enemy.xcor() + enemyspeed)

        if enemy.xcor() > 270 or enemy.xcor() < -270: #AJUSTE07!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # Move all enemies down
            for e in enemies:
                e.sety(e.ycor() - 40)
                if e.ycor() < -285 and not Game_Over:
                    e.hideturtle()
                    missed_enemies += 1
                    if missed_enemies == 5:
                        Game_Over = True
                    x = random.randint(-200, 200) #AJUSTE08!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    y = random.randint(100, 250)
                    e.setposition(x, y)
                    e.showturtle()
            enemyspeed *= -1

        if isCollision(bullet, enemy, 25): #AJUSTE09!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setposition(0, -400)
            enemy.setposition(random.randint(-border, border), random.randint(100, 250))
            enemyspeed += 0.5
            score += 10
            score_pen.clear()
            score_pen.write(f"Score: {score}", False, align="left", font=("Arial", 14, "normal"))
            explosion_sound.play()


        if isCollision(player, enemy, 30): #AJUSTE10!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            Game_Over = True
            break  # Exit the loop immediately when a collision occurs

    if Game_Over:
        window.bgpic("end.gif")
        player.hideturtle()
        bullet.hideturtle()
        pygame.mixer.quit()
        for e in enemies:
            e.hideturtle()  # Stop the soundtrack

        pygame.init()
        game_over_sound.play()
        pygame.time.delay(7000)
        break


    if bulletstate == "fire":
        bullet.sety(bullet.ycor() + bulletspeed)

    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"

pygame.mixer.quit()
turtle.done()
