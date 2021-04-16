#!/usr/bin/env python3
"""
compute sizes of all connected components.
sort and display.
"""

from timeit import timeit
from sys import argv

from geo.point import Point
from math import sqrt


def load_instance(filename):
    """
    loads .pts file.
    returns distance limit and points.
    """
    with open(filename, "r") as instance_file:
        lines = iter(instance_file)
        distance = float(next(lines))
        points = [Point([float(f) for f in l.split(",")]) for l in lines]

    return distance, points

def is_in_relation(set1, set2, points, distance):
    if 0 in [len(set1), len(set2)]:
        return (False, False)
    for point0 in set1:
        for point1 in set2:
            if points[point0].distance_to(points[point1]) <= distance:
                return (True, True)
    return (False, True)
    
def signe(entier):
    if entier == 0:
        return 0
    else:
        return int(abs(entier)/entier)



def print_components_sizes(distance, points):
    """
    affichage des tailles triees de chaque composante
    """
    if distance == 0:
        print([1 for _ in range(len(points))])
        return
    pavage_plan = [[set() for _ in range(int(sqrt(2)/distance) + 1)] for _ in range(int(sqrt(2)/distance) + 1)] 
    for indice_point in range(len(points)):
        n = int((sqrt(2)*points[indice_point].coordinates[0])/distance)
        m = int((sqrt(2)*points[indice_point].coordinates[1])/distance)
        pavage_plan[n][m].add(indice_point)
    nombre_traitees = 0
    element_deja_traitee = set()
    element_non_traite = set((i,j) for i in range(len(pavage_plan))for j in range(len(pavage_plan)))
    composantes_connexes = []
    while nombre_traitees < len(pavage_plan)**2:
        element_initial = element_non_traite.pop()
        if len(pavage_plan[element_initial[0]][element_initial[1]]) == 0:
            nombre_traitees += 1
            element_deja_traitee.add(element_initial)
            continue
        pile = [element_initial]
        composante_connexe = 0
        while len(pile) != 0:
            couramment_traitee = pile.pop()
            composante_connexe += len(pavage_plan[couramment_traitee[0]][couramment_traitee[1]])
            a_ne_pas_traiter = [(-2,-2),(-2,2),(2,-2),(2,2)]
            for ligne in [0, -1,-2, 1, 2]:
                for colonne in [0, -1, -2 , 1, 2]:
                    if (ligne, colonne) != (0,0) and (couramment_traitee[0]+ligne, couramment_traitee[1]+colonne) not in element_deja_traitee and (ligne,colonne) not in a_ne_pas_traiter and 0 <= couramment_traitee[0]+ligne < len(pavage_plan) and 0 <= couramment_traitee[1]+colonne < len(pavage_plan):
                        in_relation = is_in_relation(pavage_plan[couramment_traitee[0]][couramment_traitee[1]], pavage_plan[couramment_traitee[0]+ligne][couramment_traitee[1]+colonne], points, distance)
                        if in_relation[0]:
                            pile.append((couramment_traitee[0]+ligne, couramment_traitee[1]+colonne))
                            element_deja_traitee.add((couramment_traitee[0]+ligne, couramment_traitee[1]+colonne))
                            element_non_traite.remove((couramment_traitee[0]+ligne, couramment_traitee[1]+colonne))
                        if not in_relation[0] and in_relation[1]:
                            if ligne == 0:
                                for h in range(-1,2):
                                    a_ne_pas_traiter.append((h, colonne + signe(colonne)))
                            if colonne == 0:
                                for r in range(-1,2):
                                    a_ne_pas_traiter.append((ligne + signe(ligne), r))
                                    
                                    
                                    
            nombre_traitees += 1
            element_deja_traitee.add(couramment_traitee)
        composantes_connexes.append(composante_connexe)
    print(sorted(composantes_connexes)[::-1])






def main():
    """
    ne pas modifier: on charge une instance et on affiche les tailles
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        print_components_sizes(distance, points)


main()
