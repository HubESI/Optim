import math
import random
import sys
from copy import copy
from turtle import position
from typing import Tuple

import numpy as np

from coloring import Coloring, Graph, timer

CONFLICT_PENALTY = 10


# Les Adjacents d'un Noeud
def Adjacents(Graph, i):
    Adj = []
    [Adj.append(j) if Graph[i][j] else None for j in range(0, len(Graph))]
    return Adj


def nb_conflits(G: np.ndarray, soluce: np.ndarray) -> int:
    nb = 0
    if soluce.shape[0] < G.shape[0]:
        print("Problem : ", G.shape[0], ",G.shape[0] ", soluce.shape[0])
    for i in range(G.shape[0]):
        for j in range(i):
            if G[i][j] and soluce[i] == soluce[j]:
                nb = nb + 1
    return nb


def Couleurs(Soluce: np.ndarray) -> Tuple[np.ndarray, int]:
    couleurs = np.unique(Soluce)
    return couleurs


def random_Soluce(Graph: np.ndarray) -> np.ndarray:
    Soluce = []
    for i in range(len(Graph)):
        Soluce.append(random.random() * len(Graph))
    return np.array(Soluce)


def fitness_colors(
    Graph: np.ndarray, Soluce: np.ndarray, poid_conflits: float = 1.0
) -> int:
    round_Soluce = np.fix(Soluce)
    nb_colors = len(Couleurs(round_Soluce))
    nb_conflit = nb_conflits(Graph, round_Soluce)
    return nb_colors + nb_conflit * poid_conflits, nb_conflit


# Dictionnaire de couleurs pour recherche local
def count_couleurs(Soluce):
    count_color = {}
    for color in Soluce:
        if color in count_color.keys():
            count_color[color] += 1
        else:
            count_color[color] = 1
    return count_color


# Affecter la couleur dans la recherche local
def affecter_couleur(Graph, Soluce, count_couleur, noeud):
    Adjs = Adjacents(Graph, noeud)
    cpt_col = 0
    choix_col = Soluce[noeud]
    nbc = len(count_couleur.keys())
    for color in count_couleur.keys():  # pour chaque couleur
        # Verifier s'il n y a pas de noeud adjacents avec cette couleur
        possible = True
        for adj in Adjs:
            if color == Soluce[adj]:
                possible = False
                break
        if possible:  # Si on peut affecter la couleur
            if count_couleur[color] > cpt_col:
                choix_col = color
                cpt_col = count_couleur[color]
    # Affecter la couleur au noeud
    old_col = Soluce[noeud]
    count_couleur[Soluce[noeud]] -= 1
    Soluce[noeud] = choix_col
    count_couleur[choix_col] += 1
    if count_couleur[old_col] == 0:
        count_couleur.pop(old_col)
    return Soluce, count_couleur


# Variable neighbourhood  searsh <==> Local search
def proc_VNS(Graph, init_Soluce, max_stagnation, max_iter):
    count_couleur = count_couleurs(init_Soluce)
    best_soluce = init_Soluce
    best_fitness = len(count_couleur.keys())
    V = len(Graph)
    for Iter in range(max_iter):
        count_coleur = count_couleurs(init_Soluce)
        fitness = len(count_couleur.keys())
        Soluce = init_Soluce
        k = 1
        while k <= max_stagnation:
            noeud = random.randint(0, V - 1)
            new_Soluce, count_couleur = affecter_couleur(
                Graph, Soluce, count_couleur, noeud
            )
            new_fitness = len(count_couleur.keys())
            if new_fitness < fitness:
                fitness = new_fitness
                k = 1
                Soluce = new_Soluce
                if fitness < best_fitness:
                    best_fitness = fitness
                    best_soluce = Soluce
            else:
                k = k + 1
    return np.array(best_soluce), best_fitness


def fitness_colors(
    Graph: np.ndarray, Soluce: np.ndarray, poid_conflits: float = 1.0
) -> int:
    round_Soluce = np.fix(Soluce)
    nb_colors = len(Couleurs(round_Soluce))
    nb_conflit = nb_conflits(Graph, round_Soluce)
    return nb_colors + nb_conflit * poid_conflits, nb_conflit


# whale class
class whale:
    def __init__(self, fitness, dim, minx, maxx, seed, graphe, weight):
        self.weight_conflit = weight
        self.graphe = graphe
        self.rnd = random.Random(seed)
        self.position = [0.0 for i in range(dim)]
        for i in range(dim):
            self.position[i] = (maxx - minx) * self.rnd.random() + minx
        fitness, conflicts = fitness(
            graphe, self.position, self.weight_conflit
        )  # curr fitness
        self.fitness = fitness
        self.conflicts = conflicts


