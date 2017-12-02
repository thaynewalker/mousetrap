import random

mx = 1; my = 1 # width and height of the maze
maze = [[1 for x in range(mx)] for y in range(my)]
dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0] # directions to move in the maze


def GenerateMaze(cx, cy):
    maze[cy][cx] = 0
    while True:
        # find a new cell to add
        nlst = [] # list of available neighbors
        for i in range(4):
            nx = cx + dx[i]; ny = cy + dy[i]
            if nx >= 0 and nx < mx and ny >= 0 and ny < my:
                if maze[ny][nx] == 1:
                    # of occupied neighbors of the candidate cell must be 1
                    ctr = 0
                    for j in range(4):
                        ex = nx + dx[j]; ey = ny + dy[j]
                        if ex >= 0 and ex < mx and ey >= 0 and ey < my:
                            if maze[ey][ex] == 0: ctr += 1
                    if ctr == 1: nlst.append(i)
        # if 1 or more available neighbors then randomly select one and add
        if len(nlst) > 0:
            ir = nlst[random.randint(0, len(nlst) - 1)]
            cx += dx[ir]; cy += dy[ir]
            GenerateMaze(cx, cy)
        else: break

def SquareMaze(cx,cy):
    stack = [(cx, cy, 0)]
    maze[cy][cx]=0
    while len(stack) > 0:
        (cx, cy, cd) = stack[-1]
        # to prevent zigzags:
        # if changed direction in the last move then cannot change again
        if len(stack) > 2:
            if cd != stack[-2][2]: dirRange = [cd]
            else: dirRange = range(4)
        else: dirRange = range(4)
    
        # find a new cell to add
        nlst = [] # list of available neighbors
        for i in dirRange:
            nx = cx + dx[i]; ny = cy + dy[i]
            if nx >= 0 and nx < mx and ny >= 0 and ny < my:
                if maze[ny][nx] == 1:
                    ctr = 0 # of occupied neighbors must be 1
                    for j in range(4):
                        ex = nx + dx[j]; ey = ny + dy[j]
                        if ex >= 0 and ex < mx and ey >= 0 and ey < my:
                            if maze[ey][ex] == 0: ctr += 1
                    if ctr == 1: nlst.append(i)
    
        # if 1 or more neighbors available then randomly select one and move
        if len(nlst) > 0:
            ir = nlst[random.randint(0, len(nlst) - 1)]
            cx += dx[ir]; cy += dy[ir]; maze[cy][cx] = 0
            stack.append((cx, cy, ir))
        else: stack.pop()


def Generate(w,h):
    global mx,my,maze
    mx=w-1
    my=h-1
    maze = [[1 for x in range(mx)] for y in range(my)]
    SquareMaze(0, 0)
    for line in maze:
	line.append(1)
        line.insert(0,1)
    maze.insert(0,[1 for x in range(mx+2)])
    maze.append([1 for x in range(mx+2)])
    return maze


