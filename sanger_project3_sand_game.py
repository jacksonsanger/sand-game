"""
    A Sand Game that creates a game window where when the mouse is clicked, sand sprinkles from the mouse
    and accumulates on the Canvas. The sand flows realisticaly. Floors can also be drawn, and then the sand flows over the floor. 
    You can also switch the mode to "destroy", and then when the mouse is clicked, a fireball apears and burns everything it touches. 
    Author: Jackson Sanger
    Date: 1-22-2023
    Course: COMP 1352
    Assignment: Project SandGame - Part 1
    Collaborators: none
    Internet Source: none
"""
import dudraw
import random

def change_label(s: str)->None:
    """
        A function that places a string in the top left corner of a dudraw canvas
        param s: the string that you want the label to be changed to
        return: None
    """
    #set the pen color to light blue and draw a rectangle in the top left corner of the world to match the background
    dudraw.set_pen_color_rgb(*colors['light blue'])
    dudraw.filled_rectangle(10, WORLD_SIZE - 5, 10, 2)
    #set the pen color to black and put the text in the rectangle
    dudraw.set_pen_color(dudraw.BLACK)
    dudraw.set_font_family("Courier")
    dudraw.set_font_size(20)
    dudraw.text(10, WORLD_SIZE - 5, s)

def place_floor(x_loc: int, y_loc: int)->None:
    """
        A function that checks if there is an available place where we're trying to place floor, and if there is, 
        then it places a two-pixel thick piece of floor there
        param x_loc: the x coordinate of the "top" floor particle
        param y_loc: the y coordinate of the "top" floor particle
        return: None
    """
    #check if the two spaces where we want to place floor are empty
    if world_list[y_loc][x_loc] == EMPTY and world_list[y_loc - 1][x_loc] == EMPTY:
        #if they are, then make the current pixel floor and the one underneath it floor in the list
        world_list[y_loc][x_loc] = FLOOR
        world_list[y_loc - 1][x_loc] = FLOOR
        #draw the floor on the canvas
        dudraw.set_pen_color(dudraw.BLACK)
        dudraw.filled_square(x_loc + PARTICLE_SIZE, y_loc + PARTICLE_SIZE, PARTICLE_SIZE)
        dudraw.filled_square(x_loc + PARTICLE_SIZE, y_loc - 1 + PARTICLE_SIZE, PARTICLE_SIZE)

#sand functions

def place_sand(x_loc: int, y_loc: int)->None:
    """
        A function that checks if there is an available place for sand, and if there is, then it places sand there and updates the 2D list
        param x_loc: the x coordinate of the sand particle
        param y_loc: the y coordinate of the sand particle
        return: None
    """
    #check if the current space is open
    if world_list[y_loc][x_loc] == EMPTY:
        #if it is, make it sand in the 2D list
        world_list[y_loc][x_loc] = SAND
        #draw the sand particle on the canvas
        dudraw.set_pen_color_rgb(*colors["tan"]) #tan
        #we add the particle size to each coordinate so that the center is in the middle of each pixel
        dudraw.filled_square(x_loc + PARTICLE_SIZE, y_loc + PARTICLE_SIZE, PARTICLE_SIZE)
def sand_falls_vertically(sand_x: int, sand_y: int)->None:
    """
        A function that makes sand fall vertically by swapping the locations of a sand particle and a sky particle
        param sand_x: the x coordinate of the sand particle we want to swap
        param sand_y: the y coordinate of the sand particle we want to swap
        return: None
    """
    #make the current pixel empty in the list, and the one underneath it sand
    world_list[sand_y][sand_x] = EMPTY
    world_list[sand_y - 1][sand_x] = SAND
    #draw a sky pixel in the place where the sand previously was
    dudraw.set_pen_color_rgb(*colors["light blue"]) #blue
    dudraw.filled_square(sand_x + PARTICLE_SIZE, sand_y + PARTICLE_SIZE, PARTICLE_SIZE)
    #draw a sand pixel one spot beneath where the sand previously was
    dudraw.set_pen_color_rgb(*colors["tan"]) #tan
    dudraw.filled_square(sand_x + PARTICLE_SIZE , sand_y - 1 + PARTICLE_SIZE, PARTICLE_SIZE)

