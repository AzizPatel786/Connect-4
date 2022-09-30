import sys

import pygame


class GameBoard:
    def __init__(self, size):
        self.size = size
        self.num_entries = [0] * size
        self.items = [[0] * size for i in range(size)]
        self.points = [0] * 2

    def num_free_positions_in_column(self, column):
        free_pos = 0
        for row in range(self.size):
            if self.items[column][row] == 0:
                free_pos += 1
        return free_pos

    def game_over(self):
        for col in range(self.size):
            if self.num_free_positions_in_column(col) != 0:
                return False
        return True

    def display(self, screen):
        for row in range(self.size - 1, -1, -1):
            for col in range(0, self.size):
                if self.items[col][row] == 0:
                    print(end='  ')
                elif self.items[col][row] == 1:
                    print(end='o ')
                elif self.items[col][row] == 2:
                    print(end='x ')
            print()
        for dash in range(self.size * 2 - 1):
            print(end='-')
        print()
        for num in range(self.size):
            print(num, end=' ')
        print()
        print(f'Points player 1: {self.points[0]}')
        print(f'Points player 2: {self.points[1]}')
        blue = (0, 0, 255)
        black = (0, 0, 0)
        for col in range(self.size):
            for row in range(self.size):
                pygame.draw.rect(screen, blue, (col * 100, row * 100 + 100, 100,
                                                100))
                pygame.draw.circle(screen, black, (int(col * 100 + 100 / 2),
                                                   int(row * 100 + 100 + 100 / 2)),
                                   100/2 - 5)

    def num_new_points(self, column, row, player):
        vertical_count = 0
        horz_count = 0
        diag_ltor = 0
        diag_rtol = 0
        for col in range(column - 3, column + 1):
            if col >= 0:
                try:
                    if self.items[col][row] == player and self.items[col + 1][
                        row] == player and self.items[col + 2][
                        row] == player and self.items[col + 3][row] == player:
                        horz_count += 1
                except IndexError:
                    continue
        for row1 in range(row - 3, row + 1):
            if row1 >= 0:
                try:
                    if self.items[column][row1] == player and \
                            self.items[column][row1 + 1] == player and \
                            self.items[column][row1 + 2] == player and \
                            self.items[column][row1 + 3] == player:
                        vertical_count += 1
                except IndexError:
                    continue
        for shift in range(-3, 1):
            if column + shift >= 0 and row + shift >= 0:
                try:
                    if self.items[(column + shift)][(row + shift)] == player and \
                            self.items[(column + shift + 1)][
                                (row + shift + 1)] == player and \
                            self.items[(column + shift + 2)][
                                (row + shift + 2)] == player and \
                            self.items[(column + shift + 3)][
                                (row + shift + 3)] == player:
                        diag_rtol += 1
                except IndexError:
                    continue
        for shift in range(-3, 1):
            if column + shift >= 0 and row - shift - 3 >= 0:
                try:
                    if self.items[(column + shift)][(row - shift)] == player and \
                            self.items[(column + shift + 1)][
                                (row - shift - 1)] == player and \
                            self.items[(column + shift + 2)][
                                (row - shift - 2)] == player and \
                            self.items[(column + shift + 3)][
                                (row - shift - 3)] == player:
                        diag_ltor += 1
                except IndexError:
                    continue
        return vertical_count + horz_count + diag_ltor + diag_rtol

    def add(self, column, player):
        if self.num_entries[
            column] >= self.size or column < 0 or column >= self.size:
            return False
        else:
            for row in range(len(self.num_entries)):
                if self.items[column][row] == 0 and column < self.size:
                    self.items[column][row] = player
                    self.points[player - 1] += self.num_new_points(column, row,
                                                                   player)
                    self.num_entries[column] += 1
                    return True

    def free_slots_as_close_to_middle_as_possible(self):
        output_list = []
        if self.size % 2 == 0:
            column_2 = int(self.size / 2)
            column_1 = column_2 - 1
            while column_1 >= 0 and column_2 < self.size:
                if self.num_free_positions_in_column(column_1) > 0:
                    output_list.append(column_1)
                if self.num_free_positions_in_column(column_2) > 0:
                    output_list.append(column_2)
                column_2 += 1
                column_1 -= 1
        else:  # Odd size boards
            middle = int(self.size / 2)
            column_2 = middle + 1
            column_1 = middle - 1
            if self.num_free_positions_in_column(middle) > 0:
                output_list.append(middle)
            while column_1 >= 0 and column_2 < self.size:
                if self.num_free_positions_in_column(column_1) > 0:
                    output_list.append(column_1)
                if self.num_free_positions_in_column(column_2) > 0:
                    output_list.append(column_2)
                column_2 += 1
                column_1 -= 1
        return output_list

    def column_resulting_in_max_points(self, player):
        available_moves = []
        slot_number_for_max_points = []
        max_points = 0
        for free_slot_column in self.free_slots_as_close_to_middle_as_possible():
            row_number = self.num_entries[free_slot_column]
            self.items[free_slot_column][row_number] = player
            column_points = self.num_new_points(free_slot_column, row_number,
                                                player)
            available_moves.append([free_slot_column, column_points])
            self.items[free_slot_column][row_number] = 0

        for points_index in range(len(available_moves) - 1, -1, -1):
            if available_moves[points_index][1] >= max_points:
                max_points = available_moves[points_index][1]
                slot_number_for_max_points = available_moves[points_index]
        return tuple(slot_number_for_max_points)


