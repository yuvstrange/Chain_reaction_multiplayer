class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.p3Went = False
        self.ready = False
        self.id = id
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
        self.player_array = [0] * 2

        self.wins = [0, 0, 0]
        self.ties = 0
        self.moves = 0
        self.iterator = 1

    def read_pos(self,str):
        str = str.split(",")
        return (int(str[0]), int(str[1]))

    def play(self, player,move):
        print(player,move)

        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True
        if self.iterator == player:
            i, j = self.read_pos(move)
            self.player_input(i, j, player)
            print(self.board)
            self.iterator = (self.iterator % 2) + 1


    def getBoard(self):
        return self.board

    def player_input(self, i, j, player):
        if (self.board[i][j][1] == player or self.board[i][j][1] == 0):
            self.moves = self.moves + 1
            self.update_move(i, j, player)
            if (self.moves > len(self.player_array)):
                if (self.check_if_won()):
                    print("Player ", player, "won")
        else:
            print("Inavlid Entry")
            return


    def check_if_won(self):
        count = 0
        for i in range(len(self.player_array)):
            if (self.player_array[i] != 0):
                count += 1
                if count > 1:
                    break
        if (count > 1):
            return False
        else:
            return True

    def update_move(self, i, j, player):

        if ((i < 0 or j < 0) or (i >= self.row_length or j >= self.col_length)):
            return

        if (self.board[i][j][1] != player):
            if (self.board[i][j][1] != 0):
                self.player_array[self.board[i][j][1] - 1] -= 1
            self.board[i][j][1] = player
            self.player_array[player - 1] += 1

        if ((i != 0 and i != self.row_length - 1) and (j != 0 and j != self.col_length - 1)):
            if (self.board[i][j][0] == 3):
                self.board[i][j] = [0, 0]
                self.player_array[player - 1] -= 1

                self.update_move(i + 1, j, player)
                self.update_move(i - 1, j, player)
                self.update_move(i, j + 1, player)
                self.update_move(i, j - 1, player)
            else:
                self.board[i][j][0] += 1
        elif ((i == 0 or i == self.row_length - 1) and (j == 0 or j == self.col_length - 1)):
            if (self.board[i][j][0] == 1):
                self.board[i][j] = [0, 0]
                self.player_array[player - 1] -= 1

                self.update_move(i + 1, j, player)
                self.update_move(i - 1, j, player)
                self.update_move(i, j + 1, player)
                self.update_move(i, j - 1, player)
            else:
                self.board[i][j][0] += 1
        else:
            if (self.board[i][j][0] == 2):
                self.board[i][j] = [0, 0]
                self.player_array[player - 1] -= 1

                self.update_move(i + 1, j, player)
                self.update_move(i - 1, j, player)
                self.update_move(i, j + 1, player)
                self.update_move(i, j - 1, player)
            else:
                self.board[i][j][0] += 1

    def winner(self):
        flag = 0
        a = -1
        ctr = 0
        ptr = 0
        for i in range(self.row_length):
            for j in range(self.col_length):
                if self.board[i][j][0] != 0:
                    ctr += 1
                if ctr == 2 :
                    ptr = 1
                    break
        if ptr == 0:
            return -1

        for i in range(self.row_length):
            for j in range(self.col_length):
                if self.board[i][j][1] != 0:
                    a = self.board[i][j][1]
                    break

        for i in range(self.row_length):
            for j in range(self.col_length):
                if self.board[i][j][1] != 0 :
                    if self.board[i][j][1] != a:
                        flag = 1
                        break
                    else :
                        continue
        if flag == 1:
            return -1
        else:
            return a



    def connected(self):
        return self.ready

    def allWent(self):
        return self.p1Went and self.p2Went


    def resetWent(self):
        self.p1Went = False
        self.p2Went = False