#!/usr/bin/env python
import os,sys
import copy
import random
MIN=-99999999  
MAX=+99999999 
diff=[]
N = int(sys.argv[1])
moves=[]
for i in range(N):
	moves.append(i)
## CHECKS IF BOARD IS FULL
def isboardfull(board):
	flag=0
	for i in range(N+3):
		for j in range(N):
			if board[i][j]!='.':
				flag=1
	if flag==0:
		return True
	else:
		return False
## STATE CREATION WITH DROPPING PEBBLE IN COLUMN COL
def col_move(player,board,col): 
	empty_row=isFullFetch(board,col)  ##USES isFullFetch TO FETCH THE VACANT POSITION OR TELLS IF THE COLUMN IS FULL
	if(empty_row==-1):  ## NO EMPTY ROW
		return 0
	temp_board=copy.deepcopy(board)
	
	if(player=='H'):
			temp_board[empty_row][col]='o'
	else:
			temp_board[empty_row][col]='x'
	return temp_board
##USED TO CHECK IF CURRENT PLAYER WON IN ANY DIAGONAL(LEFT OR RIGHT)
def check_diag(player,board): 
	temp_board=copy.deepcopy(board)
	temp_board.reverse()
	a=None
	if(player=='H'):
		a='o'
	else:
		a='x'
	##LEFT DIAGONAL
	flag_l=0
	for i in range(N):
		for j in range(N):
			if(i==j):
				if(temp_board[i][j]!=a):
					flag_l=1
	if(flag_l==0):
		return True
	##RIGHT DIAGONAL
	temp_c=0
	flag_r=0
	for j in range((N-1),-1,-1):
			if(temp_board[j][temp_c]!=a):
				flag_r=1
			temp_c+=1
	if(flag_l==0 or flag_r==0):
		
		return True
	else:
	
		return False
##USED TO CHECK IF CURRENT PLAYER WON IN ANY ROW
def check_row(player,board):
	temp_board=copy.deepcopy(board)
	temp_board.reverse()
	a=None
	if(player=='H'):
		a='o'
	else:
		a='x'


	flag=0
	for i in range(N):
		for j in range(N):
			if temp_board[i][j]!=a:
				flag=1
		if(flag==0):
			return True
			break
		flag=0
	return False

## USED TO CHECK IF CURRENT PLAYER WON IN ANY COLUMN
def check_col(player,board):
	temp_board=copy.deepcopy(board)
	temp_board.reverse()
	a=None
	if(player=='H'):
		a='o'
	else:
		a='x'
	flag=0
	for i in range(N):
		for j in range(N):
			if temp_board[j][i]!=a:
				flag=1
		if(flag==0):
			return True
			break
		flag=0
	return False
## USED TO RETURN WHICH ROW AT PARTICULAR COLUMN IS EMPTY TO DROP/ADD PEBBLE AT
def isFullFetch(board,col):
	flag=0
	for i in range(N+3):
		if board[i][col]=='.':
			return i ## returns which row at Column 'col' is an empty space
			flag=1
	if(flag==0):
		return -1
##USED TO KEEP TRACK OF STATES IN THE FINAL EXECUTION
def which_col_changed(changed, initial):
  for i in range(0,len(initial)):
    if changed[i] != initial[i]:
      return i+1
##USED TO CHECK IF NO. OF PEBBLES(O OR X) IS GREATER THAN (NX(N+3)/2)
def check_max_marbles(board):
	for i in range(N+3):
		t=sum([1 for item in board[i] if item==current_player])
	if(t>(N*(N+3))/2):
		return 0
	return 1
## USED TO CHECK CASES WHERE ROTATE RETURNS THE PARENT NODE AGAIN
def norotate(board,col):
	t_current=0
	t_opponent=0
	t_current=sum([1 for item in board[:N+3] if item[col]==current_player])
	t_opponent=sum([1 for item in board[:N+3] if item[col]==opponent])
	if(t_current>0 and t_opponent==0):
		return 0
	if(t_opponent>0 and t_current==0):
		return 0
	return 1

