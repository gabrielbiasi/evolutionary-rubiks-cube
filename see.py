#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Universidade Federal de Minas Gerais
Departamento de Ciência da Computação
Programa de Pós-Graduação em Ciência da Computação

Projeto e Análise de Algoritmos
Projeto Final de Curso

Feito por Gabriel de Biasi, 2016672212.
"""
import os, sys, re
import matplotlib.pyplot as plt

def line_to_list(string):
    return [float(x) for x in re.findall(r'[+-]?\d+\.*\d*', string)]

def on_key(event):
    if event.key == 'escape':
        exit()

if __name__ == '__main__':

    # Teste de parâmetro.
    if len(sys.argv) != 2:
        print 'fail'
        exit()

    ci = 0
    figura = plt.figure()
    color = ['r', 'g', 'b', 'y']
    for file in sys.argv[1].split(','):

        # Abertura dos arquivos.
        generations = [] # Gerações
        tam_candidatos = [] # Media fitness
        THETA = 0.0
        LAMBDA = 0.0

        with open('data/'+file, 'r') as handle:
            for line in handle:
                qq = line_to_list(line)
                if qq[0] == -1:
                    THETA = qq[1]
                    LAMBDA = qq[2]
                else:
                    generations.append(qq[0])
                    tam_candidatos.append(qq[1])

        figura.canvas.set_window_title(u'Computação Natural')
        figura.canvas.mpl_connect('key_press_event', on_key)

        plt.subplot(111)
        plt.plot(generations, tam_candidatos, color[ci], label=u'L=%d\nT=%d' % (LAMBDA, THETA))
        plt.ylabel(u'Tamanho Médio')
        plt.xlabel(u'Gerações')
        plt.legend(loc=2)
        plt.grid(True)

        ci += 1

    plt.draw()
    plt.show()



