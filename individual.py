# -*- coding: utf-8 -*-
"""
Universidade Federal de Minas Gerais
Departamento de Ciência da Computação
Programa de Pós-Graduação em Ciência da Computação

Computação Natural
Trabalho Prático 1

Feito por Gabriel de Biasi, 2016672212.
"""
import math, copy, random
from cube import Cube

class Individual(object):

    def __init__(self, cube, genes=[]):
        self.genes = list(genes)
        self.cube = cube

        self.phase_start_length = [0,  1,  1,  2,  4]
        self.phase_end_length =   [7, 13, 13, 15, 17]
        self.fitness = [-1,-1,-1,-1,-1]
        self.phase = 0

        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
        self.g = [                                  #-#-#-#-
        ['L',  'R' , 'F' , 'B' , 'U' , 'D' ],       # G0   #
        ['L',  'R' , 'F' , 'B' , 'U2', 'D2'],       # G1   #
        ['L',  'R' , 'F' , 'B' , 'U2', 'D2'],       # G1.2 #
        ['L',  'R' , 'F2', 'B2', 'U2', 'D2'],       # G2   #
        ['L2', 'R2', 'F2', 'B2', 'U2', 'D2']]       # G3   #
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

        '''#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
        self.g = [                              #-#-#-#-
        ['F', 'R', 'U', 'B', 'L', 'D' ],        # G0   #
        ['F', 'U', 'B', 'D', 'R2', 'L2'],       # G1   #
        ['F', 'U', 'B', 'D', 'R2', 'L2'],       # G1.2 #
        ['U', 'D', 'R2', 'L2', 'F2', 'B2'],     # G2   #
        ['F2', 'R2', 'U2', 'B2', 'L2', 'D2']]   # G3   #
        #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-'''


    def __repr__(self):
        return self.__str__()


    def __str__(self):
        cube = self.get_cube(self.genes)
        cube.colored_printf()
        return "{}[L{}][F{}]".format(self.genes, len(self.genes), self.fitness)


    def mutation(self, phase):
        self.phase = phase

        # Reseta o fitness
        self.fitness[self.phase] = -1

        new_genes = list()
        size = random.randint(self.phase_start_length[self.phase], self.phase_end_length[self.phase])
        for i in range(size):
            new_genes.append(random.choice(self.g[self.phase]))

        self.genes += new_genes
        self.clean(self.genes)


    def get_fitness(self, phase):
        self.phase = phase
        c = len(self.genes)
        my_cube = self.get_cube(self.genes)

        if self.fitness[self.phase] == -1:
            result = 0
            if self.phase == 0:
                w = 0

                f = my_cube.matrix[0] # FRONT
                l = [f[0][1], f[2][1], f[1][0], f[1][2]]
                w += l.count('G')
                w += l.count('B')

                f = my_cube.matrix[1] # LEFT
                l = [f[0][1], f[2][1], f[1][0], f[1][2]]
                w += l.count('R')
                w += l.count('O')

                f = my_cube.matrix[2] # RIGHT
                l = [f[0][1], f[2][1], f[1][0], f[1][2]]
                w += l.count('R')
                w += l.count('O')

                f = my_cube.matrix[3] # BACK
                l = [f[0][1], f[2][1], f[1][0], f[1][2]]
                w += l.count('G')
                w += l.count('B')

                result = (5 * (2 * w)) + c

            elif self.phase == 1:
                w = 0
                f = my_cube.matrix[0]
                l = [f[1][0], f[1][2]]
                w += 2 - l.count('O')

                f = my_cube.matrix[1]
                l = [f[1][0], f[1][2]]
                w += 2 - l.count('G')

                f = my_cube.matrix[2]
                l = [f[1][0], f[1][2]]
                w += 2 - l.count('B')

                f = my_cube.matrix[3]
                l = [f[1][0], f[1][2]]
                w += 2 - l.count('R')

                result = (5 * (2 * w)) + c

            elif self.phase == 2:
                # same code of phase1 #
                w = 0
                f = my_cube.matrix[0]
                l = [f[1][0], f[1][2]]
                w += 2 - l.count('O')

                f = my_cube.matrix[1]
                l = [f[1][0], f[1][2]]
                w += 2 - l.count('G')

                f = my_cube.matrix[2]
                l = [f[1][0], f[1][2]]
                w += 2 - l.count('B')

                f = my_cube.matrix[3]
                l = [f[1][0], f[1][2]]
                w += 2 - l.count('R')

                result = (5 * (2 * w)) + c
                # end of the same code of phase1 #

                v = 0

                f = my_cube.matrix[1]
                l = [f[0][0], f[0][2], f[2][0], f[2][2]]
                v += 4 - l.count('G') - l.count('B')

                f = my_cube.matrix[2]
                l = [f[0][0], f[0][2], f[2][0], f[2][2]]
                v += 4 - l.count('G') - l.count('B')


                result = (10 * (4 * v)) + result

            elif self.phase == 3:
                x, y = 0, 0
                OP = {'O':'R','R':'O','W':'Y','Y':'W','G':'B','B':'G'}
                for face in my_cube.matrix:
                    center = face[1][1]
                    for i in range(3):
                        for j in range(3):
                            if face[i][j] != center and face[i][j] != OP[center]:
                                x += 1

                result = 5 * (x + (2 * y)) + c

            elif self.phase == 4:
                z = 0
                for face in my_cube.matrix:
                    center = face[1][1]
                    for i in range(3):
                        for j in range(3):
                            if face[i][j] != center:
                                z += 1

                result = (5 * z) + c

            self.fitness[self.phase] = result

        return self.fitness[self.phase]


    def get_cube(self, genes_list):
        my_cube = copy.deepcopy(self.cube)

        for gene in genes_list:
            mode = 0
            if len(gene) == 2:
                mode = 1 if gene[1] == 'i' else 2
            if gene[0] == 'F':
                my_cube.move_f(mode)
            elif gene[0] == 'R':
                my_cube.move_r(mode)
            elif gene[0] == 'U':
                my_cube.move_u(mode)
            elif gene[0] == 'B':
                my_cube.move_b(mode)
            elif gene[0] == 'L':
                my_cube.move_l(mode)
            elif gene[0] == 'D':
                my_cube.move_d(mode)
            else:
                print 'RADIATION DETECTED'
                exit()

        # Retorna apenas a cópia do cubo
        return my_cube


    def clean(self, moves_list):
        INVERSE = {'F': 'Fi','L': 'Li','R': 'Ri','B': 'Bi','U': 'Ui','D': 'Di','Fi': 'F','Li': 'L',
        'Ri': 'R','Bi': 'B','Ui': 'U','Di': 'D','F2': 'F2','L2': 'L2','R2': 'R2','B2': 'B2','U2': 'U2',
        'D2': 'D2'}
        SIMPLE_180 = {'F F2': 'Fi','L L2': 'Li','R R2': 'Ri','B B2': 'Bi','U U2': 'Ui','D D2': 'Di',
        'F2 F': 'Fi','L2 L': 'Li','R2 R': 'Ri','B2 B': 'Bi','U2 U': 'Ui','D2 D': 'Di','Fi F2': 'F',
        'Li L2': 'L','Ri R2': 'R','Bi B2': 'B','Ui U2': 'U','Di D2': 'D','F2 Fi': 'F','L2 Li': 'L',
        'R2 Ri': 'R','B2 Bi': 'B','U2 Ui': 'U','D2 Di': 'D'}
        
        i = 0
        while i < len(moves_list)-1:
            x, y = moves_list[i], moves_list[i+1]

            #-# Genes inversos seguidos são removidos #-#
            if x == INVERSE[y]: 
                del moves_list[i]
                del moves_list[i]
                if i > 0:
                    i -= 1

            #-# Genes iguais seguidos são convertidos para um gene 180 #-#
            elif x == y:
                del moves_list[i]
                moves_list[i] = str(moves_list[i][0]+'2')
                if i > 0:
                    i -= 1

            #-# Simplificação de um 90 e 180 para um 90 invertido #-#
            elif str(x+' '+y) in SIMPLE_180:
                del moves_list[i]
                moves_list[i] = SIMPLE_180[str(x+' '+y)]
                if i > 0:
                    i -= 1

            else:
                i += 1
