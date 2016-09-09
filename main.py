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
#--------------------------------------------------------------
#------------------------ CONSTANTES --------------------------
#--------------------------------------------------------------

GENERATIONS = 150 # Máximo de Gerações
LAMBDA = 50000 # População
THETA = 1000 # Troca de Fase

PHASE_COUNTER = 0
#--------------------------------------------------------------

import re, sys, random, copy
from timeit import default_timer as timer

from individual import Individual
from cube import Cube

file_info = None
best = None
t1 = 0.0
t2 = 0.0

def to_file(best):
    t2 = timer()
    best_file = open("best/best{}.txt".format(sys.argv[2]), "w")
    for gene in best.genes:
        best_file.write(gene + ' ')
    best_file.close()
    file_info.close()
    print '\nTIME ELAPSED %dm %ds' % ((t2-t1)/60, (t2-t1)%60)
    exit()


def generate_population(size, cube):
    population = list()
    # Cria a população e aplica a primeira mutação
    for i in range(size):
        ind = Individual(cube)
        ind.mutation(0)
        population.append(ind)

    return population


def evolution(cube):
    global best, t1, PHASE_COUNTER
    random.seed(timer())

    t1 = timer()
    population = generate_population(LAMBDA, cube)

    # Controle geral das gerações
    generation = 0
    try:
        while generation <= GENERATIONS:

            # Cálculo do Fitness e Fase de seleção
            population.sort(key=lambda x: x.get_fitness(PHASE_COUNTER))
            candidates = list(population[:THETA])
            best = candidates[0]
            print '\n',best

            # Cálculo de cubos resolvidos na fase atual
            solved_count = 0
            solved_phase = True
            for ind in candidates:
                if ind.get_fitness(PHASE_COUNTER) > len(ind.genes):
                    solved_phase = False
                    break
                else:
                    solved_count += 1

            # Condição de parada final
            if PHASE_COUNTER == 4:
                if best.get_fitness(PHASE_COUNTER) == len(best.genes):
                    print 'FOUND!',
                    to_file(best)

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

            # Tempo de Execução
            t_now = timer()
            m = (t_now-t1) / 60
            s = (t_now-t1) % 60
            sys.stdout.write('\rG %d (%dm %ds)\tPhase: %d/4\tSolved.: %d/%d\t\t' % (generation, m, s, PHASE_COUNTER, solved_count, THETA))
            sys.stdout.flush()
            #--------------------------------------------------------------
            #--------------------------------------------------------------
            #--------------------------------------------------------------

            # Mudança de fase!
            if solved_phase:
                PHASE_COUNTER += 1

            i = 0
            new_size = len(candidates)
            while new_size < LAMBDA:
                ind = random.choice(candidates)
                new_ind = Individual(cube, ind.genes)
                candidates.append(new_ind)
                new_size += 1

            for ind in candidates:
                ind.mutation(PHASE_COUNTER)

            # Fim de uma geração
            population = candidates
            generation += 1

    except KeyboardInterrupt:
        to_file(best)
    except Exception as e:
        print e

    # Fim das Gerações
    to_file(best)

if __name__ == '__main__':

    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print 'args failed'
        exit()

    cube = None
    with open(sys.argv[1], 'r') as file:

        dimensions = int(file.readline())
        if dimensions != 3:
            print 'FAILED\nOnly 3 dimensions cubes are accepted.'
            exit()

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
        print 'TEST'
        with open(sys.argv[3], 'r') as file:
            data = file.readline()
            genes = [str(x) for x in re.findall('(\S\S*)', data)]

            print '%d MOVES' % len(genes)
            my_move = Individual(cube, genes)
            result = my_move.get_cube()
            result.colored_printf()
    else:
        print 'EVOLUTION'
        file_info = open('data/data{}.txt'.format(sys.argv[2]), 'w')
        file_info.write('-1 %d %d\n' % (THETA, LAMBDA))
        best = Individual(cube)
        evolution(cube)
