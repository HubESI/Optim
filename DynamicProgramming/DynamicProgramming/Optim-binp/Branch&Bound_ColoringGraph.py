#Retourner les couleurs utilisées et leurs nombre
def Couleur(Soluce):
  couleurs = [] #Liste de couleur
  Nbcoul = 0    #Nombre de couleur
  for coul in Soluce :
    if not coul  in couleurs :
      Nbcoul = Nbcoul + 1
      couleurs.append(coul)
  return couleurs,Nbcoul

#Les Adjacents d'un Noeud
def Adjacents(Graph,i):
  Adj = []
  for j in range(0,len(Graph[i])):
    if Graph[i][j] > 0:
      Adj.append(j)
  return Adj

#Separation de solution
def GenererSoluces(Graph,Soluce,level):
  Adjs = Adjacents(Graph,level)
  sauvSoluce = Soluce.copy()
  Soluces = []
  couleurs,Nbcoul = Couleur(Soluce)
  CoulAdj = [Soluce[adj] for adj in Adjs]
  for color in couleurs:
    if (not color in CoulAdj)  :
      sauvSoluce[level] = color
      Soluces.append(sauvSoluce.copy())

  return Soluces

def ColoringGraph(Graph):
  N = len(Graph)                            #Nombre de noeuds
  Soluce = list(range(0,N))                 #Solution initiale
  Bound = N                                 #Au max N couleurs (une pour chaque noeud)
  level = 0                                 #Niveau de l'arbe  / Numero du noeud aue l'on colorise
  fifo = []                                 #Declarer une file
  Noeud = Soluce,level,N                    #Un noeud c'est la colorisation ,le niveau , L'evaluation
  fifo.append(Noeud)
  finalSoluce = Soluce,N                    #Solution Finale = Colorisation + Nombre de couleur
  while(len(fifo) > 0):
    Noeud = fifo.pop(0)
    level = Noeud[1] + 1
    Soluce = Noeud[0]
    if Noeud[2] <= Bound :
      if level < N:                         #Si on est pas au niveau des feuilles
        fils = GenererSoluces(Graph,Soluce,level)
        for i in range(0,len(fils)):        #Pour chaque fils
          colors,nbcol = Couleur(fils[i])   #Evaluer la solution
          Noeud = fils[i],level,nbcol       #Creer le Noeud
          if nbcol < Bound:
            Bound = nbcol                   #Mise a jours du bound
            finalSoluce = fils[i],nbcol     #Stocker la nouvelle meilleur solution
          fifo.append(Noeud)                #Enfiler le noeud
  return finalSoluce

#Exemple 1
Graph = [[ 0, 1, 1, 0, 1, 0],
     [ 1, 0, 1, 1, 0, 1],
     [ 1, 1, 0, 1, 1, 0],
     [ 0, 1, 1, 0, 0, 1],
     [ 1, 0, 1, 0, 0, 1],
     [ 0, 1, 0, 1, 1, 0]
]

#Exemple 2 : PETERSON GRAPH
Graph2 = [                           
     [ 0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
     [ 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
     [ 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
     [ 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
     [ 1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
     [ 1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
     [ 0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
     [ 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
     [ 0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
     [ 0, 0, 0, 0, 1, 0, 1, 1, 0, 0]
]
#Exemple 3: Contre-Exemple de worsh et Powel (Qui donne 3 couleurs)
Graph3 = [                           
     [ 0, 1, 0, 0, 0, 0, 0, 0],
     [ 1, 0, 1, 0, 0, 0, 0, 1],
     [ 0, 1, 0, 1, 0, 0, 0, 0],
     [ 0, 0, 1, 0, 1, 0, 0, 0],
     [ 0, 0, 0, 1, 0, 1, 1, 0],
     [ 0, 0, 0, 0, 1, 0, 0, 0],
     [ 0, 0, 0, 0, 1, 0, 0, 1],
     [ 0, 1, 0, 0, 0, 0, 1, 0],   
]
Gs = [Graph,Graph2,Graph3]
for i in range(0,len(Gs)):
    Soluce = ColoringGraph(Gs[i])
    print("Solution du Graph ",i+1," : "," Colorisation: ",Soluce[0]," avec ",Soluce[1], " couleur")