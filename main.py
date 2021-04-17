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

def initiating_matrix(distance, points):
    """
    initialise la matrice des sets, sous forme d'un cadrillage du plan.
    """
    plan_division = [[set() for _ in range(int(sqrt(2)/distance) + 1)] for _ in range(int(sqrt(2)/distance) + 1)] 
    for point_index in range(len(points)):
        line_index = int((sqrt(2)*points[point_index].coordinates[0])/distance)
        colomn_index = int((sqrt(2)*points[point_index].coordinates[1])/distance)
        plan_division[line_index][colomn_index].add(point_index)
    return plan_division


def related(set_a, set_b, points, distance):
    """
    relie les points de chaque carré à ceux d'un autre par le biais de la relation DISTANCE
    """
    min_in_list = sorted([set_a, set_b], key = lambda our_set : len(our_set))
    for point_a in min_in_list[0]:
        for point_b in min_in_list[1]:
            if points[point_a].distance_to(points[point_b]) <= distance:
                return True
    return False
    
def borders(i, j, my_point, visited_set, length):
    """
    élimine les bords
    """
    return((i, j) not in [(0, 0), (-2, -2),(-2, 2),(2, -2),(2, 2)] and my_point not in visited_set and 0 <= my_point[0] < length and 0 <= my_point[1] < length)


def graph_course(points, distance, plan_division, related_component, reserve, nonused_sets, visited_set):
    """
    effectue la recherche nécassaire dans les carreaux adjacents, en utilisant la pile RESERVE
    """
    just_visited = reserve.pop()
    if len(related_component) == 0:
        related_component.append(plan_division[just_visited[0]][just_visited[1]])
    else:
        related_component[0] = related_component[0] | plan_division[just_visited[0]][just_visited[1]]
    for i in range(-2,3):
        for j in range(-2,3):
            my_point = (just_visited[0] + i, just_visited[1] + j)
            if borders(i, j, my_point, visited_set, len(plan_division)):
                if related(plan_division[just_visited[0]][just_visited[1]], plan_division[my_point[0]][my_point[1]], points, distance):
                    reserve.append(my_point)
                    visited_set.add(my_point)
                    nonused_sets.remove(my_point)
    visited_set.add(just_visited)


def print_components_sizes(distance, points):
    """
    affichage des tailles triees de chaque composante
    """
    if distance == 0:
        print([1 for _ in range(len(points))])
        return
    result = []
    plan_division = initiating_matrix(distance, points)
    nonused_sets = set((i,j) for i in range(len(plan_division)) for j in range(len(plan_division)))
    visited_set = set()
    further_step = 0
    while further_step < len(plan_division)**2:
        first_set = nonused_sets.pop()
        if len(plan_division[first_set[0]][first_set[1]]) == 0:
            further_step += 1
            visited_set.add(first_set)
            continue
        reserve = [first_set]
        related_component = []
        while len(reserve) != 0:
            graph_course(points, distance, plan_division, related_component, reserve, nonused_sets, visited_set)
            further_step += 1
        result.append(len(related_component[0]))
    result.sort()
    result.reverse()
    print(result)

def main():
    """
    ne pas modifier: on charge une instance et on affiche les tailles
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        print_components_sizes(distance, points)


main()
