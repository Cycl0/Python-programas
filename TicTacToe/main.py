#!/usr/bin/env python3
import numpy as np
from random import randrange

__author__ = "Lucas Kenzo Cyra"
__version__ = "0.1.0"
__license__ = "MIT"

GRID_SIZE = 3

class TicTacToe:
    def __init__(self, cpu_symbol, user_symbol):
        self.tiles = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.rows = np.zeros(GRID_SIZE, dtype=int)
        self.cols = np.zeros(GRID_SIZE, dtype=int)
        self.diag = 0
        self.anti_diag = 0
        self.user_symbol = user_symbol
        self.cpu_symbol = cpu_symbol
        self.cpu_turn = True
        self.winner = None
        self.turn_num = 0
        self.difficulty = 1

    def __victory_for(self, x, y, mark):
        # A função analisa o estado da placa a fim de verificar se 
        # o jogador usando 'O's ou 'X's ganhou o jogo
        cpu_turn = self.cpu_turn
        rows = self.rows
        cols = self.cols

        rows[x] += mark
        cols[y] += mark
        if x == y: # (0,0), (1,1) or (2,2)
            self.diag += mark
        if x + y == GRID_SIZE - 1: # (0,2), (1,1) or (2,0)
            self.anti_diag += mark
        if (abs(rows[x]) == GRID_SIZE or
           abs(cols[y]) == GRID_SIZE or
           abs(self.diag) == GRID_SIZE or
           abs(self.anti_diag) == GRID_SIZE):
               self.winner = 1 if cpu_turn else 2 # se cpu ganhou retorna 1, se user ganhou retorna 2

    def __make_move(self, pos):
        cpu_turn = self.cpu_turn
        tiles = self.tiles
        victory_for = self.__victory_for

        mark = 1 if cpu_turn else -1
        x, y = pos
        tiles[x][y] = mark
        victory_for(x, y, mark)
        self.cpu_turn = not cpu_turn # toggle do turno

    def __display_board(self):
        # A função aceita um parâmetro contendo o status atual da placa
        # e o imprime no console.
        self.index = 0
        self.arr_ravel = self.tiles.ravel()
        def printSymbol():
            i = self.index
            symbol = i + 1
            if self.arr_ravel[i] == 1:
                symbol = self.cpu_symbol
            elif self.arr_ravel[i] == -1:
                symbol = self.user_symbol
            print(symbol, end='')
            self.index += 1

        for i in range(GRID_SIZE):
            print(('+' + '-' * 7) * GRID_SIZE + '+')
            for j in range(3):
                for k in range(GRID_SIZE):
                    if j == 1:
                        print('|' + (' ' * 3), end='')
                        printSymbol()
                        print((' ' * 3), end='')
                    else:
                        print('|' + (' ' * 7), end='')
                print("|")
        print(('+' + '-' * 7) * GRID_SIZE + '+')

    def __make_list_of_free_fields(self):
        # A função navega pelo tabuleiro e constrói uma lista de todas as casas livres; 
        # a lista consiste em tuplas, enquanto cada tupla é um par de números de linha e coluna.
        free_fields = np.where(self.tiles == 0)
        free_fields = list(zip(*free_fields)) # lista de tuples (x,y) das posicoes vazias
        return free_fields

    @staticmethod
    def __format_input(move):
        x = (move - 1) // 3
        y = (move - 1) % 3
        return (x,y)

    def __user_move(self):
        # A função aceita o status atual do tabuleiro, pergunta ao usuário sobre sua jogada, 
        # verifica a entrada e atualiza o quadro de acordo com a decisão do usuário.
        format_input = self.__format_input
        make_list_of_free_fields = self.__make_list_of_free_fields
        make_move = self.__make_move
        display_board = self.__display_board
        user_move = self.__user_move

        move = None
        while True:
            try:
                move = int(input("Escolha a posicao (1-9): "))
                if move < 1 or move > 9:
                    raise ValueError("Valor deve ser entre 1 e 9")
                move = format_input(move)
                free_fields = make_list_of_free_fields()
                if move not in free_fields:
                    raise ValueError("Posicao ja ocupada")
                break
            except ValueError as err:
                print(err)
        if move is not None:
            make_move(move) # Faz o movimento e atualiza o tabuleiro
            display_board() # Mostra o tabuleiro

    @staticmethod 
    def __make_random_move(free_fields):
        i = randrange(len(free_fields))
        move = free_fields[i]
        return move

    def __is_winning_move(self, move, mark):
        x, y = move
        imminent_win_score = mark * (GRID_SIZE - 1)
        return (self.rows[x] == imminent_win_score or
                self.cols[y] == imminent_win_score or
                (x == y and self.diag == imminent_win_score) or
                (x + y == (GRID_SIZE - 1) and self.anti_diag == imminent_win_score))

    def __make_critical_move(self, free_fields):
        is_winning_move = self.__is_winning_move

        move = None
        win = None
        block = None
        for m in free_fields:
            # Checa movimentos se for uma vitoria iminente
            if is_winning_move(m, 1): # Se cpu pode ganhar com um movimento
                win = m
                break
            # Checa movimentos de bloqueio criticos se nao houver vitoria iminente
            elif is_winning_move(m, -1): # Se usuario pode ganhar com um movimento
                block = m
        move = win or block
        return move

    def __cpu_move(self):
        # A função desenha o movimento do computador e atualiza o tabuleiro.
        make_move = self.__make_move
        display_board = self.__display_board
        make_list_of_free_fields = self.__make_list_of_free_fields
        make_random_move = self.__make_random_move
        make_critical_move = self.__make_critical_move
        #make_best_move = self.__make_best_move

        free_fields = make_list_of_free_fields()
        move = None
        if self.difficulty == 1:
            move = make_random_move(free_fields)
        elif self.difficulty == 2:
            move = make_critical_move(free_fields)
        elif self.difficulty == 3:
            move = make_best_move(free_fields)
        else:
            print("Error in cpu difficulty setting and moves")
            return
        if move is None:
            move = make_random_move(free_fields)
        make_move(move) # Faz o movimento e atualiza o tabuleiro
        display_board() # Mostra o tabuleiro

    def next_turn(self):
        cpu_turn = self.cpu_turn
        cpu_move = self.__cpu_move
        user_move = self.__user_move
        turn_num = self.turn_num
        winner = self.winner

        if turn_num == 9:
            self.winner = 3 # Retorna 3 se for empate
            return
        self.turn_num += 1
        cpu_move() if cpu_turn else user_move() # Alterna turnos

    def end_message(self):
        winner = self.winner
        if winner == 1:
            print("Computador ganhou")
        elif winner == 2:
            print("Usuario ganhou")
        elif winner == 3:
            print("Empate")

def main():
    while(True):
        game = TicTacToe("X", "O")
        game.difficulty = 2
        while not game.winner:
            game.next_turn()
        game.end_message()
        again = input("Denovo? [S/n] ").lower()
        if (again != 's' and
            again != ''):
            break

if __name__ == "__main__":
    main()
