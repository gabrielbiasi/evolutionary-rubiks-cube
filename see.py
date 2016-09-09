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

    # Abertura dos arquivos.
    generations = [] # Gerações
    THETA = 0.0
    LAMBDA = 0.0

    # Grafico 1
    fit_media = [] # Media fitness

    # Grafico 2
    solved = [] # Solved
    tam_media = [] # Media fitness

    fase_atual = 0
    new_phase = [] # Troca de Fases

    with open(sys.argv[1], 'r') as handle:
        for line in handle:
            qq = line_to_list(line)
            if qq[0] == -1:
                THETA = qq[1]
                LAMBDA = qq[2]
            else:
                generations.append(qq[0])
                fit_media.append(qq[1])
                tam_media.append(qq[2])
                solved.append(qq[3])

                if fase_atual != qq[4]:
                    fase_atual = qq[4]
                    new_phase.append(qq[0])

    figura = plt.figure()
    ini = figura.add_subplot(211)
    end = figura.add_subplot(212)

    figura.canvas.set_window_title(u'Computação Natural')
    figura.canvas.mpl_connect('key_press_event', on_key)

    plt.subplot(211)
    plt.plot(generations, tam_media, 'r', label=u'Tamanho Média')
    plt.plot(generations, fit_media, 'g', label=u'Fitness Média')
    for p in new_phase:
        plt.axvline(x=p, color='k', linestyle='--')
    plt.ylabel(u'Fitness')
    plt.xlabel(u'Gerações')
    plt.legend(loc=0)
    plt.grid(True)
    plt.draw()

    plt.subplot(212)
    plt.plot(generations, solved, 'b', label=u'Resolvidos')
    for p in new_phase:
        plt.axvline(x=p, color='k', linestyle='--')
    plt.ylabel(u'Tamanho')
    plt.xlabel(u'Gerações')
    plt.legend(loc=0)
    plt.grid(True)
    plt.draw()

    #plt.gca().set_title(u'Result')
    #plt.gca().set_aspect('auto')
    #plt.ylim((0,105))
    #plt.xlim((1, 50))
    #plt.get_current_fig_manager().window.showMaximized()

    try:
        plt.show()
    except KeyboardInterrupt:
        os.system('clear')



