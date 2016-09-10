# -*- coding: utf-8 -*-
"""
Universidade Federal de Minas Gerais
Departamento de Ciência da Computação
Programa de Pós-Graduação em Ciência da Computação

Computação Natural
Trabalho Prático 1

Feito por Gabriel de Biasi, 2016672212.
"""

#--------------------------------------------------------------#
#------------------------ CONSTANTES --------------------------#
#--------------------------------------------------------------#
#-#-# Pressão seletiva de cada fase #-#-#
CONST_PHASE_0 = 10
CONST_PHASE_1 = 10
CONST_PHASE_2 = 50
CONST_PHASE_3 = 10
CONST_PHASE_4 = 50
CONST_PHASE_5 = 10

# G0, G1.1, G1.2, G2.1, G2.2, G3
PHASE_START = [0,  1,  1,  2,  2,  4]
PHASE_END   = [7, 13, 13, 15, 15, 17]

MOVES_SET = [                                #-#-#-#-
    ['L',  'R',  'F',  'B',  'U',  'D' ],    # G0   #
    ['L2', 'R2', 'F',  'B',  'U',  'D' ],    # G1.1 #
    ['L2', 'R2', 'F',  'B',  'U',  'D' ],    # G1.2 #
    ['L2', 'R2', 'F2', 'B2', 'U',  'D' ],    # G2.1 #
    ['L2', 'R2', 'F2', 'B2', 'U',  'D' ],    # G2.2 #
    ['F2', 'R2', 'F2', 'B2', 'U2', 'D2']     # G3   #
]                                            #-#-#-#-
#--------------------------------------------------------------#

import copy, random
from cube import Cube

class Color():
    '''
    Importante!
    Esta classe se comporta como um 'Enum' à fim
    de facilitar a troca de cores de referência
    caso o arquivo de entrada esteja invertido
    de alguma forma.
    '''
    TOP = 'Y'
    BOTTOM = 'W'
    FRONT = 'O'
    BACK = 'R'
    LEFT = 'G'
    RIGHT = 'B'


