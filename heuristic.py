#   Huynh Tan Luan          1914054
#   Nguyen Thanh Luu        1914084
#   Nguyen Tran Quoc Uy     1915866

from asyncio import constants
from os import curdir

from matplotlib.cbook import print_cycles
from sympy import N, false, true

import time
import tracemalloc

import numpy as np

# def isContain(child, parrent):
#     for i in range(len(child)):
#         if child[i] == -1:          return True
#         if child[i] != parrent[i]:  return False
#     return True


def genState(constraint): # [1,3]
    if len(constraint) == 0:
        return [[0,0,0,0,0]]
    if len(constraint) == 3:
        return [[1,0,1,0,1]]
    
    if len(constraint) == 1:
        num = constraint[0]
        
        board_tmp =[]   # return
        # board_tmp = [[0 for i in range(w_size)] for i in range(h_size)]
        
        point_list = [1 for i in range(num)]
        
        for j in range(size - num +1):
            head = [0 for i in range(j)]
            tail = [0 for i in range(size - len(head) -num)]
            
            tmp = head + point_list + tail
            
            board_tmp += [tmp]
            
        # print (board_tmp)
        return board_tmp
        
    if len(constraint) == 2:
        l = constraint[0]
        r = constraint[1]
        
        board_tmp =[]   # return
        
        
        point_L = [1 for i in range(l)]
        point_R = [1 for i in range(r)]
        
        for tmp_mid_num in list(range(1, size - l - r +1)):
            midLR = point_L + [0 for i in range(tmp_mid_num)] + point_R
            
            for n_head in range(0, size - len(midLR)+1):
                head = [0 for i in range(n_head)]
                # tmp = head                
                # print (n_head,', head = ', head)
                
                tail = [0 for i in range(size - len(midLR) - n_head)]
                
                tmp = head + midLR + tail
                
                board_tmp += [tmp]
        
                
        return board_tmp
        
def checkBoard(board_curr):
    if board_curr[0][0] == -1:
        return True
    
    #count current height
    curr_height = 0
    for num_row in range(len(board_curr)):
        if board_curr[num_row][0] == -1:
            break
        curr_height += 1
        
    ## checkrow
    for num_row in range(len(board_curr)):
        if board_curr[num_row][0] == -1:
            # return True
            break
        if not (board_curr[num_row] in genState(row_constraint_init[num_row])):
            return False
        # print ('done row ',num_row)
        
    # check column
    arr = np.array(board_curr)
    board_trans = arr.transpose()
    board_trans = board_trans.tolist()
    
    for num_col in range(len(board_trans)):
        # col_gen_limit_list = [a[:curr_height] for a in genState(column_constraint_init[num_col])]
        
        col_gen_limit_raw = genState(column_constraint_init[num_col])        # [[]]
        
        col_gen_limit_list = [a[:curr_height] for a in col_gen_limit_raw]
        
        col_curr = board_trans[num_col][:curr_height]
        
        # print (num_col)
        # print (col_gen_limit_list)
        # print (col_curr)
        # print()
        
        if not (col_curr in col_gen_limit_list):    return False
        
    return True


def genRowDown(board_curr, num_row):
    #check row > 5
    if num_row >= 5: return board_curr
    row_state_list = genState(row_constraint_init[num_row])      #[[]]
    
    for row_state_child in row_state_list:                  #   []
        board_curr[num_row] = row_state_child                #   [[]]
        if checkBoard(board_curr):
            return genRowDown(board_curr, num_row + 1)
        else:
            # if num_row >= 4: print('no solution'); return []
            continue
        # check valid
        # print(board_curr)
    
def draw(boardMatrix):
    # m_print = []
    print('#: filled cell\t\t-: empty cell\t\tx: haven\'t visited yet')
    for i in boardMatrix:
        # row  = list (map (lambda x: print ('\t#') if x == 1 else print ('\tx') if x == -1 else print ('\t-'),i))
        row  = list (map (lambda x: '\t#' if x == 1 else '\tx' if x == -1 else '\t-',i))
        print(*row)
        
################################################################################
def preTravel(board_curr, isRow = True, notChange = 0):
    if notChange >= 2:
        return board_curr
    
    constraint = row_constraint_init
    if not (isRow):
        board_curr = transposeM(board_curr)
        constraint = column_constraint_init
    # notChange = 0
    
    changeLocal = False
    for i in range(size):
        if isRow and lineLock['row'][i] == 1: continue
        if lineLock['column'][i] == 1: continue
        
        if isRow:
            board_curr[i] = fillPartialOf_Row(board_curr[i], row_constraint_init[i], i)
        else:
            board_curr[i] = fillPartialOf_Col(board_curr[i], column_constraint_init[i], i)
        
        merge_LineMatrix_Lock()
        
        if isUnique(constraint[i]):
            # print(genState(constraint[i]))
            board_curr[i] = genState(constraint[i])[0]
            if isRow:
                lineLock['row'][i] = 1
            else:
                lineLock['column'][i] = 1
            changeLocal = True
            continue
 
    notChange = 0 if changeLocal else notChange + 1
    # if notChange >= 2:
    #     return board_curr
    
    if not (isRow):
        board_curr = transposeM(board_curr)

    return preTravel(board_curr, not(isRow), notChange)



#   done sub2 for row
def fillPartialOf_Row(line_Curr, constraint, line_Num):
    stateList = genState(constraint)
    
    state_Transpost = transposeM(stateList)
    
    sumState = list(map(lambda x: sum(x), state_Transpost))

    for i in range(size):
        if sumState[i] == len(stateList):
            line_Curr[i] = 1
            board_isLock[line_Num][i] = 1
            
    
    return line_Curr



