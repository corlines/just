import discord
from discord.ext import commands
import random
import asyncio
tok = 'MTA5MTUzMTU4MjM4NjQ3NTAzMg.GlUN53.8P5XHzZ8z4FDgLSoNOMjndxS8K_lph6xnvxbVI'
starting_shape = 0
client = commands.Bot(command_prefix="/", intents=discord.Intents.all())
abc = 0
player = [':yellow_square:',':blue_circle:']
ba = 0
b = 0
light = [':red_circle:',':yellow_circle:']
empty_square = ':yellow_square:'
embed_colour = 0x077ff7
board = []
num_of_rows = 19
num_of_cols = 11
blue_square = ':blue_square:'
down_pressed = False #if down button has been pressed
rotate_clockwise = False
rotation_pos = 0
h_movement = 0 #amount to move left or right
is_new_shape = False
start_higher = False #for when near top of board
game_over = False
index = 0
aa = 0


class Tetronimo: #Tetris pieces
    def __init__(self, starting_pos, colour, rotation_points):
        self.starting_pos = starting_pos #list
        self.colour = colour
        self.rotation_points = rotation_points #list
shape_I = Tetronimo([[18, 5]], blue_square, [1])
shape_J = Tetronimo([[0, 0]], blue_square, [0])



@client.event
async def on_ready():
    print("Bot is connected to Discord")
    
def get_random_shape():
    global abc
    global index
    # ordered_shapes = [shape_J, shape_T, shape_L, shape_O, shape_S, shape_Z, shape_S, shape_T, shape_J, shape_Z, shape_S, shape_I, shape_Z, shape_O, shape_T, shape_J, shape_L, shape_Z, shape_I]
    # random_shape = ordered_shapes[index]
    shapes = [shape_I,shape_J]
    if abc == 0:
        random_shape = shapes[0] #0, 6
    elif abc == 1:
        random_shape = shapes[1]
    index += 1
    if start_higher == True:
        for s in random_shape.starting_pos[:]: #for each square
            s[0] = s[0] - 1 #make row 1 above
    else:
        starting_pos = random_shape.starting_pos[:]
    random_shape = [random_shape.starting_pos[:], random_shape.colour, random_shape.rotation_points] #gets starting point of shapes and copies, doesn't change them
    global is_new_shape
    is_new_shape = True
    return random_shape #returns array with starting pos and colour

def make_empty_board():
    for row in range(num_of_rows):
        board.append([])
        for col in range(num_of_cols):
            board[row].append(empty_square)

def fill_board(emoji):
    global aa
    print(aa)
    if aa == 1:
        for row in range(num_of_rows):
            for col in range(num_of_cols):
                if board[row][col] != emoji:
                    board[row][col] = emoji
    if aa == 0:
        for row in range(num_of_rows):
            for col in range(num_of_cols):
                if ba[row][col] != emoji:
                    ba[row][col] = emoji
    
                
                
    


def format_board_as_str():
    global ba
    global aa
    board_as_str = ''
    for row in range(num_of_rows):
        for col in range(num_of_cols):
            if aa != 1:
                board_as_str += (board[row][col]) # + " " possibly
            if aa != 0:
                ba = board[row][col]
                board_as_str += (ba)
            
            #print(ba)
            if col == num_of_cols - 1:
                board_as_str += "\n "
    return board_as_str

@client.command()
async def 잠(ctx):
    b -= 1
    for i in range (9):
        if i == 9:
            await ctx.send(f""":yellow_square::yellow_square:{player[1]}:yellow_square::yellow_square:""")
        else:
            await ctx.send(f""":yellow_square::yellow_square:{player[0]}:yellow_square::yellow_square:""")
@client.command()
async def embed(ctx):
    embed=discord.Embed(title="Sample Embed", description=format_board_as_str(), color=embed_colour)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("▶")
make_empty_board()