class Individual(object):

    def __init__(self, ind):
        '''
        Construtor do Indivíduo
        Se o parâmetro passado for um indivíduo, é
        feita então uma cópia.
        '''
        if isinstance(ind, Individual):
            self.cube = copy.deepcopy(ind.cube)
            self.genes = list(ind.genes)
            self.fitness = ind.fitness
            self.phase = ind.phase
            self.size = ind.size

        else:
            self.cube = copy.deepcopy(ind)
            self.genes = list()
            self.fitness = -1
            self.phase = 0
            self.size = 0


    def __repr__(self):
        return self.__str__()


    def __str__(self):
        '''
        Representação gráfica do indivíduo.
        '''
        self.cube.colored_printf()
        return "{}[PH{}][L{}][F{}]".format(self.phase, self.genes, self.size, self.fitness)


    def mutation(self, phase):
        '''
        Este método cria uma nova jogada à ser aplicada no cubo
        mágico, de acordo com a fase atual do algoritmo, temos
        movimentos específicos e quantidade limitada, pelas listas
        PHASE_START, PHASE_END e MOVES_SET. Após a criação a os
        movimentos são "limpos" e acrescentados ao indivíduo.
        '''
        # Atualiza a fase e reseta o fitness
        self.phase = phase
        self.fitness = -1

        # Geração aleatória de uma jogada
        new_genes = list()
        size = random.randint(PHASE_START[self.phase], PHASE_END[self.phase])
        for i in range(size):
            new_genes.append(random.choice(MOVES_SET[self.phase]))

        # A jogada é aplicada ao cubo
        self.apply(new_genes)

        #-# WORKAROUND #-#
        # A junção do último movimento já feito com o novo primeiro movimento
        # pode ser um possível candidato à limpeza. O último movimento é retirado
        # do indivídio e ele "participa" da limpeza.
        if self.size > 0:
            self.size -= 1
            last_move = self.genes.pop()
            new_genes.insert(0, last_move)

        # Limpeza de movimentos
        new_genes = self.clean(new_genes)
        self.size += len(new_genes)
        self.genes += new_genes


    def get_fitness(self, phase):
        '''
        Cálculo da fitness
        Recebe por parâmetro a fase atual do
        algoritmo para realizar o cálculo corretamente.
        '''
        self.phase = phase
        c = self.size

        if self.fitness == -1:
            result = 0
            if self.phase == 0:
                '''
                Cálculo da fitness G0 -> G1
                Os meios precisam ser orientados da maneira correta,
                ou seja, é possível colocá-los em seus lugares sem uso
                dos movimentos L e R.
                '''
                w = 0

                #-#-# Mapeamento de todos os meios do cubo #-#-#
                # Deu trabalho :(
                edge_pieces = [
                    (self.cube.matrix[0][1][0], self.cube.matrix[1][1][2]), # O->G
                    (self.cube.matrix[0][1][2], self.cube.matrix[2][1][0]), # O->B
                    (self.cube.matrix[0][0][1], self.cube.matrix[4][2][1]), # O->Y
                    (self.cube.matrix[0][2][1], self.cube.matrix[5][0][1]), # O->W

                    (self.cube.matrix[3][1][0], self.cube.matrix[2][1][2]), # R->B
                    (self.cube.matrix[3][1][2], self.cube.matrix[1][1][0]), # R->G
                    (self.cube.matrix[3][0][1], self.cube.matrix[4][0][1]), # R->Y
                    (self.cube.matrix[3][2][1], self.cube.matrix[5][2][1]), # R->W

                    (self.cube.matrix[1][0][1], self.cube.matrix[4][1][0]), # G->Y
                    (self.cube.matrix[1][2][1], self.cube.matrix[5][1][0]), # G->W

                    (self.cube.matrix[2][0][1], self.cube.matrix[4][1][2]), # B->Y
                    (self.cube.matrix[2][2][1], self.cube.matrix[5][1][2])  # B->W
                ]

                # A cada meio não-orientado, 1 ponto de punição.
                for piece in edge_pieces:
                    if piece[0] in [Color.TOP, Color.BOTTOM]:
                        w += 1
                    elif piece[0] in [Color.LEFT, Color.RIGHT] and \
                    piece[1] in [Color.FRONT, Color.BACK]:
                        w += 1

                # Parâmetros de multiplicação
                # Aumenta ou diminui a pressão seletiva da fase.
                result = (CONST_PHASE_0 * w) + c

            elif self.phase == 1:
                '''
                Cálculo da fitness G1 -> G2 (Parte 1)
                Nesta parte 1, é colocado os meios na camada do meio
                apenas. Este processo facilita a convergência para o
                real cálculo da fitness G1->G2 na parte 2.
                '''
                w = 0
                #-#-# Punição por meios fora da camada do meio. #-#-#
                f = self.cube.matrix[0][1] # Face da frente, camada do meio.
                w += 0 if f[0] == Color.FRONT or f[0] == Color.BACK else 1
                w += 0 if f[2] == Color.FRONT or f[2] == Color.BACK else 1

                f = self.cube.matrix[3][1] # Face de trás, camada do meio.
                w += 0 if f[0] == Color.FRONT or f[0] == Color.BACK else 1
                w += 0 if f[2] == Color.FRONT or f[2] == Color.BACK else 1

                f = self.cube.matrix[1][1] # Face da esquerda, camada do meio.
                w += 0 if f[0] == Color.LEFT or f[0] == Color.RIGHT else 1
                w += 0 if f[2] == Color.LEFT or f[2] == Color.RIGHT else 1

                f = self.cube.matrix[2][1] # Face da direita, camada do meio.
                w += 0 if f[0] == Color.LEFT or f[0] == Color.RIGHT else 1
                w += 0 if f[2] == Color.LEFT or f[2] == Color.RIGHT else 1

                # Parâmetros de multiplicação
                # Aumenta ou diminui a pressão seletiva da fase.
                result = (CONST_PHASE_1 * w) + c

            elif self.phase == 2:
                '''
                Cálculo da fitness G1 -> G2 (Parte 2)
                Todos as cores FRONT e BACK precisam estar
                nas faces FRONT e BACK.
                '''
                # Mesmo código da fase 1 #
                w = 0
                #-#-# Punição por meios fora da camada do meio. #-#-#
                f = self.cube.matrix[0][1] # Face da frente, camada do meio.
                w += 0 if f[0] == Color.FRONT or f[0] == Color.BACK else 1
                w += 0 if f[2] == Color.FRONT or f[2] == Color.BACK else 1

                f = self.cube.matrix[3][1] # Face de trás, camada do meio.
                w += 0 if f[0] == Color.FRONT or f[0] == Color.BACK else 1
                w += 0 if f[2] == Color.FRONT or f[2] == Color.BACK else 1

                f = self.cube.matrix[1][1] # Face da esquerda, camada do meio.
                w += 0 if f[0] == Color.LEFT or f[0] == Color.RIGHT else 1
                w += 0 if f[2] == Color.LEFT or f[2] == Color.RIGHT else 1

                f = self.cube.matrix[2][1] # Face da direita, camada do meio.
                w += 0 if f[0] == Color.LEFT or f[0] == Color.RIGHT else 1
                w += 0 if f[2] == Color.LEFT or f[2] == Color.RIGHT else 1

                result = (CONST_PHASE_1 * w) + c
                # Fim do mesmo código da fase 1 #

                v = 0
                #-#-# Punição para cada canto não orientado. #-#-#
                f = self.cube.matrix[4] # Face de cima
                v += 0 if f[0][0] == Color.TOP or f[0][0] == Color.BOTTOM else 1
                v += 0 if f[0][2] == Color.TOP or f[0][2] == Color.BOTTOM else 1
                v += 0 if f[2][0] == Color.TOP or f[2][0] == Color.BOTTOM else 1
                v += 0 if f[2][2] == Color.TOP or f[2][2] == Color.BOTTOM else 1


                f = self.cube.matrix[5] # Face de baixo
                v += 0 if f[0][0] == Color.TOP or f[0][0] == Color.BOTTOM else 1
                v += 0 if f[0][2] == Color.TOP or f[0][2] == Color.BOTTOM else 1
                v += 0 if f[2][0] == Color.TOP or f[2][0] == Color.BOTTOM else 1
                v += 0 if f[2][2] == Color.TOP or f[2][2] == Color.BOTTOM else 1

                # Parâmetros de multiplicação
                # Aumenta ou diminui a pressão seletiva da fase.
                result = (CONST_PHASE_2 * v) + result

            elif self.phase == 3:
                '''
                Cálculo da fitness G2 -> G3 (Parte 1)
                Todos as faces precisam ter sua cor original ou sua cor oposta,
                além dos cantos vizinhos precisam compartilhar a mesma cor "lateral",
                não importando o topo/baixo.
                '''
                y = 0
                #-#-# Mapeamento de todos os cantos do cubo #-#-#
                # Também deu trabalho :(
                all_corners = [
                    (self.cube.matrix[0][0][0], self.cube.matrix[1][0][2]), #Y-O-G
                    (self.cube.matrix[0][2][0], self.cube.matrix[1][2][2]), #W-O-G

                    (self.cube.matrix[0][0][2], self.cube.matrix[2][0][0]), #Y-O-B
                    (self.cube.matrix[0][2][2], self.cube.matrix[2][2][0]), #W-O-B

                    (self.cube.matrix[3][0][0], self.cube.matrix[2][0][2]), #Y-R-B
                    (self.cube.matrix[3][2][0], self.cube.matrix[2][2][2]), #W-R-B

                    (self.cube.matrix[3][0][2], self.cube.matrix[1][0][0]), #Y-R-G
                    (self.cube.matrix[3][2][2], self.cube.matrix[1][2][0]), #W-R-G
                ]

                #-#-# Punição para cada canto da camada superior que não combina
                # sua cor com o canto da camada inferior (formando uma "coluna"). #-#-#
                for i in range(0, 8, 2):
                    if all_corners[i][0] != all_corners[i+1][0] or \
                    all_corners[i][1] != all_corners[i+1][1]:
                        y += 1

                # Parâmetros de multiplicação
                # Aumenta ou diminui a pressão seletiva da fase.
                result = (CONST_PHASE_3 * y) + c

            elif self.phase == 4:
                x, y = 0, 0
                # Mesmo código da fase 3 #
                #-#-# Mapeamento de todos os cantos do cubo #-#-#
                # Também deu trabalho :(
                all_corners = [
                    (self.cube.matrix[0][0][0], self.cube.matrix[1][0][2]), #Y-O-G
                    (self.cube.matrix[0][2][0], self.cube.matrix[1][2][2]), #W-O-G

                    (self.cube.matrix[0][0][2], self.cube.matrix[2][0][0]), #Y-O-B
                    (self.cube.matrix[0][2][2], self.cube.matrix[2][2][0]), #W-O-B

                    (self.cube.matrix[3][0][0], self.cube.matrix[2][0][2]), #Y-R-B
                    (self.cube.matrix[3][2][0], self.cube.matrix[2][2][2]), #W-R-B

                    (self.cube.matrix[3][0][2], self.cube.matrix[1][0][0]), #Y-R-G
                    (self.cube.matrix[3][2][2], self.cube.matrix[1][2][0]), #W-R-G
                ]

                #-#-# Punição para cada canto da camada superior que não combina
                # sua cor com o canto da camada inferior (formando uma "coluna"). #-#-#
                for i in range(0, 8, 2):
                    if all_corners[i][0] != all_corners[i+1][0] or \
                    all_corners[i][1] != all_corners[i+1][1]:
                        y += 1

                result = (CONST_PHASE_3 * y) + c

                # Fim do mesmo código da fase 3 #

                #-#-# Recebe uma punição cada cor de cubo que não é a
                # cor da correta ou não é a cor oposta da face. #-#-#
                OP = {'O':'R','R':'O','W':'Y','Y':'W','G':'B','B':'G'}
                for face in self.cube.matrix:
                    center = face[1][1]
                    for i in range(3):
                        for j in range(3):
                            if face[i][j] != center and face[i][j] != OP[center]:
                                x += 1

                # Parâmetros de multiplicação
                # Aumenta ou diminui a pressão seletiva da fase.
                result = (CONST_PHASE_4 * x) + result

            elif self.phase == 5:
                '''
                Cálculo da fitness G3 -> G4 (Resolvido)
                Agora apenas movimentos de 180 graus são permitidos, a função
                de fitness simplesmente olha a cor de cada cubo e verifica com
                o centro.
                '''
                z = 0
                #-#-# Fase final, recebe uma punição por cada cor
                # que não é a cor da face atual. #-#-#
                for face in self.cube.matrix:
                    center = face[1][1]
                    for i in range(3):
                        for j in range(3):
                            if face[i][j] != center:
                                z += 1

                # Parâmetros de multiplicação
                # Aumenta ou diminui a pressão seletiva da fase.
                result = (CONST_PHASE_5 * z) + c

            self.fitness = result

        return self.fitness


    def apply(self, new_moves):
        '''
        Este método aplica os novos movimentos gerados
        pela mutação para o cubo que pertence à este
        indivíduo.
        '''
        for gene in new_moves:
            mode = 0 # Movimento Horário
            if len(gene) == 2:
                mode = 1 if gene[1] == 'i' else 2 # Movimento anti-horário ou 180
            if gene[0] == 'F':
                self.cube.move_f(mode)
            elif gene[0] == 'R':
                self.cube.move_r(mode)
            elif gene[0] == 'U':
                self.cube.move_u(mode)
            elif gene[0] == 'B':
                self.cube.move_b(mode)
            elif gene[0] == 'L':
                self.cube.move_l(mode)
            elif gene[0] == 'D':
                self.cube.move_d(mode)
            else:
                print 'RADIATION DETECTED'
                exit()


    def clean(self, moves_list):
        '''
        Este método recebe os novos movimentos
        obtidos pela mutação  e realiza uma limpeza
        em busca de movimentos complementares ou
        movimentos que não geram efeito final no cubo.
        '''
        INVERSE = {'F': 'Fi','L': 'Li','R': 'Ri','B': 'Bi','U': 'Ui','D': 'Di','Fi': 'F','Li': 'L',
        'Ri': 'R','Bi': 'B','Ui': 'U','Di': 'D','F2': 'F2','L2': 'L2','R2': 'R2','B2': 'B2','U2': 'U2',
        'D2': 'D2'}
        SIMPLE_180 = {'F F2': 'Fi','L L2': 'Li','R R2': 'Ri','B B2': 'Bi','U U2': 'Ui','D D2': 'Di',
        'F2 F': 'Fi','L2 L': 'Li','R2 R': 'Ri','B2 B': 'Bi','U2 U': 'Ui','D2 D': 'Di','Fi F2': 'F',
        'Li L2': 'L','Ri R2': 'R','Bi B2': 'B','Ui U2': 'U','Di D2': 'D','F2 Fi': 'F','L2 Li': 'L',
        'R2 Ri': 'R','B2 Bi': 'B','U2 Ui': 'U','D2 Di': 'D'}
        
        i = 0
        result = list(moves_list)
        while i < len(result)-1:
            x = result[i]
            y = result[i+1]

            #-#-# Genes inversos seguidos são removidos #-#-#
            if x == INVERSE[y]: 
                del result[i]
                del result[i]
                if i > 0:
                    i -= 1

            #-#-# Genes iguais seguidos são convertidos para um gene 180 #-#-#
            elif x == y:
                del result[i]
                result[i] = str(result[i][0]+'2')
                if i > 0:
                    i -= 1

            #-# Simplificação de um 90 e 180 para um 90 invertido #-#
            elif str(x+' '+y) in SIMPLE_180:
                del result[i]
                result[i] = SIMPLE_180[str(x+' '+y)]
                if i > 0:
                    i -= 1

            else:
                i += 1
        return result