def fillPartialOf_Col(line_Curr, constraint, line_Col):
    stateList = genState(constraint)
    state_Transpost = transposeM(stateList)
    sumState = list(map(lambda x: sum(x), state_Transpost))
    
    for i in range(size):
        if sumState[i] == len(stateList):
            line_Curr[i] = 1
            board_isLock[i][line_Col] = 1
    
    return line_Curr


def genRowHeuristic(board_curr, num_row = 0):
    # print ('enter row: ',num_row,'th')
    print ('-----------------------------\trow: ',num_row,'th')
    draw (board_curr)
    
    if num_row >= 5: return board_curr
    
    if lineLock['row'][num_row] == 1:
        print ('row ',num_row,' is generated, continue to row ',num_row + 1)
        return genRowHeuristic(board_curr, num_row + 1)
    
    # count = sum(map(lambda x : x%2 == 1, listOfElems))

    if (sum(map(lambda x: x==1, board_curr[num_row])) == num_BlackInRow[num_row]):
        print ('row ',num_row,' have enought black cell, continue to row ',num_row + 1)
        board_curr[num_row] = list(map(lambda x: 1 if x == 1 else 0, board_curr[num_row]))
        lineLock['row'][num_row] = 1
        merge_LineMatrix_Lock()
        return genRowHeuristic(board_curr, num_row + 1)
        
    board_queue = []
  
    row_state_list = genState(row_constraint_init[num_row])      #[[]]    
    for row_state_child in row_state_list:                  
        print ('check state ',row_state_child)
        if isSameLine(board_curr[num_row], row_state_child) == False:
            continue
        board_curr[num_row] = row_state_child                
        if checkBoard(board_curr):
                       
            # return genRowHeuristic(board_curr, num_row + 1)
            board_queue += [(board_curr, heuristicFunc(board_curr))]
        else:
            # if num_row >= 4: print('no solution'); return []
            continue
    
    def f(e):
        return e[1]
    board_queue.sort(reverse=True, key=f)
    
    for i in board_queue:
        return genRowHeuristic(i[0], num_row + 1)
    
def heuristicFunc(board_curr):
    tmp_matrix = transposeM(board_curr)
    # ratio_Completed = [sum(tmp_matrix[0: num_row +1 ])]
    
    
    # n_Completed = [sum(tmp_matrix[i] for i in range(size))]
    n_Completed = []
    ratio = 0
    for i in range(size):
        n_Completed += [sum(map(lambda x: x==1, board_curr[i]))]
        # s += [sum(map(lambda x: x==1, a[i]))]
        ratio += n_Completed[i] / num_BlackInCol[i]
    
    return ratio


def merge_LineMatrix_Lock():
    # update matrix based on lineLock
    for i in range(size):
        if lineLock['row'][i] == 1:
            for j in range(size):
                board_isLock[i][j] = 1
    for i in range(size):
        if lineLock['column'][i] == 1:
            for j in range(size):
                board_isLock[j][i] = 1

    # update LineLock
    for i in range(size):
        if sum(board_isLock[i]) == 5:
            lineLock['row'][i] = 1
    for colNum in range(size):
        tmp_sum = 0
        for rowNum in range(size):
            if board_isLock[rowNum][colNum] == 1: tmp_sum += 1
        if tmp_sum == size:
            lineLock['column'][colNum] = 1

def transposeM (m):
    arr = np.array(m)
    board_trans = arr.transpose()
    board_trans = board_trans.tolist()
    return board_trans

def isUnique(constraint):
    return len(constraint) == 3 or len(constraint) == 0 or (sum(constraint) == 4 and len(constraint) == 2) or constraint == [[5]]
        
def isSameLine(line_Curr, line_Expected): # []
    for i in range(size):
        if line_Curr[i] == -1: continue
        if line_Curr[i] != line_Expected[i]:
            return False
    return True

# def isSameLine_CheckColConstraint(line_Curr): # []
#     for i in range(size):
#         if line_Curr[i] == -1: continue
#         if line_Curr[i] != line_Expected[i]:
#             return False
#     return True

stime = time.time()
tracemalloc.start()


size = 5

column_constraint_init = [[1,1],[1],[2],[2,2],[4]]   #   top of board, from L to R
row_constraint_init = [[1,3],[3],[1],[2],[2,1]]      #   left of board, form top to down

num_BlackInRow = [sum(x) for x in row_constraint_init]
num_BlackInCol = [sum(x) for x in column_constraint_init]


# column_constraint_init = [[1],[2,2],[3],[4],[1]]
# row_constraint_init = [[2],[1,1],[2],[4],[3]]


board=[]
board_init =    [[-1 for i in range(size)] for i in range(size)]


board_isLock =  [[0 for i in range(size)] for i in range(size)]
lineLock =  {   'row':      [0 for i in range(size)],
                'column':   [0 for i in range(size)]
            }

board_SpecialCase = preTravel(board_init)

        
# print (board_SpecialCase)
draw (board_SpecialCase)

result = genRowHeuristic(board_SpecialCase, 0)

draw (result)

# print (genRowDown(board_init, 0))


etime = time.time()
# print_grid(gr)
print('Solved in ', (etime - stime),' seconds')
print('The solving function has been called times')
print('Memory usage ',tracemalloc.get_traced_memory())
tracemalloc.stop()