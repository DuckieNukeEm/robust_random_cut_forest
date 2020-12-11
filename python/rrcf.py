
# Building Isolation tree in Python

import pandas as pd
import numpy as np
import random as rd

def iTree(df: pd.DataFrame, l: int, e: int = 0) -> dict:
    """Recursivley builds an iTree from a DataFrame
    df = the data
    e = current depth
    l = max depth"""
    if df.shape[0] <= 1 or e >= l:
        return {'NodeType' : 'External',
               'Left' : None,
               'Right' :  None,
               'SplitAtt' : None,
               'SplitVal' : None,
               'Size' : df.shape[0],
               'Depth' : e}
    else:
        q = rd.randint(0,df.shape[1] - 1) #stupid counting at zero *mumble mumble mumble*
        p = np.random.uniform(low = df.iloc[:,q].min(), high = df.iloc[:,q].max())
        return {'NodeType': 'Internal',
               'Left' : iTree(df[df.iloc[:,q] < p], l, e + 1),
               'Right' : iTree(df[df.iloc[:,q] >= p], l, e + 1), 
               'SplitAtt' : q,
               'SplitVal' : p,
               'Size': df.shape[0],
                'Depth' : e
               }

def USS(n: int) -> int:
    """average path length of unsuccessful search in BST"""
    if n < 2:
        return 0
    elif n == 2:
        return 1
    else:
        return (2.0 * (np.log(n - 1.0) + 0.5772156649) + 2.0 * (n - 1.0)/n)


def iForest(df: pd.DataFrame, nt: int , phi: int) -> dict:
    """builds an iForest from a data set. nt is the number of iTree's to
    build, and phi is the sample size"""
    Forest = [None] * nt
    depth = np.ceil(np.log(phi))
    for i in range(nt):
        sub_sample = np.random.choice(df.index, phi)
        Tree = iTree(df.iloc[sub_sample,:], l = depth)
        Forest[i] = Tree
    return Forest


def PathLength(pnt: pd.Series, Tree: dict, l: int) -> int:
	""" Get Path length of a data point through tree (non recursive)"""
	trvls = 0
	pnt = pnt.values
	
	while(trvls < l ):
		if Tree['NodeType'] == 'External' or trvls == (l-1):
			trvls += USS(Tree['Size'])
			break
	
		trvls += 1
		if pnt[Tree['SplitAtt']] < Tree['SplitVal']:
			Tree = Tree['Left']
		else:
			Tree = Tree['Right']
	if trvls == l:
		trvls += USS(
	return(trvls)


def ForestPathLenth(pnt: pd.Series, Forest: 'iForest', l: int) -> int:
	"""takes a forest and a point, and finds the aggregated path length"""
	PL = 0
	for T in range(len(Forest)):
		PL += PathLength(pnt, Forest[T], l)
	PL = PL/len(Forest)
	
	return(PL)
  
def predict_iForest(df: pd.DataFrame, Forest: 'iForest', phi: int, l: int = None) -> pd.Series:
	"""Takes an iForest and a DataFrame, and computes an anomoly score for each point"""
	if l is None:
		l = np.ceil(np.log(phi))
			
	PL = pd.Series(0, index = range(df.shape[0]))
	PL = df.apply(lambda x: ForestPathLenth(x, Forest, l), axis = 1)
	PL = np.power(2, -1 * PL/USS(phi))
	return(PL)


def get_columns_labels(df: pd.DataFrame) -> list:
	"""gets a list of column names to make printing variables easier"""
	col_list = df.columns.values
	return(col_list)

    
def Print_iTree(Tree, Direction = None, col_labs):
    "pretty prints an iTree"
    #getting number of indents
    Prnt_str = ' ' * Tree['Depth'] + 'Depth: ' + str(Tree['Depth'])
    if Direction != None:
        Prnt_str = Prnt_str + ' (' + Direction + ')'
    if Tree['NodeType'] == 'External':
        Prnt_str = Prnt_str + ' - External Node - (' + str(Tree['Size']) + ')'
        print(Prnt_str)
    else:
        Prnt_str = Prnt_str + ' - Split Var: ' +  str(col_labs[Tree['SplitAtt']]) + ' at ' + str(round(Tree['SplitVal'],4))
        Prnt_str = Prnt_str + ' True: ' + str(round(Tree['Left']['Size']/(Tree['Size'] * 1.000),2) * 100) + '%'
        Prnt_str = Prnt_str + ' (' + str(Tree['Size']) + ')'
        print(Prnt_str)
        Print_iTree(Tree['Left'], 'Left')
        Print_iTree(Tree['Right'], 'Right')
