import pygame
import time
import numpy as np

display_height = 600
display_width = 800
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(gameDisplay, text, x, y, size):
    largeText = pygame.font.SysFont('comicsansms', size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


def single_click(gameDisplay, color, center):
    x, y = center
    pygame.draw.circle(gameDisplay, color, (x+25, y+25), 8)


def double_click(gameDisplay, color, center):
    x, y = center
    pygame.draw.circle(gameDisplay, color, (x+20, y+25), 8)
    pygame.draw.circle(gameDisplay, color, (x+30, y+25), 8)


def triple_click(gameDisplay, color, center):
    x, y = center
    pygame.draw.circle(gameDisplay, color, (x+20, y+20), 8)
    pygame.draw.circle(gameDisplay, color, (x+30, y+20), 8)
    pygame.draw.circle(gameDisplay, color, (x+25, y+30), 8)


def display_rect(gameDisplay, color, start_x, start_y, end_x, end_y):
    pygame.draw.rect(gameDisplay, color, [start_x, start_y, end_x, end_y])


def display_name(gameDisplay):
    size = 22
    x = 75
    message_display(gameDisplay, 'Players', x, 70, 30)
    message_display(gameDisplay, 'Yashi', x, 120, size)
    message_display(gameDisplay, 'Yuvraj', x, 150, size)
    message_display(gameDisplay, 'Shrey', x, 180, size)
    message_display(gameDisplay, 'Siddhant', x, 210, size)

    pygame.display.update()


def get_block():
    x = 250
    coordinates = {}
    for i in range(6):
        y = 50
        for j in range(9):
            coordinates[(x, y)] = (j, i)
            y += 50
        x += 50
    return coordinates


def get_cord():
    a = get_block()
    b = dict()
    for i in a:
        b[a[i]] = i
    return b


def display_board(gameDisplay, color):
    x = 250
    y = 50
    line_width = 1
    display_rect(gameDisplay, black, x, y, 300, 450)

    for i in range(8):
        y += 50
        display_rect(gameDisplay, color, x, y, 300, line_width)
    y = 50
    for i in range(5):
        x += 50
        display_rect(gameDisplay, color, x, y, line_width, 450)

    pygame.display.update()


"""FINAL CODE"""


class chain_reaction:
    def __init__(self, n):
        self.board = [[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                      [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                      [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                      [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                      [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                      [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                      [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                      [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                      [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]]
        self.row_length = len(self.board)
        self.col_length = len(self.board[0])
        self.count = n
        self.moves = 0
        self.player_array = [0]*n

        pygame.init()

        self.gameDisplay = pygame.display.set_mode(
            (display_width, display_height))
        pygame.display.set_caption('Chain Reaction')

        self.gameDisplay.fill(white)
        pygame.display.update()

        self.mat_dict = self.get_block()
        self.cord_dict = self.get_cord()
        self.x, self.y = (0, 0)
        self.iterator = 0

        self.color = [green, red, blue]

        display_name(self.gameDisplay)
        display_board(self.gameDisplay, self.color[0])
        print("init")
        self.start_game()

    def get_block(self):
        print("get block")
        x = 250
        coordinates = {}
        for i in range(6):
            y = 50
            for j in range(9):
                coordinates[(x, y)] = (j, i)
                y += 50
            x += 50
        return coordinates

    def get_cord(self):
        print("get cord")
        a = get_block()
        b = dict()
        for i in a:
            b[a[i]] = i
        return b

    def player_input(self, i, j, player):
        print("player input")
        if(self.board[i][j][1] == player or self.board[i][j][1] == 0):
            self.moves = self.moves + 1
            self.update_move(i, j, player)

            if(self.moves > len(self.player_array)):
                if(self.check_if_won()):
                    print("Player ", player, "won")
        else:
            print("Inavlid Entry")
            return
        for i in range(self.row_length):
            for j in range(self.col_length):
                if self.board[i][j][0] == 0:
                    continue
                elif self.board[i][j][0] == 1:
                    single_click(self.gameDisplay, self.color[self.board[i][j][1]-1],
                                 self.cord_dict[(i, j)])
                elif self.board[i][j][0] == 2:
                    double_click(self.gameDisplay, self.color[self.board[i][j][1]-1],
                                 self.cord_dict[(i, j)])
                elif self.board[i][j][0] == 3:
                    triple_click(self.gameDisplay, self.color[self.board[i][j][1]-1],
                                 self.cord_dict[(i, j)])
                else:
                    pass
        pygame.display.update()

    def check_if_won(self):
        print("check if won")
        count = 0
        for i in range(len(self.player_array)):
            if(self.player_array[i] != 0):
                count += 1
                if count > 1:
                    break
        if(count > 1):
            return False
        else:
            return True

    def update_move(self, i, j, player):
        print("update move")
        if((i < 0 or j < 0) or (i >= self.row_length or j >= self.col_length)):
            return

        if(self.board[i][j][1] != player):
            if(self.board[i][j][1] != 0):
                self.player_array[self.board[i][j][1] - 1] -= 1
            self.board[i][j][1] = player
            self.player_array[player - 1] += 1

        if((i != 0 and i != self.row_length-1) and (j != 0 and j != self.col_length-1)):
            if(self.board[i][j][0] == 3):
                self.board[i][j] = [0, 0]
                self.player_array[player - 1] -= 1

                self.update_move(i+1, j, player)
                self.update_move(i-1, j, player)
                self.update_move(i, j+1, player)
                self.update_move(i, j-1, player)
            else:
                self.board[i][j][0] += 1
        elif((i == 0 or i == self.row_length - 1) and (j == 0 or j == self.col_length - 1)):
            if(self.board[i][j][0] == 1):
                self.board[i][j] = [0, 0]
                self.player_array[player - 1] -= 1

                self.update_move(i+1, j, player)
                self.update_move(i-1, j, player)
                self.update_move(i, j+1, player)
                self.update_move(i, j-1, player)
            else:
                self.board[i][j][0] += 1
        else:
            if(self.board[i][j][0] == 2):
                self.board[i][j] = [0, 0]
                self.player_array[player - 1] -= 1

                self.update_move(i+1, j, player)
                self.update_move(i-1, j, player)
                self.update_move(i, j+1, player)
                self.update_move(i, j-1, player)
            else:
                self.board[i][j][0] += 1

    def is_game_over(self):
        print("is game over")
        count = 0
        for i in range(len(self.player_array)):
            if(self.player_array[i] != 0):
                count += 1
                if count > 1:
                    break
        if self.moves < len(self.player_array) or count > 1:
            return False
        else:
            return True

    def start_game(self):
        print("start game")
        while(self.is_game_over() == False):
            self.iterator = 1
            # pygame.display.update()
            while(self.iterator <= len(self.player_array)):
                move_x, move_y = (0, 0)
                pygame.display.update()
                if(self.if_player_can_continue(self.iterator)):
                    flag = True
                    while flag:
                        for event in pygame.event.get():
                            mouse = pygame.mouse.get_pos()
                            click = pygame.mouse.get_pressed()
                            if click[0] == 1:
                                display_board(self.gameDisplay,
                                              self.color[self.iterator % self.count])
                                self.x, self.y = mouse
                                a = self.x % 50
                                b = self.y % 50
                                self.x, self.y = self.x-a, self.y-b
                                move_x, move_y = self.mat_dict[(
                                    self.x, self.y)]
                                flag = False
                    self.player_input(move_x, move_y, self.iterator)
                self.iterator += 1

    def if_player_can_continue(self, player):
        print("if player can continue")
        if(self.moves < len(self.player_array) or self.player_array[player-1] > 0):
            return True
        else:
            return False


cr = chain_reaction(3)

