import functools
from functools import reduce
import sys

# This is demonstrating a class implementation of AC3. You can accomplish the same with lists. For the project, you can choose either.

# The primary problem set-up consists of "variables" and "constraints":
#   "variables" are a dictionary of constraint variables (of type ConstraintVar), example variables['A1']
#   "constraints" are a set of binary constraints (of type BinaryConstraint)

# First, Node Consistency is achieved by passing each UnaryConstraint of each variable to nodeConsistent().
# Arc Consistency is achieved by passing "constraints" to Revise().
# AC3 is not fully implemented, Revise() needs to be repeatedly called until all domains are reduced to a single value 

class ConstraintVar:
	# instantiation example: ConstraintVar( [1,2,3],'A1' )
	# MISSING filling in neighbors to make it easy to determine what to add to queue when revise() modifies domain
    def __init__(self, d, n ):
        self.domain = [ v for v in d ]
        self.name = n
        self.neighbors = []

class UnaryConstraint:
    # v1 is of class ConstraintVar
    # fn is the lambda expression for the constraint
    # instantiation example: UnaryConstraint( variables['A1'], lambda x: x <= 2 )
    def __init__(self, v, fn):
        self.var = v
        self.func = fn

class BinaryConstraint:
	# v1 and v2 should be of class ConstraintVar
	# fn is the lambda expression for the constraint
	# instantiate example: BinaryConstraint( A1, A2, lambda x,y: x != y ) 
    def __init__(self, v1, v2, fn):
        self.var1 = v1
        self.var2 = v2
        self.func = fn


def allDiff( constraints, v ):    
	# generate a list of constraints that implement the allDiff constraint for all variable combinations in v
	# constraints is a preconstructed list. v is a list of ConstraintVar instances.
	# call example: allDiff( constraints, [A1,A2,A3] ) will generate BinaryConstraint instances for [[A1,A2],[A2,A1],[A1,A3] ...
    fn = lambda x,y: x != y
    for i in v:
        for j in v:
            if ( i != j ) :
                constraints.append(BinaryConstraint( i,j,fn ))
    
def setUpKenKen( variables, constraints ):
    # This setup is applicable to KenKen and Sudoku. For this example, it is a 3x3 board with each domain initialized to {1,2,3}
    # The VarNames list can then be used as an index or key into the dictionary, ex. variables['A1'] will return the ConstraintVar object

    # Note that I could accomplish the same by hard coding the variables, for example ...
    # A1 = ConstraintVar( [1,2,3],'A1' )
    # A2 = ConstraintVar( [1,2,3],'A2' ) ...
    # constraints.append( BinaryConstraint( A1, A2, lambda x,y: x != y ) )
    # constraints.append( BinaryConstraint( A2, A1, lambda x,y: x != y ) ) ...
    #   but you can see how tedious this would be.
    
    # Create variable names. Create a variable with domain [1,2,3] for each
    # Place each variable in a dictionary, indexed by name (e.g. "A1")
    rows = ['A','B','C']
    cols = ['1','2','3']
    varNames = [ x+y for x in rows for y in cols ]
    for var in varNames:
        variables[var] = ConstraintVar( [1,2,3],var )
    
    # establish the allDiff constraint for each column and each row
    # for AC3, all constraints would be added to the queue 
    
    # for example, for rows A,B,C, generate constraints A1!=A2!=A3, B1!=B2...   
    for r in rows:
        aRow = []
        for k in variables.keys():
            if ( str(k).startswith(r) ):
		#accumulate all ConstraintVars contained in row 'r'
                aRow.append( variables[k] )
	#add the allDiff constraints among those row elements
        allDiff( constraints, aRow )
        
    # for example, for cols 1,2,3 (with keys A1,B1,C1 ...) generate A1!=B1!=C1, A2!=B2 ...
    for c in cols:
        aCol = []
        for k in variables.keys():
            key = str(k)
            # the column is indicated in the 2nd character of the key string
            if ( key[1] == c ):
		# accumulate all ConstraintVars contained in column 'c'
                aCol.append( variables[k] )
        allDiff( constraints, aCol )

#--------------------------------------------------------------------------------------------
#########################            COMPLETE REVISE               ##########################

def Revise( bc ):
	# The Revise() function from AC-3, which removes elements from var1 domain, if not arc consistent
	# A single BinaryConstraint instance is passed in to this function. 
	# MISSSING the part about returning sat to determine if constraints need to be added to the queue
	
    # copy domains for use with iteration (they might change inside the for loops)
    '''
    dom1 = list(bc.var1.domain)
    print("dom1 is: "+str(dom1))
    dom2 = list(bc.var2.domain)
    print("dom2 is: "+str(dom2))
    
    revised = False
    # for each value in the domain of variable 1
    for x in dom1:
#>>>>   
        noMatch = True
        # for each value in the domain of variable 2
        for y in dom2:
#           print(str(x)+' '+str(y))
            if (bc.func(int(x),int(y))):
                print(str(bc.var1.name)+' '+str(x)+' '+str(bc.var2.name)+' '+str(y))
                noMatch = False
                break
        if noMatch == True:        
            print(str(bc.var1.name)+' removed '+str(x))
            if len(bc.var1.domain) != 1:
                bc.var1.domain.remove(x)
                revised = True
    '''
    dom1 = list(bc.var1.domain)
    dom2 = list(bc.var2.domain)
    revised=False
    for x in dom1:
	    delete_x=True
	    for y in dom2:
		if (bc.func(x, y)):
                    delete_x=False
	    if (delete_x):
                bc.var1.domain.remove(x)
                revised=True
    return revised
