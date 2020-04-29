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
from math import ceil

DEBUG = False


def get_adjacent(point):
     x, y, z = point
     sign = 1 if z else -1
     return {(x, y, not z), (x - sign, y, not z), (x, y + sign, not z)}


def get_rand():
     return randint(0, 2) == 0


def sim():
     old_active = set()
     new_active = {(0, 0, False)} # our starting triangle

     while len(new_active) > 0:
          # get the list of triangle adject to the ones activated last round
          adjacent = set()
          for tri in new_active:
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
     return new_active | old_active


# add two triangle coordinates, keeping the sign from the latter
def add_point(a, b):
     return (a[0] + b[0], a[1] + b[1], b[2])

def draw(triangles):
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
          miny -=1

     # make sure deltax is odd and adjust maxx to agree
     if deltax % 2 == 0:
          deltax += 1
          minx +=1

     # move things to be at the origin ish
     triangles = {add_point(p, (-minx + 1, -miny, p[2])) for p in triangles}
     if DEBUG:
          print(F'minmæx {minx} {maxx}  {miny} {maxy}')
          print(F'dœltas {deltax} {deltay}')

     render_cell = [
          '----',
          '{upleft_minus}/\{upright_minus}',
          '/{plus}{plus}\\',
          '----',
          '\{minus}{minus}/',
          '{downleft_plus}\/{downright_plus}'
     ]


     for row in range(-deltay // 2, deltax // 2 + 1):
          for line in render_cell:
               this_rhombus = (-row, row) # I think this should be (-row, row), but this makes it work so *SHRUG?*

               # do better with plotting -x triangle coordinate rhombuses
               for col in range((deltay + deltax) // 2):
               # for col in range(-deltax // 2, deltay // 2 + 1):
                    this_rhombus = add_point(this_rhombus, (col, col, True))
                    triangles_on = {
                         "upleft_minus":   add_point(this_rhombus, (-1, 0, False)) in triangles,
                         "upright_minus":  add_point(this_rhombus, ( 0, 1, False)) in triangles,
                         "downleft_plus":  add_point(this_rhombus, (0, -1, True)) in triangles,
                         "downright_plus": add_point(this_rhombus, (1,  0, True)) in triangles,
                         "plus":   this_rhombus in triangles,
                         "minus": (this_rhombus[0], this_rhombus[1], False) in triangles,
                    }

                    triangles_on = {k: 'X' if v else ' ' for k, v in triangles_on.items()}
                    print(line.format(**triangles_on), end='')
               print()

                    
               


if __name__ == '__main__':
     tris = sim()
     print(tris)
     draw(tris)
     # draw({(0, 0, True), (0, 0, False), (1, 0, True)})
     # draw({(0, 0, True), (0, 0, False), (1, 0, True), (0, -1, False)})
     # draw({(0, 0, True), (0, 0, False), (1, 0, True), (0, 1, False)})
