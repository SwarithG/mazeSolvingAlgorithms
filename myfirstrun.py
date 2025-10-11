from collections import deque

"""
Working Version With Shortest Path Reconstruction
"""
def move(row,column,direction):
    """
    This is a helper function for the Grid Sovler and helps create new co-ords to move
    Uses variable reassignment/tuple unpacking"""
    row,column = row + direction[0] , column + direction[1]
    return row,column

def main(grid):
    """
    The Main Solving Logic
    Requirements : move()
    Arguments : grid (The grid to be solved with obstacles as 1 and empty slots as 0 in a 2D List)"""
    rows,columns = len(grid) , len(grid[0]) #Analyze the length and width of the grid
    # if length != breadth:
    #     return "Not a Square Maze"
    right = (0,1)
    left = (0,-1)
    down = (1,0)
    up = (-1,0)

    directions = [up,right,down,left] #Makes a collection of all the possible moves from a given position

    dest = len(grid)-1,len(grid[0])-1 #Sets the final destination square
    #TODO Set destination square to be any square of the user's choice

    # Initializes the Queue and creates a set to store all visited nodes
    # The Queue stores the values as (node,history) where history also contains the node itself
    my_deque = deque([[(0,0),[(0,0)]]])
    visited = set()

    #Main Solving Loop
    while len(my_deque) != 0:
    
        #Removes an element from the Queue and unpacks the history and node from the element popped
        popped = my_deque.popleft()
        currentNode = popped[0]
        history = popped[1]

        #Unpacks the co-ordinates of the node
        row,column = currentNode
        
        #Checks if the current node is the dest
        if currentNode == dest:
            # print(visited)
            return "Solved the Maze",history

        #Add the current node to the history of all visited nodes
        visited.add(currentNode)

        #Iterate through the directiosn to find all valid moves from a given Node
        for di in directions:
            nr,nc = move(row,column,di)
            if 0 <= nr < rows and 0 <= nc < columns and grid[nr][nc] != 1:
                cord = nr,nc

                #If the discovered node is unseen and valid add it to the queue after updating it's hisotry
                if cord not in visited:
                    copy = list(history)
                    copy.append(cord)
                    my_deque.append([cord,copy])
                    visited.add(cord)

    #If the code reached here then there are no more valid nodes to reach and we haven't got to dest
    return "No Path Found",(0,0)
if __name__=="__main__":
    grid = [
        [0,1,1,0,0],
        [0,1,0,0,0],
        [0,1,0,1,0],
        [0,0,0,1,0]
    ]
    for i in grid:
        print(i)
    print("\n"*2)
    sol,path = main(grid)
    print(sol)
    print(path)