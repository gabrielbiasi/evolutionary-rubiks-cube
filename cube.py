# -*- coding: utf-8 -*-
"""
Universidade Federal de Minas Gerais
Departamento de Ciência da Computação
Programa de Pós-Graduação em Ciência da Computação

Computação Natural
Trabalho Prático 1

Feito por Gabriel de Biasi, 2016672212.
"""

class Cube(object):

    def __init__(self):
        #-#-# Inicialização da Matrix de Representação #-#-#
        self.matrix = list()
        for i in range(6):
            self.matrix.append(list())
            for j in range(3):
                self.matrix[i].append(list())
                for k in range(3):
                    self.matrix[i][j].append(list())
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


    def set_color(self, x, y, z, color):
        try:
            self.matrix[x][y][z] = color
        except:
            print '[ERROR]\nWrong enconding file, use Unix terminators.'
            exit()


    def printf(self):
        print '3\nFront'
        for line in self.matrix[0]:
            for color in line:
                print color,
            print
        print 'Left'
        for line in self.matrix[1]:
            for color in line:
                print color,
            print
        print 'Right'
        for line in self.matrix[2]:
            for color in line:
                print color,
            print
        print 'Back'
        for line in self.matrix[3]:
            for color in line:
                print color,
            print
        print 'Up'
        for line in self.matrix[4]:
            for color in line:
                print color,
            print
        print 'Down'
        for line in self.matrix[5]:
            for color in line:
                print color,
            print

    def colored_printf(self):
        color_dic = {'W':'\033[1;0m','R':'\033[1;31m',
        'G':'\033[1;32m','O':'\033[0;33m','B':'\033[1;34m',
        'Y':'\033[1;33m'}

        for line in self.matrix[4]:
            for i in range(2):
                print '\t',

            for color in line:
                print color_dic[color],
                print color,
            print
        print color_dic['W']
        for i in range(3):
            for j in [1, 0, 2, 3]:
                for color in self.matrix[j][i]:
                    print color_dic[color],
                    print color,
                print '\t',
            print
        print color_dic['W']
        for line in self.matrix[5]:
            for i in range(2):
                print '\t',
            for color in line:
                print color_dic[color],
                print color,
            print

        print color_dic['W']

    def move_f(self, mode):
        U4, R2, D5, L1 = list(), list(), list(), list()
        for i in range(3):
            U4.append(self.matrix[4][2][i])
            R2.append(self.matrix[2][i][0])
            D5.append(self.matrix[5][0][i])
            L1.append(self.matrix[1][i][2])

        # Horário
        if mode == 0:
            self.clockwise_rotation(0)
            for i in range(3):
                self.matrix[4][2][i] = L1[2-i]  # Left  -> Up
                self.matrix[2][i][0] = U4[i]    # Up    -> Right
                self.matrix[5][0][i] = R2[2-i]  # Right -> Down
                self.matrix[1][i][2] = D5[i]    # Down  -> Left

        # Anti-Horário
        elif mode == 1:
            self.anti_clockwise_rotation(0)
            for i in range(3):
                self.matrix[4][2][i] = R2[i]    # Right -> Up
                self.matrix[2][i][0] = D5[2-i]  # Down  -> Right
                self.matrix[5][0][i] = L1[i]    # Left  -> Down 
                self.matrix[1][i][2] = U4[2-i]  # Up    -> Left

        # 180
        else:
            self.double_rotation(0)
            for i in range(3):
                self.matrix[4][2][i] = D5[2-i]  # Down  -> Up
                self.matrix[2][i][0] = L1[2-i]  # Left  -> Right
                self.matrix[5][0][i] = U4[2-i]  # Up    -> Down 
                self.matrix[1][i][2] = R2[2-i]  # Right -> Left



    def move_r(self, mode):
        F0, U4, B3, D5 = list(), list(), list(), list()

        for i in range(3):
            F0.append(self.matrix[0][i][2])
            U4.append(self.matrix[4][i][2])
            B3.append(self.matrix[3][i][0])
            D5.append(self.matrix[5][i][2])

        # Horário
        if mode == 0:
            self.clockwise_rotation(2)
            for i in range(3):
                self.matrix[0][i][2] = D5[i]    # Down  -> Front
                self.matrix[4][i][2] = F0[i]    # Front -> Up
                self.matrix[3][i][0] = U4[2-i]  # Up    -> Back
                self.matrix[5][i][2] = B3[2-i]  # Back  -> Front

        # Anti-Horário
        elif mode == 1:
            self.anti_clockwise_rotation(2)
            for i in range(3):
                self.matrix[0][i][2] = U4[i]    # Up    -> Front
                self.matrix[4][i][2] = B3[2-i]  # Back  -> Up
                self.matrix[3][i][0] = D5[2-i]  # Down  -> Back
                self.matrix[5][i][2] = F0[i]    # Front -> Down

        # 180
        else:
            self.double_rotation(2)
            for i in range(3):
                self.matrix[0][i][2] = B3[2-i]  # Back  -> Front
                self.matrix[4][i][2] = D5[i]    # Down  -> Up
                self.matrix[3][i][0] = F0[2-i]  # Front -> Back
                self.matrix[5][i][2] = U4[i]    # Up    -> Down


    def move_u(self, mode):
        F0, R2, B3, L1 = list(), list(), list(), list()

        for i in range(3):
            F0.append(self.matrix[0][0][i])
            R2.append(self.matrix[2][0][i])
            B3.append(self.matrix[3][0][i])
            L1.append(self.matrix[1][0][i])

        # Horário
        if mode == 0:
            self.clockwise_rotation(4)
            for i in range(3):
                self.matrix[0][0][i] = R2[i]    # Right -> Front
                self.matrix[2][0][i] = B3[i]    # Back  -> Right
                self.matrix[3][0][i] = L1[i]    # Left  -> Back
                self.matrix[1][0][i] = F0[i]    # Front -> Left


        # Anti-Horário
        elif mode == 1:
            self.anti_clockwise_rotation(4)
            for i in range(3):
                self.matrix[0][0][i] = L1[i]    # Left  -> Front
                self.matrix[2][0][i] = F0[i]    # Front -> Right
                self.matrix[3][0][i] = R2[i]    # Right -> Back
                self.matrix[1][0][i] = B3[i]    # Back  -> Left

        # 180
        else:
            self.double_rotation(4)
            for i in range(3):
                self.matrix[0][0][i] = B3[i]    # Back  -> Front
                self.matrix[2][0][i] = L1[i]    # Left  -> Right
                self.matrix[3][0][i] = F0[i]    # Front -> Back
                self.matrix[1][0][i] = R2[i]    # Right -> Left


    def move_b(self, mode):
        U4, R2, D5, L1 = list(), list(), list(), list()
        for i in range(3):
            U4.append(self.matrix[4][0][i])
            R2.append(self.matrix[2][i][2])
            D5.append(self.matrix[5][2][i])
            L1.append(self.matrix[1][i][0])

        # Horário
        if mode == 0:
            self.clockwise_rotation(3)
            for i in range(3):
                self.matrix[4][0][i] = R2[i]    # Right -> Up
                self.matrix[2][i][2] = D5[2-i]  # Down  -> Right
                self.matrix[5][2][i] = L1[i]    # Left  -> Down 
                self.matrix[1][i][0] = U4[2-i]  # Up    -> Left

        # Anti-Horário
        elif mode == 1:
            self.anti_clockwise_rotation(3)
            for i in range(3):
                self.matrix[4][0][i] = L1[2-i]  # Left  -> Up
                self.matrix[2][i][2] = U4[i]    # Up    -> Right
                self.matrix[5][2][i] = R2[2-i]  # Right -> Down
                self.matrix[1][i][0] = D5[i]    # Down  -> Left

        # 180
        else:
            self.double_rotation(3)
            for i in range(3):
                self.matrix[4][0][i] = D5[2-i]  # Down  -> Up
                self.matrix[2][i][2] = L1[2-i]  # Left  -> Right
                self.matrix[5][2][i] = U4[2-i]  # Up    -> Down 
                self.matrix[1][i][0] = R2[2-i]  # Right -> Left


    def move_l(self, mode):
        F0, U4, B3, D5 = list(), list(), list(), list()

        for i in range(3):
            F0.append(self.matrix[0][i][0])
            U4.append(self.matrix[4][i][0])
            B3.append(self.matrix[3][i][2])
            D5.append(self.matrix[5][i][0])

        # Horário
        if mode == 0:
            self.clockwise_rotation(1)
            for i in range(3):
                self.matrix[0][i][0] = U4[i]    # Up    -> Front
                self.matrix[4][i][0] = B3[2-i]  # Back  -> Up
                self.matrix[3][i][2] = D5[2-i]  # Down  -> Back
                self.matrix[5][i][0] = F0[i]    # Front -> Down


        # Anti-Horário
        elif mode == 1:
            self.anti_clockwise_rotation(1)
            for i in range(3):
                self.matrix[0][i][0] = D5[i]    # Down  -> Front
                self.matrix[4][i][0] = F0[i]    # Front -> Up
                self.matrix[3][i][2] = U4[2-i]  # Up    -> Back
                self.matrix[5][i][0] = B3[2-i]  # Back  -> Front

        # 180
        else:
            self.double_rotation(1)
            for i in range(3):
                self.matrix[0][i][0] = B3[2-i]  # Back  -> Front
                self.matrix[4][i][0] = D5[i]    # Down  -> Up
                self.matrix[3][i][2] = F0[2-i]  # Front -> Back
                self.matrix[5][i][0] = U4[i]    # Up    -> Down


    def move_d(self, mode):
        F0, R2, B3, L1 = list(), list(), list(), list()

        for i in range(3):
            F0.append(self.matrix[0][2][i])
            R2.append(self.matrix[2][2][i])
            B3.append(self.matrix[3][2][i])
            L1.append(self.matrix[1][2][i])

        # Horário
        if mode == 0:
            self.clockwise_rotation(5)
            for i in range(3):
                self.matrix[0][2][i] = L1[i]    # Left  -> Front
                self.matrix[2][2][i] = F0[i]    # Front -> Right
                self.matrix[3][2][i] = R2[i]    # Right -> Back
                self.matrix[1][2][i] = B3[i]    # Back  -> Left


        # Anti-Horário
        elif mode == 1:
            self.anti_clockwise_rotation(5)
            for i in range(3):
                self.matrix[0][2][i] = R2[i]    # Right -> Front
                self.matrix[2][2][i] = B3[i]    # Back  -> Right
                self.matrix[3][2][i] = L1[i]    # Left  -> Back
                self.matrix[1][2][i] = F0[i]    # Front -> Left


        # 180
        else:
            self.double_rotation(5)
            for i in range(3):
                self.matrix[0][2][i] = B3[i]    # Back  -> Front
                self.matrix[2][2][i] = L1[i]    # Left  -> Right
                self.matrix[3][2][i] = F0[i]    # Front -> Back
                self.matrix[1][2][i] = R2[i]    # Right -> Left


    def clockwise_rotation(self, pos):
        new_matrix = list()
        for i in range(3):
            new_matrix.append(list())
        for i in range(3):
            for j in range(3):
                new_matrix[j].insert(0, self.matrix[pos][i][j])
        self.matrix[pos] = new_matrix


    def anti_clockwise_rotation(self, pos):
        new_matrix = list()
        for i in range(3):
            new_matrix.append(list())
        for i in range(3):
            for j in range(3):
                new_matrix[j].append(self.matrix[pos][i][2-j])
        self.matrix[pos] = new_matrix


    def double_rotation(self, pos):
        new_matrix = list()
        for i in range(3):
            new_matrix.append(list())
        for i in range(3):
            for j in range(3):
                new_matrix[2-i].append(self.matrix[pos][i][2-j])
        self.matrix[pos] = new_matrix


    def is_finished(self):
        colors = list()
        for face in self.matrix:
            active = face[0][0]
            # Cor já foi verificada
            if active in colors:
                return False
            else:
            # Cor da face é selecionada
                colors.append(active)
                for line in face:
                    for color in line:
                        # Cor diferente da cor "ativa"
                        if color != active:
                            return False
        return True
