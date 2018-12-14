#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 21:41:01 2018

@author: Bastien
"""

import urllib
import requests
import re
  

def parse_english_word(text):
    '''Cette fonction permet de récupérer le mot anglais dont on veut la traduction'''
    w = ''
    definition = ''
    deadlock = False
    for z in text.split():
        if (w.lower()).startswith('<title>'):   # on détecte le <Title>
            if ('Cambridge' in w):
                raise ValueError
            definition += (w.lower()).replace('<title>','')
            if z=="|":
                return(definition)
            deadlock = True
            w = z
        elif deadlock and z!="|":
            definition += ' '+w.lower()
            w = z
        elif z=="|":
            definition += ' '+w.lower()
            break
        else:
            w = z #une variable qui permet de faire un suivi des mots précédents 
    return(definition)

#print(parse_english_word(textWebPage))


def parse_english_definition(text):
    '''Cette fonction permet de récupérer la définition du mot anglais'''
    w = ''  #le mot avant le mot z qui parcourt le fichier html
    definition = ''
    deadlock = False
    for z in text.split():
        if w.lower()=='definition:':   # on détecte la définition>
            definition += (z +' ')
            deadlock = True
            w = z
        elif deadlock and (z!='.' and z!='Learn'):
            definition += (z +' ')
            w = z
        elif z=='.' or z=='Learn':
            break
        else:
            w = z #une variable qui permet de faire un suivi des mots précédents 
    return(definition[:-2])

#print(parse_english_definition(textWebPage))

def parse_english_pronunciation(text):
    '''Cette fonction permet de récupérer la prononciation du mot anglais, si elle existe'''
    pronunciation = ''
    for z in text.split():
        if z.find('ipa')!=-1:   # on détecte la définition
            try:
                l = re.search('">(.+?)</span',z).group(1)
                pronunciation += '/'+l+'/'
                return(pronunciation)
            except AttributeError: # les balises ne sont pas trouvées
                print('Prononciation mal configurée') # on lève une exception
    return('')


def get_definition(link):
    '''Cette fonction permet d'avoir le mot en anglais, sa prononciation et  sa définition si on donne 'link' l'adresse
    de la définition sur un des sites définis'''
    try:
        f = urllib.request.urlopen(link)
        myfile = f.read() # la variable est de la classe bytes
        text = myfile.decode("utf-8") # cette fois-ci la var est de la classe str 
        return(parse_english_word(text) + ' ' + parse_english_pronunciation(text) + ' = ' + parse_english_definition(text))
    except ValueError:
        print('\n /!\ Le site ne connaît pas ce mot /!\ ')
        raise

   
def input_link_cambridge(entree):
    '''Pour un mot donné, retourne le lien correspondant sur le site Cambidge'''
    word = entree.replace(" ", "-")
    word = word.replace("/", "-")
    link = 'https://dictionary.cambridge.org/dictionary/english/'+word.lower()
    return(link)
    
def vocabulaire_cambridge(entree):
    link = input_link_cambridge(entree)
    try:
        definition = get_definition(link)
        print('\n -->',definition,'\n')
        file = open('Vocabulaire 0.txt','a')
        file.write('\n'+definition) 
        file.close()
    except ValueError:
        print("Ce n'est probablement pas le bon orthographe")

def app_cambridge():
    '''Fait tourner indéfiniment la fonction vocabulaire_cambridge jusqu'à l'arrêt
    par l'utilisateur'''
    print(' \n [Q] pour quitter [E] pour effacer \n Entre le mot dont tu veux la définition :\n')
    entree = input()
    if entree=='E':
        open('Vocabulaire 0.txt','w').close()   # on efface tout le fichier de vocabulaire
    elif entree=='Q' or entree=='q':
        return()
    else:
        vocabulaire_cambridge(entree)
        app_cambridge()


# Un chtit test

if __name__=='__main__':
    app_cambridge()

#%%


link = 'https://dictionary.cambridge.org/dictionary/english/umbrage'
f = urllib.request.urlopen(link)
myfile = f.read() # la variable est de la classe bytes
text = myfile.decode("utf-8")
words = text.split()
print(parse_english_pronunciation(text))
    
# Ancien test
#if __name__=='__main__':
#    link = 'https://dictionary.cambridge.org/dictionary/english/blow-off-steam'
#    link2 = 'https://dictionary.cambridge.org/dictionary/english/bygone'
#    f = urllib.request.urlopen(link)
#    myfile = f.read() # la variable est de la classe bytes
#    textWebPage = myfile.decode("utf-8") # cette fois-ci la var est de la classe str 
#    print(get_definition_cambridge("https://dictionary.cambridge.org/dictionary/english/bygone"))
#    print(get_definition_cambridge("https://dictionary.cambridge.org/dictionary/english/blow-off-steam"))