def sand_falls_diagonal_left(sand_x: int, sand_y: int)->None:
    """
        A function that makes sand flow diagonally to the left by swapping the position of a sand and sky particle diagonally to the left
        param sand_x: the x coordinate of the sand particle we want to swap
        param sand_y: the y coordinate of the sand particle we want to swap
        return: None
    """
    #make the current pixel empty in the list, and the one that is down one row and one column to the left sand
    world_list[sand_y][sand_x] = EMPTY
    world_list[sand_y - 1][sand_x-1] = SAND
    #draw a sky particle where our sand originally was
    dudraw.set_pen_color_rgb(*colors["light blue"]) #blue
    dudraw.filled_square(sand_x + PARTICLE_SIZE, sand_y + PARTICLE_SIZE, PARTICLE_SIZE)
    #draw the particle down one row and one column to the left as sand
    dudraw.set_pen_color_rgb(*colors["tan"]) #tan
    dudraw.filled_square(sand_x - 1 + PARTICLE_SIZE , sand_y - 1 + PARTICLE_SIZE, PARTICLE_SIZE)

def sand_falls_diagonal_right(sand_x: int, sand_y: int)->None:
    """
        A function that makes sand flow diagonally to the right by swapping the position of a sand and sky particle diagonally to the right
        param sand_x: the x coordinate of the sand particle we want to swap
        param sand_y: the y coordinate of the sand particle we want to swap
        return: None
    """
    #make the current pixel empty in the list, and the one down row and one column to the right sand
    world_list[sand_y][sand_x] = EMPTY
    world_list[sand_y - 1][sand_x + 1] = SAND
    ##draw a sky particle where our sand originally was
    dudraw.set_pen_color_rgb(*colors["light blue"]) #blue
    dudraw.filled_square(sand_x + PARTICLE_SIZE, sand_y + PARTICLE_SIZE, PARTICLE_SIZE)
    #draw a sand particle down one row and one column to the right from where our sand originally was
    dudraw.set_pen_color_rgb(*colors["tan"]) #tan
    dudraw.filled_square(sand_x + 1 + PARTICLE_SIZE , sand_y - 1 + PARTICLE_SIZE, PARTICLE_SIZE)

#fire functions

def place_fire_pixel(x_loc: int, y_loc: int, color: str)->None:
    """
        A function that draws a fire particle on the canvas if that space is not already a fire particle
        param x_loc: the x coordinate of the fire particle
        param y_loc: the y coordinate of the fire particle
        param color: the color of the fire pixel, either "white", "red", or "yellow"
        return: None
    """
    #check if the x location is inside the bounds of the world, and only execute if it is
    if x_loc >= 0 and x_loc <= WORLD_SIZE and y_loc >= 0 and y_loc <= WORLD_SIZE:
        #check if the current location is not already occupied by a fire particle (could be any color)
        if world_list[y_loc][x_loc] != FIRE_R and world_list[y_loc][x_loc] != FIRE_Y and world_list[y_loc][x_loc] != FIRE_W:
            #if the color is red:
            if color == 'red':
                #store it in the list as a red fire particle and then draw it on the canvas in the appropriate color
                world_list[y_loc][x_loc] = FIRE_R
                dudraw.set_pen_color_rgb(*colors["red"])
                dudraw.filled_square(x_loc + PARTICLE_SIZE, y_loc + PARTICLE_SIZE, PARTICLE_SIZE)
            #if the color is yellow:
            if color == 'yellow':
                #store it in the list as a yellow fire particle and then draw it on the canvas in the appropriate color
                world_list[y_loc][x_loc] = FIRE_Y
                dudraw.set_pen_color_rgb(*colors["yellow"])
                dudraw.filled_square(x_loc + PARTICLE_SIZE, y_loc + PARTICLE_SIZE, PARTICLE_SIZE)
            #if the color is white:
            if color == 'white':
                #store it in the list as a white fire particle and then draw it on the canvas in the appropriate color
                world_list[y_loc][x_loc] = FIRE_W
                dudraw.set_pen_color_rgb(*colors["white"])
                dudraw.filled_square(x_loc + PARTICLE_SIZE, y_loc + PARTICLE_SIZE, PARTICLE_SIZE)

