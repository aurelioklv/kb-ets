import networkx as nx
import random


#NOTE : Harus python 3.10+ karena pakai "match case"


#Domain sets :
    #1. Forest, USED FOR INITIAL TESTING
    #   "entry" : "neutral"
    #   "long"  : "road", "river", "ravine"
    #   "3x3"   : "clearing", "forest", "camp", "lake"

#Constraints :
#NEXT TO ONE ANOTHER
#CAN'T BE NEXT TO EACH OTHER

#TODO : Integrate the code with networkx graph?


# REF : https://freecontent.manning.com/constraint-satisfaction-problems-in-python/
#START
from typing import Dict, List, Optional, TypeVar, Generic
from abc import ABC, abstractmethod

V = TypeVar('V')
#Variabel berupa node dalam graph networkx yang disimpan dalam list
D = TypeVar('D')
#Domain dihardcode berupa dictionary yang terdiri dari ["tipe node", List["Kemungkinan domain/tipe"]]
#Setiap variabel diberi domain saat program dijalankan sesuai tipe yang diinginkan pengguna
R = TypeVar('R', str, bool)
#Return value dari constraint bisa bool (binary) atau str (preference)


# Base class for all constraints
class Constraint(Generic[V, D], ABC):
    # The variables that the constraint is between
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    # Must be overridden by subclasses
    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> R:
        ...

    # A constraint satisfaction problem consists of variables of type V
    # that have ranges of values known as domains of type D and constraints
    # that determine whether a particular variable's domain selection is valid



class CSP:
    def __init__(self, variables: List[V], types: Dict[V, V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables  # variables to be constrained
        self.types: Dict[V, V] = types #Tipe dari node
        self.domains: Dict[V, List[D]] = domains  # domain of each variable
        self.constraints: Dict[V, List[Constraint]] = {}
        self.prefConstraint: Dict[V, List[Constraint]] = {}


        for variable in self.variables:
            self.constraints[variable] = []
            self.prefConstraint[variable] = []
            if not self.domains[int(variable)]:
                raise LookupError("Every variable should have a domain assigned to it.")

    def add_constraint(self, constraint: Constraint) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def add_preference(self, constraint: Constraint) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.prefConstraint[variable].append(constraint)

    #Fungsi untuk preference constraint (ori)
    def preference(self, variable: V, assignment: Dict[V, D]) -> D:
        for constraint in self.prefConstraint[variable]:
            return constraint.satisfied(assignment, self.types)



    # Check if the value assignment is consistent by checking all constraints
    # for the given variable against it


    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True


    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        # assignment is complete if every variable is assigned (our base case)
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables in the CSP but not in the assignment
        unassigned: List[V] = [v for v in self.variables if v not in assignment]

        # get the every possible domain value of the first unassigned variable
        first: V = unassigned[0]

        #MOD : Change value selection from first on list to --> 1. Random OR 2. Least Constraining Value
        for value in self.domains[int(first)]:
            local_assignment = assignment.copy()
            prefered_value = self.preference(first, local_assignment)
            if prefered_value is not None:
                local_assignment[first] = prefered_value
            else:
                local_assignment[first] = value
            # if we're still consistent, we recurse (continue)
            if self.consistent(first, local_assignment):
                result: Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
        return None

# Constraints sesuai abstract class
# NOTE :
# Saat ini : Contraint deklarasi antar 2 variabel
# TODO : Constraint deklarasi untuk 1 node, otomatis memeriksa untuk semua neighbour node menggunakan networkx

class notAdjacentConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.variables = [place1, place2]
        self.place1: str = place1
        self.place2: str = place2

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        # If either place is not in the assignment then it is not
        # yet possible for their colors to be conflicting
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        # check the color assigned to place1 is not the same as the
        # color assigned to place2
        match assignment[self.place1]:
            #For "long" type
            case "road":
                return (assignment[self.place2] != "river") or (assignment[self.place2] != "ravine")
            case "river":
                return (assignment[self.place2] != "road") or (assignment[self.place2] != "ravine")
            case "ravine":
                return ((assignment[self.place2] != "river") or
                        (assignment[self.place2] != "road") or
                        (assignment[self.place2] != "lake"))
            #For "3x3" type
            case "lake":
                return assignment[self.place2] != "ravine"
        return True

# END

# Preference constraint : Pilihan pertama yang sebaiknya dipakai jika memiliki tetangga dengan nilai tertentu
class preferedValue(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.variables = [place1, place2]
        self.place1: str = place1
        self.place2: str = place2
    def satisfied(self, assignment: Dict[str, str], types: Dict[str, str]) -> str:
        # If either place is not in the assignment then it is not
        # yet possible for their colors to be conflicting
        self.type1: str = types[int(self.place1)]
        self.type2: str = types[int(self.place2)]
        if (self.type1 != self.type2) or (self.place2 not in assignment):
            return None
        # check the color assigned to place1 is not the same as the
        # color assigned to place2

        else:
            if(random.random() < 0.7):
                return self.place2
            else:
                return None

# Unary constraint : Jarak node dari titik "entry"



#Memberi domain setiap variabel sesuai jenisnya.
def assign_domain(type: V) -> List[str]:
    if type == "entry":
        return ["road"]
    elif type == "long":
        return ["road", "river", "ravine"]
    elif type == "3x3":
        return ["clearing", "forest", "camp"]


#Menyimpan cluster graph sebagai graph networkx
#START

#Variables : Nodes
cluster_graph: nx.Graph = nx.read_edgelist("clusters.txt")
cluster_list = list(cluster_graph.nodes)
#Types
cluster_type: Dict[str, str] = {}
#Domains
cluster_domain: Dict[str, List[str]] = {}

#Reading types from "types.txt"
types: List = []

with open('types.txt') as f:
    for line in f:
        types.append(line.rstrip())



#Creating csp object
for cluster_node in cluster_list:
    node = int(cluster_node)
    # Assign types from preassigned list
    cluster_type[node] = types[node]
    # Assign domain List based on type
    cluster_domain[node] = assign_domain(cluster_type[node])
print("kek")
csp: CSP = CSP(cluster_list, cluster_type, cluster_domain)

#Creating constraints for each node
for cluster_node in cluster_list:
    for neighbour in cluster_graph.neighbors(cluster_node):
        csp.add_constraint(notAdjacentConstraint(cluster_node, neighbour))
        csp.add_preference(preferedValue(cluster_node, neighbour))

solution: Optional[Dict[str, str]] = csp.backtracking_search()
if solution is None:
    print("No solution found!")
else:

    print(solution)
#END