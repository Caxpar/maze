import numpy as np
import random
from collections import deque
import queue
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

"""
def draw_maze():
    fig, ax = plt.subplots()
    for i in range(np.shape(maze)[0]):
        for j in range(np.shape(maze)[1]):
            x = i*10 + 1
            y = j*10 + 1
            h = 9
            w = 9
            cl = '#cc6600' if maze[i][j] == 1 else '#F0EEEE'
            rect = mpatches.Rectangle([x, y], w, h, color=cl)
            ax.add_patch(rect)

    plt.axis([0, dim*10 + 1, 0, dim*10 + 1])
    fig.set_size_inches(6, 6)
    plt.show()

def draw_maze_with_path():
    fig, ax = plt.subplots()
    for i in range(np.shape(maze)[0]):
        for j in range(np.shape(maze)[1]):
            x = i*10 + 1
            y = j*10 + 1
            h = 9
            w = 9
            cl = '#cc6600' if maze[i][j] == 1 else '#F0EEEE'
            if (i, j) in path:
                cl = 'green'
            rect = mpatches.Rectangle([x, y], w, h, color=cl)
            ax.add_patch(rect)

    plt.axis([0, dim*10 + 1, 0, dim*10 + 1])
    fig.set_size_inches(6, 6)
    plt.show()
"""

############# Jiyu's work #############
def make_maze(dim, p):
    maze = np.zeros((dim, dim))
    for i in range(dim):
        for j in range(dim):
            if(random.random() < p):
                maze[i][j] = 1
    maze[0][0] = 0
    maze[dim-1][dim-1] = 0
    return maze

dim = 10
p = 0.3
maze = make_maze(dim, p)

def get_method(fringe,method):
    if method == 1:
        def get():
            return fringe.pop()
    if method == 0:
        def get():
            return fringe.popleft()
    if method in (2,3):
        def get():
            pair = fringe.get()
            return pair[1]
    return get

def make_node(method, goal = (9,9)):
    if method == 1:
        fringe = []
        fringe.append((0,0))
    if method == 0:
        fringe = deque([])
        fringe.append((0,0))
    if method in (2,3):
        fringe = []
        fringe.append((0,0))
    return fringe

def heuristic(method):
    if method == 2:
        def h(node, goal):
            exp = ((goal[0]-node[0])**2 + (goal[1] - node[1])**2) ** 0.5
            return exp   
    if method == 3:
        def h(node, goal):
            exp = abs(goal[0]-node[0]) + abs(goal[1]-node[1])
            return exp
    return h

def explore_method(visited, fringe):
    def explore(node):
        x, y = node
        nodes_to_add = []
        if x-1 > -1 and (x-1, y) not in visited and maze[x-1][y] == 0 and (x-1, y) not in fringe:
            nodes_to_add.append((x-1, y))
        if y-1 > -1 and (x, y-1) not in visited and maze[x][y-1] == 0 and (x, y-1) not in fringe:
            nodes_to_add.append((x, y-1))
        if y+1 < dim and (x, y+1) not in visited and maze[x][y+1] == 0 and (x, y+1) not in fringe:
            nodes_to_add.append((x,y+1))
        if x+1 < dim and (x+1, y) not in visited and maze[x+1][y] == 0 and (x+1, y) not in fringe:
            nodes_to_add.append((x+1,y))
        return nodes_to_add
    return explore

def search(maze, method, goal):
    """ 0 for BFS; 1 for DFS; """
    
    fringe = make_node(method)
    if method in (2,3):
        h = heuristic(method)
        f_queue = queue.PriorityQueue()
        f_queue.put((h((0,0), goal), (0,0)))
    get = get_method(f_queue, method) if method in (2,3) else get_method(fringe, method)
    visited = []
    path = []
    explore = explore_method(visited, fringe)
    while fringe:
        node = get()
        fringe.remove(node)
        visited.append(node)
        path.append(node)
        if node == goal:
            print(path)
            path = list(reversed(path))
            real_path = []
            for i in range(len(path)):
                real_path.append(path[i])
            for j in range(len(path)-1):
                if path[j+1][0]!=path[j][0] and path[j+1][1]!=path[j][1]:
                    real_path.remove(path[j+1])
            path = list(reversed(real_path))
            return path
        pre_nodes = explore(node)
        fringe.extend(pre_nodes)
        if method in (2,3):
            eva_nodes = [1+h(x, goal) for x in pre_nodes]
            for i in range(len(pre_nodes)):
                f_queue.put((eva_nodes[i], pre_nodes[i]))
    return False


path = search(maze, 2, (9,9))
print(maze)
print(path)













