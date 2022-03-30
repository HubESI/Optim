#!/usr/bin/env python
# coding: utf-8


import numpy as np
import time
#Lire une instance du graph a partir d'un fichier
def from_file(file_path):
        with open(file_path) as f:
            line = f.readline()
            while line[0] != "p":
                line = f.readline()
            n = int(line.split()[2])
            adj_mat = []
            for i in range(0,n):
                adj_mat.append([False]*n)
            for line in f:
                if line[0] == "e":
                    w, v = map(int, line.split()[1:])
                    adj_mat[w-1][v-1] = adj_mat[v-1][w-1] = True
        return np.array(adj_mat)

#Ecrire la solution dans un fichier 
def to_file(file_path , Graph):                                                                   
  Temps,Soluce = DynamicProgramming(Graph)
  with open(file_path,"w") as f:
    f.write( "# Solution pour le Graph du fichier "+file_path+"\n" )
    f.write( "Minimum number of colors used : " + str(Soluce[1]) + "\n" )
    f.write( "Temps execution :: "+str(Temps) + "\n" )
    f.write( "Color Affectation to the nodes : \n")
    [f.write( "Node "+ str(i)+ " :: "+str(Soluce[0][i]) +"\n") for i in range(0,len(Soluce[0]))]
  return

#Fonction de Transition d'un etat a un autre
#Colorer le noeud node avec toutes les couleurs possibles
#Si aucune couleur possible, ajouter une nouvelle couleur

def ColorerVoisin(Graph, state, node):
    #Le premier noeud, on lui affectte la couleur 0
    if node == 0:
        NewStates = [ ([0] , 1) ]
    else : 
        #Recuperer la colorisation sous-optimale 
        Soluce = state[0]
        #Le nombre de couleur sous-optimal
        XG = state[1]
        #Initialisation de la liste des sous-solutions optimales
        NewStates = []
        #Recuperer la liste des adjacents du noeud
        Adjacents = np.where(Graph[node][:node] == True)[0]
        #Recuperer la liste des couleurs deja utiliser par les adjacents du noeud
        AdjColor = np.unique( np.array( [Soluce[V] for V in Adjacents] ) )
        #Affecter Toutes les couleurs possibles au noeud
        for color in range(0,XG):
            if color not in AdjColor:
                NewSoluce = Soluce.copy()
                NewSoluce.append(color)
                NewState = (NewSoluce , XG)
                NewStates.append(NewState)
        #Si pas de couleurs possibles alors ajouter une nouvelle couleur
        if len(NewStates) == 0:
            NewSoluce = Soluce.copy()
            NewSoluce.append(XG)
            NewState = (NewSoluce , XG + 1)
            NewStates.append(NewState) 
    return np.array(NewStates,dtype=object)

#Programmation dynamique
#Input : Un graph a N noeuds
# Supposons qu'on a une solution optimale pour le Graph a (N - 1) Noeuds : X( G (N-1) )
# Quel est la solution optimale pour un graph a (N) Noeuds, X( G(N) ) = ?
# Ensemble des decisitons possible : 
# Soit on peut affecter une couleur au noeud N, sans enfreindre les regles de colorisation ==> X( G(N) ) = X( G(N-1) )
# Si aucune couleur possible au noeud N, Ajouter une nouvelle couleur ==> X( G(N) ) = X( G(N-1) ) + 1

def DynamicProgramming(Graph):
    #Temps initial
    ts = time.time()
    #Nombre de Noeuds
    V = len(Graph)
    #Etat initiale : Aucun noeud , 0 couleur
    state = ([],0)
    #Ensembles des etats Ek : Ensemble des colorisations possibles optimales du sous-graph a k noeuds
    Level = [np.array( [ ( [] , 0) ], dtype=object)]
    #Pour chaque Noeud : 
    for node in range(0,V):
        #Obtenir l'ensembles des etats precedent :E(k-1)
        States = Level.pop()
        #Recuperer le cout de chaque solution (nombre de couleurs)
        XG_list = States[:,1]
        #Recupere les solutions avec le moindres couts(nombre de couleur)
        indStates = np.where(XG_list== XG_list.min())[0]
        #Initialiser l'ensemble E(k)
        Solutions = []
        #Pour chaque  Solutions optimales a k-1
        for i in indStates :
            #Obtenir les nouvelles solutions optimales a l'ordre k
            Solutions.extend(ColorerVoisin(Graph,States[i],node) )
        #Ajouter les Ek
        Level.append(np.array(Solutions))
    #Recupere les solutions optimales des derniers etats E(n)
    States = Level.pop()
    XG_list = States[:,1]
    tf = time.time()
    return tf-ts,States[np.argmin(XG_list)]

def coloring_graph(fromFile , toFilePath):
  Graph = from_file(fromFile)
  to_file(toFilePath+ fromFile+".Soluce.txt",Graph)
  
coloring_graph("myciel4.col","DynamicSoluce/")






