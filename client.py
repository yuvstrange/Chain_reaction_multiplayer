

from network import Network

import pygame
import time

from rock_game import  Game



black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
display_width = 600
display_height = 600
yellow = (255, 71, 26)

"""FINAL CODE"""
def text_objects(text, font):
    textSurface = font.render(text, True, yellow)
    return textSurface, textSurface.get_rect()

def message_display( gameDisplay, text, x, y, size):
    largeText = pygame.font.SysFont('comicsansms', size)
    TextSurf, TextRect =  text_objects(text, largeText)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)


def single_click( gameDisplay, color, center):
    x, y = center
    pygame.draw.circle( gameDisplay, color, (x+25, y+25), 8)

def double_click( gameDisplay, color, center):
    x, y = center
    pygame.draw.circle( gameDisplay, color, (x+20, y+25), 8)
    pygame.draw.circle( gameDisplay, color, (x+30, y+25), 8)

def triple_click( gameDisplay, color, center):
    x, y = center
    pygame.draw.circle( gameDisplay, color, (x+20, y+20), 8)
    pygame.draw.circle( gameDisplay, color, (x+30, y+20), 8)
    pygame.draw.circle( gameDisplay, color, (x+25, y+30), 8)

def display_rect( gameDisplay, color, start_x, start_y, end_x, end_y):
    pygame.draw.rect( gameDisplay, color, [
                     start_x, start_y, end_x, end_y])


def get_cord():
    a =  get_block()
    b = dict()
    for i in a:
        b[a[i]] = i
    return b




def DrawBoard(game, player):
    pygame.init()

    gameDisplay = pygame.display.set_mode(
        (display_width, display_height))
    pygame.display.set_caption('Chain Reaction')

    gameDisplay.fill(white)

    color = red


    x = 250
    y = 50
    board_from_server = game.getBoard()
    row_length = len(board_from_server)
    col_length = len(board_from_server[0])
    line_width = 1
    display_rect(gameDisplay,black, x, y, 300, 450)
    cord_dict = get_cord()
    for i in range(8):
        y += 50
        display_rect(gameDisplay, color, x, y, 300, line_width)
    y = 50
    for i in range(5):
        x += 50
        display_rect(gameDisplay, color, x, y, line_width, 450)
    color_list = [green,red,blue]
    for i in range( row_length):
        for j in range( col_length):
            color_disp = board_from_server[i][j][1]
            if board_from_server[i][j][0] == 0:
                continue
            elif board_from_server[i][j][0] == 1:
                single_click( gameDisplay, color_list[color_disp-1],
                                   cord_dict[(i, j)])
            elif board_from_server[i][j][0] == 2:
                double_click( gameDisplay, color_list[color_disp-1],
                                   cord_dict[(i, j)])
            elif board_from_server[i][j][0] == 3:
                triple_click( gameDisplay, color_list[color_disp-1],
                                  cord_dict[(i, j)])
            else:
                pass
    message_display(gameDisplay, str("Player : "+str(player)), 75, 70, 30)
    if (game.winner() != -1) :
        win = game.winner()
        message_display(gameDisplay,str("Player "+str(win)+" won"),display_width/2-50,display_height/2-20,80)
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        return

    pygame.display.update()



def get_block( ):
    x = 250
    coordinates = {}
    for i in range(6):
        y = 50
        for j in range(9):
            coordinates[(x, y)] = (j, i)
            y += 50
        x += 50
    return coordinates




def main():
    game = Game(0)
    pygame.init()
    global run
    run = True
    clock = pygame.time.Clock()
    n = Network()
    mat_dict = get_block()
    move_x = -1
    move_y = -1

    player = int(n.getP())
    print("You are player", player)


    while run:
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game ")
            break

        clock.tick(60)



        if game.allWent():


            DrawBoard(game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game ")
                break





            #pygame.display.update()

        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()



            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN :
                x, y = mouse
                a = x % 50
                b = y % 50
                x,y = x - a, y - b
                try:
                    move_x, move_y = mat_dict[(x, y)]
                    if game.winner() == -1 :
                        move = str(str(move_x) + ',' + str(move_y))

                        n.send(move)
                    else:
                        time.sleep(3)
                        pygame.quit()
                except Exception as e:
                    print(e)


                pygame.time.delay(2000)
        DrawBoard(game, player)




while True:
    main()






