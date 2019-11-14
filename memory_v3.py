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

        # state of the whole board and clicked point
        self.state = [0] * pow(self.board_size, 2)
        self.click_x = 0
        self.click_y = 0

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
        self.tiles *= 2
        # shuffle board
        random.shuffle(self.tiles)

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()            
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
        height = self.surface.get_height()//self.board_size
        index = 0

        # for row and col in matrix (i.e. for every cell), create a tile class obj
        for row_index in range(0, self.board_size):
            row = []
            for col_index in range(0,self.board_size):
                # added margins
                # sourced from
                # https://stackoverflow.com/questions/41886369/pygame-offset-a-grid-made-out-of-rectangles (first answer)
                x = (1+height) * col_index + 2
                y = (1+height) * row_index + 2

                # using a test area of tile, test if the click overlaps with the tile
                # if so, change the state of the tile to 1, meaning flipped
                test_area = pygame.Rect(x,y,height,height)
                if test_area.collidepoint(self.click_x, self.click_y):
                    self.state[index] = 1

                tile = Tile(x, y, self.tiles[index], self.state[index])
                row.append(tile)
                index += 1

            # append the list in the board list
            # (this will be like a 4x4 matrix)
            self.board.append(row)

        self.frame_counter = self.frame_counter + 1

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        
        # TODO: game ends when * cards are flipped

        if 0 in self.state:
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
    border_size = 2
    border_color = pygame.Color('black')
    question = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image0.bmp'))

    # decorator with class attributes that sets surface
    @classmethod
    def set_surface(cls, game_surface):
        # Sets the surface of Tile
        # - cls is the class (i.e. Tile)
        # - game_surface is the surface to draw on

        cls.surface = game_surface

    # Instance Methods
    def __init__(self, x, y, image, state):
        # Initialize a Tile.
        # - self is the Tile to initialize
        # - x is the x coord of the image
        # - y is the y coord of the image
        # - image is the image to draw to the coords
        # - state is the bool state of the tile (0 = unknown, 1 = known)

        self.x = x
        self.y = y
        self.image = image
        self.state = state


    def draw(self):
        # Draw the tile on the surface
        # - self is the Tile

        if self.state:
            Tile.surface.blit(self.image, (self.x, self.y))
        else:
            Tile.surface.blit(Tile.question, (self.x, self.y))

main()
