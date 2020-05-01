#!/usr/bin/env python3

# Point is (x, y, z) where x,y are integers and z is bool
# z True is +, z False is -

# * indicates the origin when drawing

#      /\(-1, 2, -)/\ (0, 3, -)/\ (1, 4, -)/\ (2, 5, -)/
#     /  \        /  \        /  \        /  \        / 
#    /    \      /    \      /    \      /    \      /  
#   /      \    /      \    /      \    /      \    /   
#  /        \  /        \  /        \  /        \  /    
# /          \/          \/          \/          \/     
# ------------------------------------------------------
# \          /\          /\          /\          /\     
#  \        /  \        /  \        /  \        /  \    
#   \      /    \      /    \      /    \      /    \   
#    \    /      \    /      \    /      \    /      \  
#     \  /        \  /        \  /        \  /        \ 
#      \/ (0, 1, +)\/ (1, 2, +)\/ (2, 3, +)\/ (3, 4, +)\
# ------------------------------------------------------
#      /\ (0, 1, -)/\ (1, 2, -)/\ (2, 3, -)/\ (3, 4, -)/
#     /  \        /  \        /  \        /  \        / 
#    /    \      /    \      /    \      /    \      /  
# x0/      \   1/      \   2/      \   3/      \   4/   
#  /        \  /        \  /        \  /        \  /    
# / (0, 0, +)\/ (1, 1, +)\/ (2, 2, +)\/ (3, 3, +)\/     
# *-----------------------------------------------------
# \ (0, 0, -)/\ (1, 1, -)/\ (2, 2, -)/\ (3, 3, -)/\     
#  \        /  \        /  \        /  \        /  \    
# y0\      /   1\      /   2\      /   3\      /   4\   
#    \    /      \    /      \    /      \    /      \  
#     \  /        \  /        \  /        \  /        \ 
#      \/ (1, 0, +)\/ (2, 1, +)\/ (3, 2, +)\/ (4, 2, +)\
# ------------------------------------------------------
#      /\ (1, 0, -)/\ (2, 1, -)/\ (3, 2, -)/\ (4, 2, -)/
#     /  \        /  \        /  \        /  \        / 
#    /    \      /    \      /    \      /    \      /  
#   /      \    /      \    /      \    /      \    /   
#  /        \  /        \  /        \  /        \  /    
# /          \/          \/          \/          \/     


# How does this [attempt to] draw the triangles
# We tile a cell to make a grid large enough to draw all the triangles.
# The cell is below
#       /\     
#      /  \    
#     /    \   
#    /      \  
#   /        \ 
#  /          \
#  ------------
#  \          /
#   \        / 
#    \      /  
#     \    /   
#      \  /    
#       \/     
#  ------------

from random import randint
from math import ceil,sqrt

DEBUG = False


def get_adjacent(point):
     x, y, z = point
     sign = 1 if z else -1
     return {(x, y, not z), (x - sign, y, not z), (x, y + sign, not z)}


def get_rand():
     return randint(0, 2) == 0

from collections import defaultdict

def connected(p):
    (r,c) = p
    return [(r,c-1),(r,c+1),((r+c%2)^1-c%2,c)]

def sim1():
    active = defaultdict(lambda: False)
    active[(0,0)] = True
    new_active = [(0,0)]
    count = -1

    while len(new_active) > 0:
        # print(new_active)
        count += 1
        next_new = []
        for i in set([x for p in new_active for x in connected(p)]):
            if not active[i]:
                if get_rand():
                    active[i] = True
                    next_new.append(i)
        new_active = next_new
    return count

def sim():
     timing = {}
     old_active = set()
     new_active = {(0, 0, False)} # our starting triangle
     count = -1

     while len(new_active) > 0:
          count += 1
          # get the list of triangle adject to the ones activated last round
          adjacent = set()
          for tri in new_active:
               timing[tri] = count
               adjacent.update(get_adjacent(tri))

          # remove any active triangles
          adjacent_off = adjacent - (new_active | old_active)

          # what's old is new
          old_active |= new_active
          new_active = set()

          # randomly activate triangles
          for tri in adjacent_off:
               if get_rand():
                    new_active |= {tri}

     return count #,old_active|new_active,timing)
     # return (count,old_active|new_active,timing)


