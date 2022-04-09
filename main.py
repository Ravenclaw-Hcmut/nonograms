#   Huynh Tan Luan          1914054
#   Nguyen Thanh Luu        1914084
#   Nguyen Tran Quoc Uy     1915xxx

from asyncio import constants
from os import curdir

from matplotlib.cbook import print_cycles
from sympy import N, false, true

import numpy as np

# def isContain(child, parrent):
#     for i in range(len(child)):
#         if child[i] == -1:          return true
#         if child[i] != parrent[i]:  return false
#     return true

size = 5

column_constrain_init = [[1,1],[1],[2],[2,2],[4]]   #   top of board, from L to R
row_constrain_init = [[1,3],[3],[1],[2],[2,1]]      #   left of board, form top to down


# column_constrain_init = [[1],[2,2],[3],[4],[1]]
# row_constrain_init = [[2],[1,1],[2],[4],[3]]


board=[]
board_init = [[-1 for i in range(size)] for i in range(size)]


def genState(constrain): # [1,3]
    if len(constrain) == 0:
        return [[0,0,0,0,0]]
    if len(constrain) == 3:
        return [[1,0,1,0,1]]
    
    if len(constrain) == 1:
        num = constrain[0]
        
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
        
    if len(constrain) == 2:
        l = constrain[0]
        r = constrain[1]
        
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
        
            
# for i_row in range(len(row_constrain_init)):
#     tmp_rowState = genState(row_constrain_init[i_row])
#     print(tmp_rowState[0])
    
#     break

# list_row0_state = genState(row_constrain_init[0])
# for row0_state in list_row0_state:
#     print (row0_state)
#     list_row1_state = genState(row_constrain_init[1])
#     for 

def checkBoard(board_curr):
    if board_curr[0][0] == -1:
        return true
    
    #count current height
    curr_height = 0
    for num_row in range(len(board_curr)):
        if board_curr[num_row][0] == -1:
            break
        curr_height += 1
        
    ## checkrow
    for num_row in range(len(board_curr)):
        if board_curr[num_row][0] == -1:
            # return true
            break
        if not (board_curr[num_row] in genState(row_constrain_init[num_row])):
            return false
        # print ('done row ',num_row)
        
    # check column
    arr = np.array(board_curr)
    board_trans = arr.transpose()
    board_trans = board_trans.tolist()
    
    for num_col in range(len(board_trans)):
        # col_gen_limit_list = [a[:curr_height] for a in genState(column_constrain_init[num_col])]
        
        col_gen_limit_raw = genState(column_constrain_init[num_col])        # [[]]
        
        col_gen_limit_list = [a[:curr_height] for a in col_gen_limit_raw]
        
        col_curr = board_trans[num_col][:curr_height]
        
        # print (num_col)
        # print (col_gen_limit_list)
        # print (col_curr)
        # print()
        
        if not (col_curr in col_gen_limit_list):    return false
        
    return true


    
                        # def genRowDown(board_curr, num_row):
                        #     #check row > 5
                            
                        #     row_state_list = genState(row_constrain_init[num_row])  
                            
                        #     for row_state_child in row_state_list:                  #   []
                        #         board_curr[num_row] = row_state_child                #   [[]]
                                
                        #         # check valid
                        #         print(board_curr)
                        #     # print (row_state)7

def genRowDown(board_curr, num_row):
    #check row > 5
    if num_row >= 5: return board_curr
    row_state_list = genState(row_constrain_init[num_row])      #[[]]
    
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
        
        
# draw (genRowDown(board_init, 0))
print (genRowDown(board_init, 0))