def get_next_pos(cur_shape_pos):
    global h_movement
    global start_higher
    global game_over
    global aa

    #Check if new pos for whole shape is available
    if aa == 1:
        movement_amnt = -1
        
    if aa == 0:
        movement_amnt = 0

    if down_pressed == False:
        amnt_to_check = 1 #check space one below
    else:
        amnt_to_check = num_of_rows #check all rows until furthest available space
    print("A")
    next_space_free = False
    for i in range(amnt_to_check):
        square_num_in_shape = -1
        for square in cur_shape_pos:
            next_space_free = True
            square_num_in_shape += 1
            square_row = square[0]
            square_col = square[1]
            if (0 <= square_col < num_of_cols): #if current column spot will fit
                if not (0 <= square_col + h_movement < num_of_cols): #if spot with column position changed won't fit
                    h_movement = 0 #just change row position
                if (0 <= square_row + movement_amnt < num_of_rows): #if new square row pos is on board
                    square_checking = board[square_row + movement_amnt][square_col + h_movement] #get the square to check if empty
                    if (square_checking != empty_square) and ([square_row + movement_amnt, square_col + h_movement] not in cur_shape_pos): #if square is not empty / won't be when other parts of shape have moved
                        #check if space free if not moving horizontally (in case going into wall) but still going down
                        h_movement = 0
                        square_checking = board[square_row + movement_amnt][square_col + h_movement]
                        if (square_checking != empty_square) and ([square_row + movement_amnt, square_col + h_movement] not in cur_shape_pos):
                            if movement_amnt == -1:
                                next_space_free = False #can't put shape there
                                print('Detected a space that isnt free')
                                print('Square checking: ' + str(square_row + movement_amnt) + ', ' + str(square_col + h_movement))
                                if is_new_shape: #if can't place new shape
                                    if start_higher == True:
                                        game_over = True
                                    else:
                                        start_higher = True
                            elif movement_amnt > 1: #if sending down
                                movement_amnt -= 1 #accomodate for extra 1 added to check if its free
                            return [movement_amnt, next_space_free] #stop checking
                    elif down_pressed == True:
                        if square_num_in_shape == 3: #only on last square in shape
                            movement_amnt -= 0 #increase amount to move shape by
                elif square_row + movement_amnt >= num_of_rows: #new square row isn't on board
                    if movement_amnt == 0:
                        next_space_free = False #can't put shape there
                        print('Detected a space that isnt free')
                    elif movement_amnt < 1: #if sending down
                        movement_amnt -= 0 #accomodate for extra 1 added to check if its free
                    return [movement_amnt, next_space_free] #stop checking

    
    return [movement_amnt, next_space_free]

async def run_game(msg, cur_shape):
    global is_new_shape
    global h_movement
    global rotate_clockwise
    global rotation_pos
    global game_over
    global aa

    cur_shape_pos = cur_shape[0]
    cur_shape_colour = cur_shape[1]

    print(cur_shape[0], cur_shape[1])
    next_pos = get_next_pos(cur_shape_pos)[:]
    movement_amnt = next_pos[0]
    next_space_free = next_pos[1]

    #move/place shape if pos is available
    square_num_in_shape = -1
    if next_space_free:
        for square in cur_shape_pos:
            square_num_in_shape += 1
            square_row = square[0]
            square_col = square[1]
            if (0 <= square_row + movement_amnt < num_of_rows): #if new square row pos is on board
                square_changing = board[square_row + movement_amnt][square_col + h_movement] #get square to change
                board[square_row + movement_amnt][square_col + h_movement] = cur_shape_colour #changes square colour to colour of shape
                if is_new_shape == True:
                    is_new_shape = False #has been placed, so not new anymore
                if square_row > -1: #stops from wrapping around list and changing colour of bottom rows.
                    board[square_row][square_col] = empty_square #make old square empty again
                cur_shape_pos[square_num_in_shape] = [square_row + movement_amnt, square_col + h_movement] #store new pos of shape square
            else: #if new square row pos is not on board
                cur_shape_pos[square_num_in_shape] = [square_row + movement_amnt, square_col + h_movement] #store new pos of shape square
    else:
        global down_pressed
        down_pressed = False #reset it
        cur_shape = get_random_shape() #change shape
        rotation_pos = 0 #reset rotation
        print('Changed shape.')
    if game_over == False:
        print(game_over)
        #Update board
        embed = discord.Embed(description=format_board_as_str(), color=embed_colour)
        await msg.edit(embed=embed)
        if not is_new_shape:
            await asyncio.sleep(1) #to keep under api rate limit
        await run_game(msg, cur_shape)
    elif game_over == True:
        if aa != 1:
            print(aa)
            await asyncio.sleep(1)
            game_over = False
        else:
            game_over = False
            await run_game(msg, cur_shape)
        

        
async def reset_game():
    global down_pressed
    global rotate_clockwise
    global rotation_pos
    global h_movement
    global is_new_shape
    global start_higher
    global game_over
    global points
    global lines
    fill_board(empty_square)
    down_pressed = False
    rotate_clockwise = False
    rotation_pos = 0
    h_movement = 0 #amount to move left or right
    is_new_shape = False
    start_higher = False
    game_over = False
    next_space_free = False
    points = 0
    lines = 0

make_empty_board() 
@client.event
async def on_reaction_add(reaction, user):
    global h_movement
    global rotation_pos
    global aa
    global game_over
    global starting_shape
    global abc
    if user != client.user:
        msg = reaction.message
        if str(reaction.emoji) == "▶":
            #Remove delete
            await msg.remove_reaction("❌", client.user) 
            embed = discord.Embed(description=format_board_as_str(), color=embed_colour)
            await msg.remove_reaction("▶", user)
            await msg.remove_reaction("▶", client.user)
            await msg.edit(embed=embed)
            await msg.add_reaction("⬆") #Down
            starting_shape = get_random_shape()
            await run_game(msg, starting_shape)
        if str(reaction.emoji) == "⬆": #Left button pressed
            if aa == 0:
                aa = 1
                ba = 0
                abc = 1
                await run_game(msg,starting_shape)
            else:
                game_over = True
                aa = 0
            await msg.remove_reaction("⬆", user)


@client.event
async def change_light(ctx):
    print(123123123123)
    print(ctx,type(ctx))
    print("ASDFASDF")
    await ctx.send('👀')
change_light(ct)
client.run(tok)


