# Memory Version 1 - Andrew Li
# This program is a matching game that consists of a 4x4 matrix.
# You try to match the tiles of two chooses tiles by 
# fliping the tiles (future versions) via clicking on the tiles
# Version 2 - first version plus scoring
# event handling of clicks and having the game end when
# all tiles are flipped

# import pygame and random and os for file path
import pygame
import random
import os


# User-defined functions

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((520, 415))
    # set the title of the display window
    pygame.display.set_caption('Memory')   
    # get the display surface
    w_surface = pygame.display.get_surface() 
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play() 
    # quit pygame and clean up the pygame window
    pygame.quit() 


# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game

        self.surface = surface
        self.bg_color = pygame.Color('black')
        self.fg_color = pygame.Color('white')
        
        # timing, frames and some inits for the game
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.time = 0
        self.close_clicked = False
        self.continue_game = True
        self.frame_counter = 0
        
        # === game specific objects
        self.board = []
        self.tiles = []
        self.board_size = 4
        self.create_board()
        self.text()
        self.change = 0
        self.previous = 0

        # state of the whole board and clicked point
        self.click_x, self.click_y = 0, 0

        self.tile_selected_flag = False
        self.time_pause = False

    def create_board(self):
        # create the board shown
        # - self is the game class

        # sets surface of game
        Tile.set_surface(self.surface) 
        # since the tile and grid is square and we base the game off of the height,
        # only height is necessary

        # insert board
        for i in range(self.board_size*2):
            # TODO: remove for unix systems
            # append image to tile set
            self.tiles.append(pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image'+ str(1 + i) + '.bmp')))

        # since the tiles comes in pairs, 
        # add two of the same image, then shuffle
        self.tiles += self.tiles
        # shuffle board
        random.shuffle(self.tiles)

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()

            # If time is pause (giving a second for incorrect tile)
            # then pause for 1 second and change 
            # the current and previous state for not active
            if self.time_pause:
                pygame.time.wait(1000)
                Tile(0).change(self.change)
                self.time_pause = False
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        # added click events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.click_x, self.click_y = event.pos

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
        
        self.surface.fill(self.bg_color) # clear the display surface first
        # Draw the tiles
        for each_row in self.board:
            for each_tile in each_row:
                each_tile.draw()
        
        # draws text
        self.text()
        pygame.display.update() # make the updated surface appear on the display


    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update

        # inits height and index
        index = 0

        # for row and col in matrix (i.e. for every cell), create a tile class obj
        for row_index in range(0, self.board_size):
            row = []
            for col_index in range(0, self.board_size):
                tile = Tile(index, row_index, col_index, self.tiles[index])

                # if collides with tile that has not been clicked
                if tile.collision(self.click_x, self.click_y, self.tile_selected_flag):
                    tile.change_state(1)
                    self.change = index

                    if self.tile_selected_flag:
                        # if it is not the same tile, revert changes
                        if not tile == self.previous:
                            self.time_pause = True
                    else:
                        self.previous = tile

                    # flip the tile selected flag
                    self.tile_selected_flag = not self.tile_selected_flag

                    # sets clicked back to 0, 0
                    self.click_x = 0
                    self.click_y = 0

                row.append(tile)
                index += 1

            # append the list in the board list
            # (this will be like a 4x4 matrix)
            self.board.append(row)

        self.frame_counter = self.frame_counter + 1

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check

        if Tile(0).is_end():
            self.continue_game = True
        else:
            self.continue_game = False

    def text(self):
        # displays the text score
        # - self is the Game class

        # set font to 75 and if the game is still going, display time
        # else, do not change the time for the game has ended
        font = pygame.font.SysFont('', 75)
        
        if self.continue_game:
            self.time = str(pygame.time.get_ticks()//1000)


        # displays text box at the top, right hand side
        text_box = font.render(self.time, True, self.fg_color, self.bg_color)
        text_rect = text_box.get_rect() # get rect from textbox
        text_rect.right = self.surface.get_width()
        coordinate = text_rect

        # prints to surface
        self.surface.blit(text_box, coordinate)


class Tile:
    # An object in this class represents a Tile 

    # Shared Attributes or Class Attributes
    surface = None
    border_color = pygame.Color('black')
    board_size = 4
    state = [0] * pow(board_size, 2)
    height = 415//board_size
    question = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image0.bmp'))
    previous_image = 0
    previous_image_index = -1

    # decorator with class attributes that sets surface
    @classmethod
    def set_surface(cls, game_surface):
        # Sets the surface of Tile
        # - cls is the class (i.e. Tile)
        # - game_surface is the surface to draw on

        cls.surface = game_surface

    # Instance Methods
    def __init__(self, index, col_index = 0, row_index = 0, image=0):
        # Initialize a Tile.
        # - self is the Tile to initialize
        # - x is the x coord of the image
        # - y is the y coord of the image
        # - image is a tuple containing the number of the image and the image obj
        # - state is the bool state of the tile (0 = unknown, 1 = known)

        # added margins
        # sourced from
        # https://stackoverflow.com/questions/41886369/pygame-offset-a-grid-made-out-of-rectangles (first answer)
        self.x = (1+Tile.height) * col_index + 2
        self.y = (1+Tile.height) * row_index + 2
        self.current_state = index

        self.image = image


    def __eq__(self, other):
        return pygame.image.tostring(self.get_image(), "RGBA") == pygame.image.tostring(other.get_image(), "RGBA")


    def get_image(self):
        return self.image

    def draw(self):
        # Draw the tile on the surface
        # - self is the Tile

        if Tile.state[self.current_state]:
            Tile.surface.blit(self.image, (self.x, self.y))
        else:
            Tile.surface.blit(Tile.question, (self.x, self.y))

    def change_state(self, new_state):
        Tile.state[self.current_state] = new_state

    def change(self, change):
        Tile.state[change] = 0
        Tile.state[Tile.previous_image_index] = 0

    def collision(self, click_x, click_y, flag):
        # collision is to test collision given compare_tile
        # - self is Tile class
        # - click_x is the x coord of click
        # - click_y is the y coord of click

        is_collided = pygame.Rect(self.x, self.y, Tile.height, Tile.height).collidepoint(click_x, click_y)

        if is_collided and not flag:
            Tile.previous_image_index = self.current_state

        return is_collided and not Tile.state[self.current_state]


    def test(self, current):
        # tests to see if the two selected tiles are the same
        # - self is the Tile class
        # - current is the image obj

        if Tile.previous_image == current:
            return True
        return False

    def is_end(self):
        return 0 in Tile.state

main()
