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
from individual import Individual
from cube import Cube

import traceback

file_info = None

def to_file(best):
    best_file = open("best/best{}.txt".format(sys.argv[2]), "w")
    for gene in best.genes:
        best_file.write(gene + ' ')
    best_file.close()
    file_info.close()
    print
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
    global PHASE_COUNTER

    random.seed()
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
                    print 'FOUND!'
                    to_file(best)

            # Mudança de fase!
            if solved_phase:
                PHASE_COUNTER += 1
                print 'NEW PHASE!'

            #--------------------------------------------------------------
            #--------------------- OBTENÇÃO DE DADOS ----------------------
            #--------------------------------------------------------------
            file_info.write('%d %d %d %d\n' % (generation, PHASE_COUNTER, solved_phase, best.get_fitness(PHASE_COUNTER)))
            sys.stdout.write('\rG %d\tPhase: %d/4\tSolved.: %d/%d\t' % (generation, PHASE_COUNTER, solved_count, THETA))
            sys.stdout.flush()
            #--------------------------------------------------------------
            #--------------------------------------------------------------
            #--------------------------------------------------------------

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
    finally:
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

            my_move = Individual(cube, genes)
            my_move.apply(my_move.genes)
            fit = my_move.get_fitness(0)
            print my_move
    else:
        print 'EVOLUTION'
        file_info = open('data/data{}.txt'.format(sys.argv[2]), 'w')
        file_info.write('%d %d %d\n' % (THETA, LAMBDA, GENERATIONS))
        evolution(cube)
