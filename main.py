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

def related(set_a, set_b, points, distance): 
    min_in_list = sorted([set_a, set_b], key = lambda our_set : len(our_set))
    for point_a in min_in_list[0]:
        for point_b in min_in_list[1]:
            if points[point_a].distance_to(points[point_b]) <= distance:
                return True
    return False
    
def borders(i, j, just_visited, visited_set, length):
    return((i, j) not in [(0, 0), (-2, -2),(-2, 2),(2, -2),(2, 2)] and (just_visited[0] + i, just_visited[1] + j) not in visited_set and 0 <= just_visited[0] + i < length and 0 <= just_visited[1] + j < length)


def initiating_matrix(distance, points):
    plan_division = [[set() for _ in range(int(sqrt(2)/distance) + 1)] for _ in range(int(sqrt(2)/distance) + 1)] 
    for point_index in range(len(points)):
        line_index = int((sqrt(2)*points[point_index].coordinates[0])/distance)
        colomn_index = int((sqrt(2)*points[point_index].coordinates[1])/distance)
        plan_division[line_index][colomn_index].add(point_index)
    return plan_division


def graph_course(points, distance, plan_division, related_component, pile, nonused_sets, visited_set):
    just_visited = pile.pop()
    if len(related_component) == 0:
        related_component.append(plan_division[just_visited[0]][just_visited[1]])
    else:
        related_component[0] = related_component[0] | plan_division[just_visited[0]][just_visited[1]]
    for i in range(-2,3):
        for j in range(-2,3):
            if borders(i, j, just_visited, visited_set, len(plan_division)):
                if related(plan_division[just_visited[0]][just_visited[1]], plan_division[just_visited[0] + i][just_visited[1] + j], points, distance):
                    pile.append((just_visited[0] + i, just_visited[1] + j))
                    visited_set.add((just_visited[0] + i, just_visited[1] + j))
                    nonused_sets.remove((just_visited[0] + i, just_visited[1] + j))
    visited_set.add(just_visited)

def print_components_sizes(distance, points):
    """
    affichage des tailles triees de chaque composante
    """
    if distance == 0:
        print([1 for _ in range(len(points))])
        return
    plan_division = initiating_matrix(distance, points)
    result = []
    visited_set = set()
    nonused_sets = set((i,j) for i in range(len(plan_division)) for j in range(len(plan_division)))
    counting = 0
    while counting < len(plan_division)**2:
        first_set = nonused_sets.pop()
        if len(plan_division[first_set[0]][first_set[1]]) == 0:
            counting += 1
            visited_set.add(first_set)
            continue
        pile = [first_set]
        related_component = []
        while len(pile) != 0:
            graph_course(points, distance, plan_division, related_component, pile, nonused_sets, visited_set)
            counting += 1
        result.append(len(related_component[0]))
    print(sorted(result)[::-1])

def main():
    """
    ne pas modifier: on charge une instance et on affiche les tailles
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        print_components_sizes(distance, points)


main()