def draw_fireball(x:int, y: int)->None:
    """
        A function that draws a fireball on the canvas and updates all the appropriate positions in the list.
        Based on where the mouse is pressed, the rest of the fireball is drawn relative to that
        param x: the x cooridnate of the bottom left corner of the fireball
        param y: the y coordinate of the bottom left corner of the fireball
        return: None
    """
    #we repeatedly call the place_fire_pixel() function to draw all the pixels, which updates the list
    #this function also checks if the location we want to put our fire pixel is within the world bounds
    place_fire_pixel(x, y, "red")
    place_fire_pixel(x +1, y-1, "red")
    place_fire_pixel(x+2, y-1, "red")
    place_fire_pixel(x+1, y, "yellow")
    place_fire_pixel(x+2, y, "yellow")
    place_fire_pixel(x+3, y, "red")
    place_fire_pixel(x-1, y+1, "red")
    place_fire_pixel(x, y+1, "yellow")
    place_fire_pixel(x+1, y+1, "yellow")
    place_fire_pixel(x+2, y+1, "white")
    place_fire_pixel(x+3, y+1, "yellow")
    place_fire_pixel(x+4, y+1, "red")
    place_fire_pixel(x-1, y+2, "red")
    place_fire_pixel(x, y+2, "yellow")
    place_fire_pixel(x+1, y+2, "white")
    place_fire_pixel(x+2, y+2, "white")
    place_fire_pixel(x+3, y+2, "yellow")
    place_fire_pixel(x+4, y+2, "red")
    place_fire_pixel(x, y+3, "red")
    place_fire_pixel(x + 1, y+3, "yellow")
    place_fire_pixel(x+2, y+3, "yellow")
    place_fire_pixel(x+3, y+3, "red")
    place_fire_pixel(x+1, y+4, "red")
    place_fire_pixel(x+2, y+4, "red")

def fire_pixel_destroys(fire_x: int, fire_y: int, color: str)->None:
    """
        A function that makes fire fall vertically and "destroy" what it touches by swapping a fire pixel of any color with a sky particle
        param fire_x: the x coordinate of the fire particle we want to swap
        param fire_y: the y coordinate of the fire particle we want to swap
        param color: the color of the fire pixel that is falling
        return: None
    """
    #if we want it to be red:
    if color == 'red':
        #make the current location empty
        world_list[fire_y][fire_x] = EMPTY
        #store the pixel underneath as a red fire particle
        world_list[fire_y - 1][fire_x] = FIRE_R
        #draw a sky particle where our fire particle used to be
        dudraw.set_pen_color_rgb(*colors["light blue"]) #blue
        dudraw.filled_square(fire_x + PARTICLE_SIZE, fire_y + PARTICLE_SIZE, PARTICLE_SIZE)
        #draw a red fire particle in the location underneath where the fire originally was
        dudraw.set_pen_color_rgb(*colors["red"])
        dudraw.filled_square(fire_x + PARTICLE_SIZE , fire_y - 1 + PARTICLE_SIZE, PARTICLE_SIZE)
    #if we want it to be yellow:
    if color == 'yellow':
        #make the current location empty
        world_list[fire_y][fire_x] = EMPTY
        #store the pixel underneath as a yellow fire particle
        world_list[fire_y - 1][fire_x] = FIRE_Y
        #draw a sky particle where our fire particle used to be
        dudraw.set_pen_color_rgb(*colors["light blue"]) #blue
        dudraw.filled_square(fire_x + PARTICLE_SIZE, fire_y + PARTICLE_SIZE, PARTICLE_SIZE)
        #draw a yellow fire particle in the location underneath where the fire originally was
        dudraw.set_pen_color_rgb(*colors["yellow"])
        dudraw.filled_square(fire_x + PARTICLE_SIZE , fire_y - 1 + PARTICLE_SIZE, PARTICLE_SIZE)
    #if we want it to be white:
    if color == 'white':
        #make the current location empty
        world_list[fire_y][fire_x] = EMPTY
        #store the pixel underneath as a white fire particle
        world_list[fire_y - 1][fire_x] = FIRE_W
        #draw a sky particle where our fire particle used to be
        dudraw.set_pen_color_rgb(*colors["light blue"]) #blue
        dudraw.filled_square(fire_x + PARTICLE_SIZE, fire_y + PARTICLE_SIZE, PARTICLE_SIZE)
        #draw a white fire particle in the location underneath where the fire originally was
        dudraw.set_pen_color_rgb(*colors["white"])
        dudraw.filled_square(fire_x + PARTICLE_SIZE , fire_y - 1 + PARTICLE_SIZE, PARTICLE_SIZE)