##CREATES SUCCESSORS WITH ROTATIONS
def rotate(board,col):
	if(board[0][col]=='.'):
		return -1
	temp_board=copy.deepcopy(board)
	if board[0][col]!='.':
		temp=board[0][col]
	if board[N+2][col]!='.':
		for i in range(N+2):
			temp_board[i][col]=temp_board[i+1][col]
		temp_board[N+2][col]=temp
	else:	
		for i in range(N+3):

			if(temp_board[i][col]=='.'):
				break
			temp_board[i][col]=temp_board[i+1][col]
		temp_board[i-1][col]=temp
	return temp_board
##RETURNS HOW MANY BLANK SPACES IN BOARD LATER TO BE USED IN EVALUATION FUNCTION(NOT USED EVENTUALLY)
def how_many(board):
	temp=copy.deepcopy(board)
	temp.reverse()
	counter=0
	for i in range(N+3):
		for j in range(N):
			if(temp[i][j]=='.'):
				counter+=1
	return counter
## USED TP PRINT BOARD IN HUMAN READABLE FORM(NOT USED)
def print_board(b):
   temp=copy.deepcopy(b)
   temp.reverse()
   print("\n".join([ " ".join([ "o" if element=='o' else "x" if element=='x' else "." if element=='.' else ""  for element in item ]) for item in temp]))

##FUNCTION FOR STATE GENERATION
def states(b,which):
	state=[]
	rows=len(b)
	cols=rows-3
	f=random.sample(moves,3)
	
	for i in f:
		t=rotate(b,i)
		w=norotate(b,i)
		if(t!=-1 and w==1):
			state.append(t)
	counter=1	
	for i in f:
		t=col_move(which,b,i)
		if(t!=0 and check_max_marbles(t)):
			state.append(t)
	return state
##FUNCTION TO CHECK HOW MANY CURRENT PLAYER PEBBLES ARE THERE IN BOTTOM ROW WHICH COULD BE ROTATED IN FUTURE AND BROUGHT UP(USED IN HEURISTIC)
def bottom(player,board):
	a=None
	if(player=='H'):
		a='o'
	else:
		a='x'
	bot=0
	for i in range(N):
		if board[0][i]==a:
			bot+=1
	return bot
## EVALUATES NO. OF WAYS THE CURRENT PLAYER CAN WIN IN A GIVEN BOARD(i.e, rows,cols,diags where the current player could still win)
def eval(player,board):
	counter=0
	
	temp_board=copy.deepcopy(board)
	temp_board.reverse()
	## ROW CHECK
	for i in range(N):
		t=sum([1 for item in temp_board[i] if item==player])
		if(t==0):
			counter+=1
	
	## COLUMN CHECK
	for i in range(N):
		t=sum([1 for item in temp_board[:N ]if item[i]==player])
		if(t==0):
			counter+=1
	## LEFT DIAG CHECK
	flag_l=0
	for i in range(N):
		for j in range(N):
			if(i==j):
				if(temp_board[i][j]==player):
					flag_l=1
	if(flag_l==0):
		counter+=1
	
	## RIGHT DIAG CHECK
	temp_c=0
	flag=0
	for j in range((N-1),-1,-1):
			if(temp_board[j][temp_c]==player):
				flag=1
			temp_c+=1
	if(flag==0):
		counter+=1
	return counter
## EVALUATION FUNCTION SENDS AN ADDITION OF NO. OF WAYS CURRENT PLAYER CAN WIN + NO. OF PEBBLES IN BOTTOM ROW(CURRENT PLAYERS' PEBBLES)
def evaluate(player,board):
	counter=0
	if(player=='H'):
		a=eval('x',board)
		
		b=eval('o',board)
	
	else:
		a=eval('o',board)
		b=eval('x',board)
	counter=a-b
	bot=bottom(player,board)
	counter1=(counter)+(bot)
	if (check_col(player,board)) or (check_row(player,board)) or (check_diag(player,board)):
		 if(player==pl):
			return 60+counter1
		 else:
		    return (-60-counter1)
	if(isboardfull(board)):
		return counter1
	return counter1
		