#>>>>>            
        # if nothing in domain of variable2 satisfies the constraint when variable1==x, remove x
#>>>>>
        
def nodeConsistent( uc ):
    domain = list(uc.var.domain)
    for x in domain:
        if ( False == uc.func(x) ):
            print(str(uc.var.name)+' removed unary '+str(x))
            uc.var.domain.remove(x)

def printDomains( vars, n=3 ):
    count = 0
    for k in sorted(vars.keys()):
        print( k,'{',vars[k].domain,'}, ',end="" )
        count = count+1
        if ( 0 == count % n ):
            print(' ')
        
def tryAC3( ):
    
    # create a dictionary of ConstraintVars keyed by names in VarNames.
    variables = dict()
    constraints = []
    setUpKenKen( variables, constraints)
    
    #print("initial domains")
    #printDomains( variables )

    nodeConsistent( UnaryConstraint( variables['A3'], lambda x: x==2 ) )
    #print("unary constraint A3")
    #printDomains( variables )
    
    ######          FILL IN REST OF BINARY CONSTRAINTS. NOTE that they need to be reciprocal A!=B, as well as B!=A
    constraints.append( BinaryConstraint( variables['A1'], variables['A2'], lambda x,y: abs(x-y) == 2 ) )
    constraints.append( BinaryConstraint( variables['A2'], variables['A1'], lambda x,y: abs(x-y) == 2 ) )
    constraints.append( BinaryConstraint( variables['B1'], variables['C1'], lambda x,y: abs(x/y) == 2 ) )
    constraints.append( BinaryConstraint( variables['C1'], variables['B1'], lambda x,y: abs(x/y) == 2 ) )
    constraints.append( BinaryConstraint( variables['B2'], variables['B3'], lambda x,y: abs(x/y) == 3 ) )
    constraints.append( BinaryConstraint( variables['B3'], variables['B2'], lambda x,y: abs(x/y) == 3 ) )
    constraints.append( BinaryConstraint( variables['C2'], variables['C3'], lambda x,y: abs(x-y) == 1 ) )
    constraints.append( BinaryConstraint( variables['C3'], variables['C2'], lambda x,y: abs(x-y) == 1 ) )

    Cnt = 0
    for c in constraints:
        print("constrain var1: "+c.var1.name+", constrain var2: "+c.var2.name+", constrain func: "+str(c.func))
        Revise( c )
        Cnt += 1
        if Cnt >= 5:
            sys.exit(1)
    #print("all constraints pass 1")
    printDomains( variables )
    
    for c in constraints:
        Revise( c )
    #print("all constraints pass 2")
    printDomains( variables )

    for c in constraints:
        Revise( c )

    result = []
    for key, value in variables.items():
        print( key, value.domain)
        if len(value.domain) > 1:
            return False
        result.append([key, value.domain])
    return result

def help() :

    print('----------------------------------------------------------')
    print('TO DO:')
    print('1) Write the function revise().')
    print('2) Complete the binary constraints for KenKen puzzle.')
    print('3) Modify tryAC3 to return solution as list of rows and remove all the print statements.')
    print('4) Ensure that we can run a script that imports AC3starter.py and can call solveKen')
    print('5) Run code and confirm that all domains are reduced to single value.')
    print('')
    print('OPTIONAL for bonus points ...') 
    print('Create the variables and constraints for the sport logic puzzle.')
    print('-- Do not hand edit the domains based on Unary constraints. Define those as part of the puzzle.')
    print('Solve the puzzle using nodeConsistent() and revise().')
    print('OTHER BONUS option ... Implement neighbors')

    print(' IF you finish all of that, see if you can frame the person-animal-color puzzle for AC3 for fun')

    print('NOTE, the implementation of AC3 requires a queue on which you pop a constraint, then push neighbors if necessary')
    print('   Since this is not implemented here, you can create a "hack" by repeatedly calling Revise.')


def solveKen():
    kenken = [
        ['-', 2, ['A1','A2']],
        ['abs',2,['A3']],
        ['/',2,['B1','C1']],
        ['/',3,['B2','B3']],
        ['-',1,['C2','C3']]
        ]
    return tryAC3()

def solveLogic():
    return None

if __name__ == "__main__":
    solveKen()
        
    

    
    