class FourInARow:
    def __init__(self, size):
        self.board = GameBoard(size)
        self.size = size

    def play(self):
        frame_size = 100
        width = frame_size * self.size
        height = frame_size * (self.size + 1)
        area = (width, height)
        screen = pygame.display.set_mode(area)

        print("*****************NEW GAME*****************")
        self.board.display(screen)
        pygame.display.update()
        player_number = 0
        print()
        while not self.board.game_over():
            for action in pygame.event.get():
                if action.type == pygame.QUIT:
                    sys.exit()
                if action.type == pygame.MOUSEBUTTONDOWN:
                    print()
                    '''print("Player ", player_number + 1, ": ")
                    if player_number == 0:
                        valid_input = False
                        while not valid_input:
                            try:
                                column = int(input("Please input slot: "))
                            except ValueError:
                                print("Input must be an integer in the range 0 to ",
                                      self.board.size)
                            else:
                                if column < 0 or column >= self.board.size:
                                    print("Input must be an integer in the range 0 to ",
                                          self.board.size)
                                else:
                                    if self.board.add(column, player_number + 1):
                                        valid_input = True
                                    else:
                                        print("Column ", column,
                                              "is alrady full. Please choose another one.")
                    else:
                        # Choose move which maximises new points for computer player
                        (best_column,
                         max_points) = self.board.column_resulting_in_max_points(2)
                        if max_points > 0:
                            column = best_column
                        else:
                            # if no move adds new points choose move which minimises
                            # points opponent player gets
                            (best_column,
                             max_points) = self.board.column_resulting_in_max_points(1)
                            if max_points > 0:
                                column = best_column
                            else:
                                # if no opponent move creates new points then choose
                                # column as close to middle as possible
                                column = \
                                    self.board.free_slots_as_close_to_middle_as_possible()[
                                        0]
                        self.board.add(column, player_number + 1)
                        print("The AI chooses column ", column)
                    self.board.display(screen)
                    pygame.display.update()
                    player_number = (player_number + 1) % 2
                if self.board.points[0] > self.board.points[1]:
                    print("Player 1 (circles) wins!")
                elif self.board.points[0] < self.board.points[1]:
                    print("Player 2 (crosses) wins!")
                else:
                    print("It's a draw!")'''


pygame.init()
game = FourInARow(6)
game.play()