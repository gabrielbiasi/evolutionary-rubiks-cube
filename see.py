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
    generations = []

    media = [] # Media
    fit_desvio = [] # desvio padrao
    tam_media = [] # tam_media
    tam_desvio = [] # desvio padrao
    melhor = [] # Melhor
    pior = [] # Pior

    with open(sys.argv[1], 'r') as handle:
        for line in handle:
            qq = line_to_list(line)
            generations.append(float(qq[0]))

            media.append(float(qq[1]))
            fit_desvio.append(float(qq[2]))
            tam_media.append(float(qq[3]))
            tam_desvio.append(float(qq[4]))

            melhor.append(float(qq[5]))
            pior.append(float(qq[6]))

    figura = plt.figure()
    ini = figura.add_subplot(211)
    end = figura.add_subplot(212)

    figura.canvas.set_window_title(u'Computação Natural')
    figura.canvas.mpl_connect('key_press_event', on_key)

    plt.subplot(211)
    
    plt.plot(generations, melhor, 'r', label=u'Melhor')
    plt.plot(generations, media, 'g', label=u'Média')
    plt.plot(generations, fit_desvio, 'm', label=u'Desvio Padrão')
    plt.plot(generations, pior, 'b', label=u'Pior')
    plt.ylabel(u'Fitness')
    plt.xlabel(u'Gerações')
    plt.legend(loc=0)
    plt.grid(True)
    plt.draw()

    plt.subplot(212)

    plt.plot(generations, tam_media, 'r', label=u'Tamanho Médio')
    plt.plot(generations, tam_desvio, 'm', label=u'Desvio Padrão')

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