def replace_fire_in_first_row(matrix: list[list])->None:
    """
        A function that checks the first row of the world list and searches for any fire, if a fire particle is encountered,
        then it gets replaced by sky to make it seem like the fireball falls off the canvas
        param matrix: The 2D list that represents the state of our sand world
        return: None
    """
    #iterate through the first row of the list by index
    for col_index in range(len(matrix[0])):
        #if fire of any color is encountered:
        if matrix[0][col_index] == FIRE_R or matrix[0][col_index] == FIRE_Y or matrix[0][col_index] == FIRE_W:
            #set that value to empty, then draw a sky particle in its place
            matrix[0][col_index] = EMPTY
            dudraw.set_pen_color_rgb(*colors["light blue"])
            dudraw.filled_square(col_index + PARTICLE_SIZE, 0 + PARTICLE_SIZE, PARTICLE_SIZE)

def advance_world(matrix: list[list])->None:
    """
        A function that iterates through a 2D list and checks certain conditions and decides what to do with the particles involved
        param matrix: The 2D list that we iterate through and that represents our game world
        return: None
    """
    #iterate through the list, starting at the first row to avoid an index error
    for row_index in range(1, len(matrix)):
        #sand controls

        #iterate through every particle in the current row
        for col_index in range(len(matrix[row_index])):
            #if we encounter a sand particle and the space below it is empty, make the sand fall down vertically by calling the appropriate function
            if matrix[row_index][col_index] == SAND and matrix[row_index-1][col_index] == EMPTY:
                #pass the col_index as the x coordinate, and the row_index as the y
                sand_falls_vertically(col_index, row_index)
            #first put in a check to make sure we don't make sand flow diagonally outside of the world. 
            #then check if the space underneath is floor, because if it is, then the stand willl stay stationary(Sand flows on other sand but not on floors)
            #then, if we encounter a sand particle and the space underneath and one to the left is empty, call the function that makes sand flow diagonally left
            if col_index - 1 >= 0 and matrix[row_index-1][col_index] != FLOOR and matrix[row_index][col_index] == SAND and matrix[row_index-1][col_index-1] == EMPTY:
                sand_falls_diagonal_left(col_index, row_index)
            #first put in a check to make sure we don't make sand flow diagonally outside of the world. 
            #then check if the space underneath is floor, because if it is, then the stand willl stay stationary(Sand flows on other sand but not on floors)
            #then, if we encounter a sand particle and the space underneath and one to the right is empty, call the function that makes sand flow diagonally right
            if col_index + 1 < WORLD_SIZE and matrix[row_index-1][col_index] != FLOOR and matrix[row_index][col_index] == SAND and matrix[row_index-1][col_index+1] == EMPTY:
                sand_falls_diagonal_right(col_index, row_index)

            #fire controls

            #if we encounter any fire pixels of any color, then call the function that makes that pixel fall down vertically and "burn" other particles
            #make sure to pass the appropriate color depending on the type of particle we encountered
            if matrix[row_index][col_index] == FIRE_R:
                fire_pixel_destroys(col_index, row_index, "red")
            if matrix[row_index][col_index] == FIRE_Y:
                fire_pixel_destroys(col_index, row_index, "yellow")
            if matrix[row_index][col_index] == FIRE_W:
                fire_pixel_destroys(col_index, row_index, "white")
  