# add two triangle coordinates, keeping the sign from the latter
def add_point(a, b):
     return (a[0] + b[0], a[1] + b[1], b[2])

def draw(triangles,timing):
     minx = min(triangles, key=lambda x: x[0])[0]
     miny = min(triangles, key=lambda x: x[1])[1]
     maxx = max(triangles, key=lambda x: x[0])[0]
     maxy = max(triangles, key=lambda x: x[1])[1]

     # size of the grid in traingle coordinates
     deltax = maxx - minx + 1
     deltay = maxy - miny + 1

     if DEBUG:
          print(F'minmax {minx} {maxx}  {miny} {maxy}')
          print(F'deltas {deltax} {deltay}')

     # FORGIVEME: explain top left minus and bottom left plus requirement better
     # make sure deltay is odd. This ensures that the top left triangle we draw is a minus
     if deltay % 2 == 0:
          deltay += 1
          maxy +=1

     # make sure deltax is odd and adjust maxx to agree
     if deltax % 2 == 0:
          deltax += 1
          maxx +=1

     # move things to start at the origin
     timing = {add_point(p, (-minx, -miny, p[2])) : v for p,v in
             timing.items()}
     triangles = {add_point(p, (-minx, -miny, p[2])) for p in triangles}

     render_cell = [
          '----',
          '{upleft_minus}/\{upright_minus}',
          '/{plus}{plus}\\',
          '----',
          '\{minus}{minus}/',
          '{downleft_plus}\/{downright_plus}'
     ]

     startrow = -(deltay // 2)
     stoprow = (deltax // 2) + 1   # I think add one because range(x, y) covers [x, y) and we want [x, y]

     if DEBUG:
          print(triangles)
          print(F'minmæx {minx} {maxx}  {miny} {maxy}')
          print(F'dœltas {deltax} {deltay}')
          print(F'start {startrow} stop {stoprow}')

     for row in range(startrow, stoprow):
          for line in render_cell:
               # TODO: do better with plotting -x triangle coordinate rhombuses
               for col in range((deltay + deltax) // 2):
                    this_rhombus = add_point((row, -row), (col, col, True))
                    triangles_on = {
                         "upleft_minus":   (add_point(this_rhombus,
                             (-1, 0, False)),add_point(this_rhombus,
                                 (-1, 0, False)) in triangles),
                         "upright_minus":  (add_point(this_rhombus, (
                             0, 1, False)),add_point(this_rhombus, (
                             0, 1, False)) in triangles),
                         "downleft_plus":  (add_point(this_rhombus, (0,
                             -1, True)),add_point(this_rhombus, (0,
                             -1, True)) in triangles),
                         "downright_plus": (add_point(this_rhombus, (1,
                             0, True)),add_point(this_rhombus, (1,
                             0, True)) in triangles),
                         "plus":   (this_rhombus,this_rhombus in triangles),
                         "minus": ((this_rhombus[0], this_rhombus[1],
                             False),(this_rhombus[0], this_rhombus[1],
                                 False) in triangles),
                    }

                    for k,(v0,v) in triangles_on.items():
                        if v:
                            assert v0 in triangles,(v0,k)
                            assert v0 in timing,(v0,k)

                    # print(timing)
                    triangles_on = {k: chr(ord('A')+timing.get(v0,-1)) if v
                            else ' ' for k, (v0,v) in triangles_on.items()}
                    print(line.format(**triangles_on), end='')
               print()


if __name__ == '__main__':
    for (i,f) in enumerate([sim,sim1]):
        print(i)
        results = [f() for _ in range(1000000)]
        mean = sum(results)/len(results)
        var = sum(((x-mean)**2 for x in results))/len(results)
        stddev = sqrt(var)
        median = sorted(results)[len(results)//2]

        print("  min:",min(results))
        print("  max:",max(results))
        print("  mean:",mean)
        print("  var:",var)
        print("  stddev:",stddev)
        print("  median:",median)

    # tris = sim()
    # print(tris)
    # draw(tris[1],tris[2])