## TO CHECK IF CURRENT BOARD/NODE IS GOAL NODE
def isterminal(player,board):
	if(check_col(player,board) or check_diag(player,board) or check_row(player,board)):
		return True
	else:
		return False
	
## MINI MAX ALGORITHM USING APLHA BETA PRUNING
def minimax(node,depth,maxmizingPlayer,alpha,beta): ## https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/
		
		if(maxmizingPlayer):
			a=op
		else:
			a=pl
		if(isterminal(a,node) or depth==30):
			
			score=evaluate(a,node)
			
			if(maxmizingPlayer):
				if(isterminal(a,node)):
					return (depth+score)
				else:
					return(score)
				
			else:
				
				
				if(isterminal(a,node)):
					return (score-depth)
				else:
					return score



		if maxmizingPlayer:
			bestvalue=MIN
			child_nodes=states(node,pl)
			for child in child_nodes:
				v=minimax(child,depth+1,False,alpha,beta)
				
				if(v>alpha):
					alpha=v
				if(alpha>=beta):
					return alpha
				return alpha
		
		else:
			bestvalue=MAX
			child_nodes_1=states(node,op)
			for child in child_nodes_1:
				v=minimax(child,depth+1,True,alpha,beta)
				if(v<beta):
					beta=v
				if(alpha>=beta):
					return beta
				return beta
				
## USED TO KEEP TRACK OF MOVES
def check_which_move_best(move_dict): ## Reffered from Aravin Parappil
    best_state_after_move = move_dict[max(move_dict.keys())]

    # Find those rows which are different from initial state
    for i in range(0,len(best_state_after_move)):
        if best_state_after_move[i] != initial_board[i]:
            diff.append((best_state_after_move[i], initial_board[i]))

    # If drop move, then only one row would have been changed 
    if len(diff) == 1:
        return which_col_changed(diff[0][1],diff[0][0]), best_state_after_move

    # If not, then a rotate happened
    else:
        return -which_col_changed(diff[0][1],diff[0][0]), best_state_after_move

## STARTING FUNCTION CALL WITH INITIAL BOARD
def bestmove(initial):
	
	fin=[-99,-99,-99]
	index=[]  
	for i in range(N):  ## for cases where column drop can't be done as column in full
		if isFullFetch(initial,i)==-1:
			index.append(i) 
	child_nodes=states(initial,pl)
	val=[]
	for child in child_nodes:
		moveval=minimax(child,0,False,MIN,MAX)

		
		val.append((moveval))
	print(val)
	move_dict = dict(zip(val, child_nodes))
	print(move_dict)
	best_move,best_board=check_which_move_best(move_dict)
	return moveval,val,best_move,best_board

current_player = sys.argv[2]
string_board = sys.argv[3]
time_limit = int(sys.argv[4])
initial = [[0]*(N) for i in range(N+3)]
k=0
for i in range(0,N+3):
    for j in range(0,N):
        initial[i][j] = string_board[k]
        k+=1
initial.reverse()
initial_board=copy.deepcopy(initial)
if(current_player=='o'):
		pl='H'
		op='C'
		opponent='x'
else:
		pl='C'
		op='H'
		opponent='o'


m,v,best_move,best_board = bestmove(initial_board) ## FIRST CALL TO BESTY PROGRAM HERE
if best_move > 0:
    print "\n","You should drop a pebble in column", best_move
else:
    print "\n","I'd recommend you rotate column", abs(best_move)

print('\n')

best_board.reverse()
s = ""
for i in range(N+3):
  for j in range(N):
    s+=str(best_board[i][j])
print best_move,"",s