#set up constant variables
EMPTY = 0
SAND = 1
FLOOR = 2
#set up three different types of fire constants so that we know what color the pixel is
FIRE_R = 3
FIRE_Y = 4
FIRE_W = 5
#the x and y scale as well as the number of rows/cols in the list
WORLD_SIZE = 150
#the half width of each square/sand particle drawn
PARTICLE_SIZE = 0.5
#set up a dictionary to store our color values
colors = {"light blue" : (173, 216, 230), "tan": (175, 148, 97), "red": (247, 41, 2), "yellow": (249, 250, 166), "white": (248, 248, 248)} 

#setup the initial canvas and create a 2D list that represents the world   
dudraw.set_canvas_size(5*WORLD_SIZE, 5*WORLD_SIZE)
dudraw.set_x_scale(0, WORLD_SIZE)
dudraw.set_y_scale(0, WORLD_SIZE)
#clear the canvas to our light blue color using the unpacking operator
dudraw.clear_rgb(*colors['light blue'])
#use a list comprehension to set up our world list and set everything to empty
#we add 1 more row and 1 more column because since the particles are drawn in the middle of a pixel, we need an extra row and column
world_list = [[EMPTY for _ in range(WORLD_SIZE + 1)] for _ in range(WORLD_SIZE + 1)]

#set up a key variable as an empty string, which we will use for our while loop condition
key = ''
#initialize the mode to sand and draw the sand label in the top left corner
mode = 'sand'
change_label("Sand")

#animation loop that continues while key is not q
while key != 'q':
    #check to see what mode we are in and then change the label accordingly
    if mode == 'sand':
        change_label("Sand")
    if mode == 'floor':
        change_label("Floor")
    if mode == 'destroy':
        change_label("Destroy")
    #check if mouse is pressed:
    if dudraw.mouse_is_pressed():
        #get mouse press location
        x_location = int(dudraw.mouse_x())
        y_location = int(dudraw.mouse_y())
        #if we are in sand mode, then we place sand
        if mode == 'sand':
            #make a variable that is a random int between -3 and 3
            #this is what we will add to our x coordinate to make the sand "sprinkle"
            random_x_cord = random.randint(-3,3)
            #add an additonal check to make sure that we don't go out of the list indeces when we are making the sand "sprinkle"
            if x_location + random_x_cord >= 0 and x_location + random_x_cord < WORLD_SIZE:
                #place sand and add the random number to the x coord each time sand is placed
                place_sand(x_location + random_x_cord, y_location)
        #if we are in floor mode, then place floor using the appropriate function
        if mode == 'floor':
            place_floor(x_location, y_location)
        #if we are in destroy mode, then draw a fireball by using the draw_fireball function
        if mode == 'destroy':
            draw_fireball(x_location, y_location)
    #check if key clicked:
    if dudraw.has_next_key_typed():
        #get the key value
        key = dudraw.next_key_typed()
        #if the key is c, then clear the screen and reset our list so that everything is empty
        if key == "c":
            dudraw.clear_rgb(*colors["light blue"])
            world_list = [[EMPTY for _ in range(WORLD_SIZE + 1)] for _ in range(WORLD_SIZE + 1)]
        #if the key is s, change to sand mode
        if key == 's':
            mode = 'sand'
        #if the key is f, change to floor mode
        if key == 'f':
            mode = 'floor'
        #if the key is d, change to destroy mode
        if key == 'd':
            mode = 'destroy'
    #now, call the advance_world function to advance the world by one step and then display the canvas
    advance_world(world_list)
    dudraw.show()
    #after we show the canvas and the fire pixels drop all the way to the bottom, then replace them with sky to make the fireball "pass" through the screen
    replace_fire_in_first_row(world_list)