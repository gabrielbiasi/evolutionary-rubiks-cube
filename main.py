#!/usr/bin/python
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

GENERATIONS = 100   # Máximo de gerações
LAMBDA = 50000      # Tamanho da população
THETA = 1000        # Necessário para troca de fase

#--------------------------------------------------------------#

import re, sys, random
from timeit import default_timer as timer

from individual import Individual
from cube import Cube

PHASE_COUNTER = 0
file_info = None
best = None
t1 = 0.0
t2 = 0.0

def to_file(best):
    '''
    Joga para um arquivo de saída o melhor conjunto
    de movimentos encontrados pelo algoritmo e exibe
    o tempo de execução.
    '''
    t2 = timer()
    best_file = open("best/best{}.txt".format(sys.argv[2]), "w")
    for gene in best.genes:
        best_file.write(gene + ' ')
    best_file.close()
    file_info.close()
    print '\nTIME ELAPSED %dm %ds' % ((t2-t1)/60, (t2-t1)%60)
    exit()


def generate_population(size, cube):
    '''
    Cria a população vazia de (size) indivíduos
    e aplica a primeira mutação.
    '''
    population = list()
    for i in range(size):
        ind = Individual(cube)
        ind.mutation(0)
        population.append(ind)

    return population


def evolution(cube):
    '''
    Algoritmo principal do trabalho.
    Gera a população e gerencia o fluxo
    das gerações.
    '''
    global best, t1, PHASE_COUNTER
    random.seed(timer())

    t1 = timer() # Timer inicia neste ponto
    population = generate_population(LAMBDA, cube)

    # Controle geral das gerações
    generation = 0
    try:
        while generation <= GENERATIONS:

            # Cálculo do fitness e fase de seleção
            population.sort(key=lambda x: x.get_fitness(PHASE_COUNTER))
            candidates = list(population[:THETA])
            best = candidates[0]
            #print '\n', best


            # Condição de parada final.
            if PHASE_COUNTER == 5 and best.get_fitness(PHASE_COUNTER) == best.size:
                    print 'FOUND! %d MOVES!' % best.size,
                    to_file(best)


            # Contagem de cubos resolvidos da fase
            # atual para provável troca de fase.
            solved_count = 0
            solved_phase = True
            for ind in candidates:
                if ind.get_fitness(PHASE_COUNTER) > ind.size:
                    solved_phase = False
                    break
                else:
                    solved_count += 1

            #--------------------------------------------------------------
            #--------------------- OBTENÇÃO DE DADOS ----------------------
            #--------------------------------------------------------------
            
            # Fitness Média
            '''
            soma1 = 0.0
            soma2 = 0.0
            for ind in population:
                s = len(ind.genes)
                soma1 += s
                soma2 += ind.get_fitness(PHASE_COUNTER) - s
            tam_media = soma1 / float(LAMBDA)
            fit_media = soma2 / float(LAMBDA)
            tup = (generation, fit_media, tam_media, solved_count, PHASE_COUNTER)

            file_info.write('%d %d %d %d\n' % tup)'''    

            # Tempo de Execução de cada geração
            t_now = timer()
            m = (t_now-t1) / 60
            s = (t_now-t1) % 60
            sys.stdout.write('G %d (%dm %ds)\tPhase: %d/5\tSolved.: %d/%d\n' % (generation, m, s, PHASE_COUNTER, solved_count, THETA))
            sys.stdout.flush()
            #--------------------------------------------------------------
            #--------------------------------------------------------------
            #--------------------------------------------------------------

            # Mudança de fase!
            if solved_phase:
                PHASE_COUNTER += 1

            # Criação da nova população para a próxima geração,
            # duplicando os candidatos da geração anterior.
            i = 0
            new_size = THETA
            while new_size < LAMBDA:
                ind = random.choice(candidates)
                new_ind = Individual(ind)
                candidates.append(new_ind)
                new_size += 1

            # Todos os indivíduos da nova população
            # sofrem mutação.
            for ind in candidates:
                ind.mutation(PHASE_COUNTER)

            # Fim de uma geração.
            population = candidates
            generation += 1

    except KeyboardInterrupt:
        to_file(best)
    except Exception as e:
        print e

    # Fim das Gerações
    to_file(best)

if __name__ == '__main__':

    # Condição de teste dos argumentos de entrada
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print 'args failed'
        exit()

    # Criação do objeto Cube
    cube = None
    with open(sys.argv[1], 'r') as file:

        # Neste trabalho, apenas os cubos de
        # 3 dimensões são aceitos.
        dimensions = int(file.readline())
        if dimensions != 3:
            print 'FAILED\nOnly 3 dimensions cubes are accepted.'
            exit()

        # A estrutura abaixo permite que o arquivo de entrada
        # tenha a ordem das faces livremente, pois o código se
        # adapta à ordem de faces do arquivo.
        pos = 0
        active = -1
        cube = Cube()
        for line in file:
            if line == 'Front\n':
                active = 0
            elif line == 'Left\n':
                active = 1
            elif line == 'Right\n':
                active = 2
            elif line == 'Back\n':
                active = 3
            elif line == 'Up\n':
                active = 4
            elif line == 'Down\n':
                active = 5
            else:
                for i in range(3):
                    cube.set_color(active, pos, i, line[i*2])
                pos += 1
                continue
            pos = 0

    if len(sys.argv) == 4:
        '''
        Se um terceiro argumento é passado por parâmetro de entrada,
        ele é considerado um indivíduo e então é exibido o cubo de
        entrada com os movimentos do arquivo.
        '''
        print 'TEST'
        with open(sys.argv[3], 'r') as file:
            data = file.readline()
            genes = [str(x) for x in re.findall('(\S\S*)', data)]

            print '%d MOVES' % len(genes)
            my_move = Individual(cube)
            my_move.apply(genes)
            my_move.cube.colored_printf()
            print genes
    else:
        '''
        Condição normal do algoritmo, a função
        (evolution) é chamada e o fluxo de gerações
        se inicia.
        '''
        print 'EVOLUTION'
        file_info = open('data/data{}.txt'.format(sys.argv[2]), 'w')
        file_info.write('-1 %d %d\n' % (THETA, LAMBDA))
        best = Individual(cube)
        evolution(cube)