class WOA(Coloring):
    def __init__(
        self,
        g: Graph,
        nb_search_agents: int = 30,
        max_iter: int = 100,
        epsilon=0.5,
        vns_iteration=65,
    ):
        super().__init__(g)
        self.graphe = np.array(g.adj_mat)
        self.greedy_coloring()
        self.bound = self.solution[0]
        self.dim = self.g.order
        self.nb_search_agents = nb_search_agents
        self.fitness = fitness_colors
        self.conflict_penalty = CONFLICT_PENALTY
        self.max_iter = max_iter
        self.epsilon = epsilon
        self.vns_iteration = vns_iteration
        self.leader_pos = None
        self.leader_score = None
        self.leader_score_info = (None, None, None)
        self.positions = None
        self.convergence_curve = None

    @timer
    def solve(self):
        bestAgents = np.zeros(self.max_iter)
        nb_conflicts = np.zeros(self.max_iter)
        rnd = random.Random(0)

        # create n random whales
        whalePopulation = [
            whale(self.fitness, self.dim, 0, self.dim, i, self.graphe, CONFLICT_PENALTY)
            for i in range(self.nb_search_agents)
        ]

        # compute the value of best_position and best_fitness in the whale Population
        Xbest = [0.0 for i in range(self.dim)]
        Fbest = sys.float_info.max

        for i in range(self.nb_search_agents):  # check each whale
            if whalePopulation[i].fitness < Fbest:
                Fbest = whalePopulation[i].fitness
                Xbest = copy(whalePopulation[i].position)
                Fconflicts = whalePopulation[i].conflicts

        # main loop of woa
        Iter = 0
        while Iter < self.max_iter:

            # after every 10 iterations
            # print iteration number and best fitness value so far
            # if Iter % 100 == 0 and Iter > 1:
            #    print("Iter = " + str(Iter) + " best fitness = ", Fbest)

            # linearly decreased from 2 to 0
            a = 2 * (1 - Iter / self.max_iter)
            a2 = -1 + Iter * ((-1) / self.max_iter)

            for i in range(self.nb_search_agents):
                r = rnd.random()
                A = 2 * a * rnd.random() - a
                C = 2 * rnd.random()
                b = 1
                l = (a2 - 1) * rnd.random() + 1
                p = rnd.random()
                D = [0.0 for i in range(self.dim)]
                D1 = [0.0 for i in range(self.dim)]
                Xnew = [0.0 for i in range(self.dim)]
                Xrand = [0.0 for i in range(self.dim)]
                wi = math.exp(Iter / (self.max_iter - 1))
                if p < 0.5:
                    if abs(A) < 1:
                        for j in range(self.dim):
                            D[j] = abs(C * Xbest[j] - whalePopulation[i].position[j])
                            Xnew[j] = Xbest[j] - wi * A * D[j]
                    else:  # |A| <= 1
                        if r < 0.5:
                            # eq 15 : X(t+1) = X_best + epsilon * normal_distr_N(0,1) * wi
                            delta = np.random.normal(0, 1, self.dim)
                            for j in range(self.dim):
                                Xnew[j] = Xbest[j] + self.epsilon * delta[j] * float(
                                    (self.max_iter - Iter) / self.max_iter
                                )
                                if Xnew[j] < 0.0:
                                    # print("Xnew < 0")
                                    Xnew[j] = 0.0
                                else:
                                    if Xnew[j] >= self.dim:
                                        # print("Xnew >= dim = ",dim)
                                        Xnew[j] = self.dim - 1
                        else:
                            # eq 12 :  X(t+1) = Xrand - wi * A * D
                            p = random.randint(0, self.nb_search_agents - 1)
                            while p == i:
                                p = random.randint(0, self.nb_search_agents - 1)
                            Xrand = whalePopulation[p].position
                            for j in range(self.dim):
                                D[j] = abs(
                                    C * Xrand[j] - whalePopulation[i].position[j]
                                )
                                Xnew[j] = Xrand[j] - wi * A * D[j]
                        if r > 0.5:
                            # Update the local optimal solution
                            Xnew = proc_VNS(
                                self.graphe, np.fix(Xnew), 3, self.vns_iteration
                            )[0]

                else:  # p > 0.5
                    if r < 0.5:
                        # eq 15 : X(t+1) = X_best + epsilon * normal_distr_N(0,1) * wi
                        delta = np.random.normal(0, 1, self.dim)
                        for j in range(self.dim):
                            Xnew[j] = Xbest[j] + self.epsilon * delta[j] * float(
                                (self.max_iter - Iter) / self.max_iter
                            )
                            if Xnew[j] < 0.0:
                                #   print("Xnew < 0")
                                Xnew[j] = 0.0
                            else:
                                if Xnew[j] >= self.dim:
                                    #        print("Xnew >= dim = ",dim)
                                    Xnew[j] = self.dim - 1
                    else:
                        for j in range(self.dim):
                            D1[j] = abs(Xbest[j] - whalePopulation[i].position[j])
                            Xnew[j] = (
                                wi * D1[j] * math.exp(b * l) * math.cos(2 * math.pi * l)
                                + Xbest[j]
                            )
                    if r > 0.5:
                        Xnew = proc_VNS(
                            self.graphe, np.fix(Xnew), 3, self.vns_iteration
                        )[0]
                        # Xbest,Fbest = proc_VNS(graphe , np.fix(Xbest) , 3 , 100)

                for j in range(self.dim):
                    whalePopulation[i].position[j] = Xnew[j]

            for i in range(self.nb_search_agents):
                # if Xnew < minx OR Xnew > maxx
                # then clip it
                for j in range(self.dim):
                    whalePopulation[i].position[j] = max(
                        whalePopulation[i].position[j], 0
                    )
                    whalePopulation[i].position[j] = min(
                        whalePopulation[i].position[j], self.dim
                    )

                whalePopulation[i].fitness, whalePopulation[i].conflicts = self.fitness(
                    whalePopulation[i].graphe,
                    whalePopulation[i].position,
                    whalePopulation[i].weight_conflit,
                )

                if whalePopulation[i].fitness < Fbest:
                    Xbest = copy(whalePopulation[i].position)
                    Fbest = whalePopulation[i].fitness
                    Fconflicts = whalePopulation[i].conflicts

            bestAgents[Iter] = Fbest
            nb_conflicts[Iter] = Fconflicts
            Iter += 1
        # end-while

        # returning the best solution
        self.solution = (Fbest, list(map(int, Xbest)))
        return bestAgents, nb_conflicts


if __name__ == "__main__":
    g = Graph.from_file("instances/myciel4.col")
    col = WOA(g)
    r = col.solve()
    t = r[1]
    col.to_file(
        "instances/myciel4.col.vdwoa.sol",
        method_time_info=f"VDWA {t:0.6f} seconds",
    )
