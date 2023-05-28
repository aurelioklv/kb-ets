import networkx as nx # Digunakan untuk menyimpan graph
import matplotlib.pyplot as plt # Digunakan untuk menampilkan graph
import random # Digunakan untuk random number generator (random()).


#NOTE : Harus python 3.10+ karena pakai "match case"

#Variables :
    # "entry" : Single node
    # "long" : 3 node long
    # "3x3" : 9 node 3x3

#Domain sets :
    #1. Forest, USED FOR INITIAL TESTING
    #   "entry" : "road"
    #   "long"  : "road", "river", "ravine"
    #   "3x3"   : "clearing", "forest", "camp", "lake"

#Colour Table :
    #1. Forest
    #   "long"  : "road", = "goldenrod"
    #           "river", = "skyblue"
    #           "ravine" = "silver"
    #   "3x3"   : "clearing", = "greenyellow"
    #           "forest", = "green"
    #           "camp", = "orange"
    #           "lake" = "royalblue"

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



# Kelas abstract untuk constraint yang digunakan.
class Constraint(Generic[V, D], ABC):
    # Menyimpan variabel-variabel yang dipengaruhi constraint.
    # Constraint harus dibuat untuk setiap set variabel yang dipengaruhi constraint agar diuji satu per satu.
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> R:
        ...

# Class CSP, diubah agar sesuai dengan masalah yang dikerjakan :
# Tambahan :
    # types dan domains, untuk menyimpan informasi tipe cluster node dan domainnya.
    # prefConstraint, untuk menyimpan preference constraint yang penggunaannya berbeda dengan constraint yang benar atau salah.
class CSP:
    def __init__(self, variables: List[V], types: Dict[V, V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables  # Variable dalam CSP (Cluster nodes)
        self.types: Dict[V, V] = types # Tipe setiap cluster node
        self.domains: Dict[V, List[D]] = domains  # Domain setiap variable
        self.constraints: Dict[V, List[Constraint]] = {} # Berisi setiap constraint yang mempengaruhi variabel 'V'
        self.prefConstraint: Dict[V, List[Constraint]] = {} # Berisi preference constraint yang mempengaruhi variabel 'V'

        # Inisialisasi list kosong untuk menyimpan constraints + memastikan setiap variable ada domain.
        for variable in self.variables:
            self.constraints[variable] = []
            self.prefConstraint[variable] = []
            if not self.domains[int(variable)]:
                raise LookupError("Every variable should have a domain assigned to it.")

    # Kedua fungsi add digunakan untuk menambah constraint ke dalam objek CSP
    # Digunakan untuk mempermudah pengaksesan constraint di backtracking algorithm
    def add_constraint(self, constraint: Constraint) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    # Fungsi tambahan untuk preference constraint
    def add_preference(self, constraint: Constraint) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.prefConstraint[variable].append(constraint)

    #Fungsi tambahan untuk preference constraint
    # Digunakan untuk memberi nilai assignment node 'V' yang sesuai dengan preference constraint.
    def preference(self, variable: V, assignment: Dict[V, D]) -> D:
        for constraint in self.prefConstraint[variable]:
            return constraint.satisfied(assignment, self.types)



    # Fungsi untuk menguji assignment nilai node 'V' terhadap semua constraint node tersebut agar memenuhi semuanya atau tidak.

    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    # Fungsi recursive untuk backtracking search
    # Args:
        # assignment : Dictionary berisi hasil assignment untuk setiap node, setiap rekursi akan semakin terisi.
    def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        # Jika semua variable sudah diberi nilai, proses assignment selesai.
        if len(assignment) == len(self.variables):
            return assignment

        # Mengambil list berisi variable yang belum diberi nilai
        unassigned: List[V] = [v for v in self.variables if v not in assignment]

        # Mendapatkan setiap nilai pada domain yang bisa diberi ke variable pertama di list unassigned.
        first: V = unassigned[0]
        random.shuffle(self.domains[int(first)])

        # Memeriksa untuk setiap value yang bisa diassign apakah memenuhi constraint2 atau tidak.
        for value in self.domains[int(first)]:
            local_assignment = assignment.copy()
            prefered_value = self.preference(first, local_assignment)
            # Mencoba mencari nilai yang sesuai preference constraint sebaiknya dipilih dulu
            if prefered_value is not None:
                local_assignment[first] = prefered_value # Jika ditemukan, coba nilai ini dulu sebelum value
            else:
                local_assignment[first] = value
            # Jika masih ditemukan nilai yang bisa diassign, lanjutkan rekursi.
            if self.consistent(first, local_assignment):
                result: Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
                # Backtracking jika tidak ditemukan nilai yang bisa diassign
                if result is not None:
                    return result
        return None

# Constraint yang memastikan bahwa terdapat 2 nilai (region) yang tidak bisa saling terhubung
class notAdjacentConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.variables = [place1, place2]
        self.place1: str = place1
        self.place2: str = place2

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        # Jika setidaknya 1 node yang ingin dibandingkan belum ada nilai, tidak mungkin constraint gagal.
        if self.place1 not in assignment or self.place2 not in assignment:
            return True

        # Melakukan perbandingan berdasarkan tipe cluster
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
        if str(self.place1) not in assignment:
            return None

        self.type1: str = types[int(self.place1)]
        self.type2: str = types[int(self.place2)]
        # Jika tipe kedua cluster node tidak sama, otomatis domainnya berbeda.
        if (self.type1 != self.type2):
            return None
        # Jika sama dan node pertama sudah terisi, maka tambah kemungkinan node kosong diisi dengan nilai node pertama.
        else:
            if(random.random() < 0.7):
                return assignment[self.place1]
            else:
                return None

# assign_colour :
#Memberi warna setiap verteks yang sudah diberi value (warna menggunakan daftar warna matplotlib).
    #   "long"  : "road", = "goldenrod"
    #           "river", = "skyblue"
    #           "ravine" = "silver"
    #   "3x3"   : "clearing", = "greenyellow"
    #           "forest", = "green"
    #           "camp", = "orange"
    #           "lake" = "royalblue"
# Input :
    #  1. Dictionary berisi tipe setiap node cluster.
    #  2. Dictionary berisi hasil assignment per cluster.
# Output :
    #  List berisi warna setiap node, urut dengan urutan node di dictionary dan sejumlah dengan jumlah node setiap cluster.
def assign_colour(types: Dict[str, str], result: Dict[str, str]) -> List[str]:
    colour_list: List[str] = []
    node_amount = 0
    # Menentukan jumlah node yang diberi warna berdasarkan cluster.
    for key, value in result.items():
        key = int(key)
        if(types[key] == "entry"):
            node_amount = 1
        elif(types[key] == "long"):
            node_amount = 3
        elif(types[key] == "3x3"):
            node_amount = 9
        # Memberi warna sejumlah node di dalam cluster.
        for x in range(node_amount):
            if value == "road":
                colour_list.append("goldenrod")
            elif value == "river":
                colour_list.append("skyblue")
            elif value == "ravine":
                colour_list.append("silver")
            elif value == "clearing":
                colour_list.append("greenyellow")
            elif value == "forest":
                colour_list.append("green")
            elif value == "camp":
                colour_list.append("orange")
            elif value == "lake":
                colour_list.append("royalblue")
            else:
                colour_list.append("magenta")
    return colour_list

#Memberi domain setiap variabel sesuai jenis clusternya.
def assign_domain(type: V) -> List[str]:
    if type == "entry":
        return ["road"]
    elif type == "long":
        return ["road", "river", "ravine"]
    elif type == "3x3":
        return ["clearing", "forest", "camp", "lake"]

#Membangun graph utuh dari cluster_graph
#Input :
    # Daftar node cluster
#Output :
    # nx.graph berisi terjemahan cluster menjadi node-node sesungguhnya.
def build_output(input: List[str]) -> nx.Graph:
    result = nx.Graph()
    nodeCount = 0
    for value in input:
        if value == "entry":
            result.add_node(nodeCount)
            nodeCount += 1
        # long berupa 3 node (O-O-O)
        elif value == "long":
            for i in range(3):
                result.add_node(nodeCount)
                #For undirected edge
                result.add_edge(nodeCount - 1, nodeCount)
                result.add_edge(nodeCount, nodeCount - 1)
                nodeCount += 1
        # 3x3 berupa 9 nodes tersusun seperti grid
        elif value == "3x3":
            for i in range(9):
                result.add_node(nodeCount)
                nodeCount += 1
            #Builds edges
            nodeCount -= 1 #Accounts for mistake in add_edge
            for x in range(2):
                i = x*3
                result.add_edge(nodeCount - 1 - i, nodeCount - i)
                result.add_edge(nodeCount - i, nodeCount - 1 - i)
                result.add_edge(nodeCount - 2 - i, nodeCount - i)
                result.add_edge(nodeCount - i, nodeCount - 2 - i)
                result.add_edge(nodeCount - 3 - i, nodeCount - i)
                result.add_edge(nodeCount - i, nodeCount - 3 - i)
                result.add_edge(nodeCount - 4 - i, nodeCount - 1 - i)
                result.add_edge(nodeCount - 1 - i, nodeCount - 4 - i)
                result.add_edge(nodeCount - 2 - i, nodeCount - 5 - i)
                result.add_edge(nodeCount - 5 - i, nodeCount - 2 - i)
            result.add_edge(nodeCount - 6, nodeCount - 7)
            result.add_edge(nodeCount - 7, nodeCount - 6)
            result.add_edge(nodeCount - 6, nodeCount - 8)
            result.add_edge(nodeCount - 8, nodeCount - 6)
            result.add_edge(nodeCount - 6, nodeCount - 9)
            result.add_edge(nodeCount - 9, nodeCount - 6)
            nodeCount += 1

    return result
#MAIN


#Menyimpan cluster graph sebagai graph networkx
#START

#Variables : Nodes
cluster_graph: nx.Graph = nx.read_edgelist("clusters.txt")
cluster_list = list(cluster_graph.nodes)
#Types
cluster_type: Dict[str, str] = {}
#Domains
cluster_domain: Dict[str, List[str]] = {}

#Membaca tipe cluster dari "types.txt"
types: List = []

with open('types.txt') as f:
    for line in f:
        types.append(line.rstrip())



#Membuat objek "csp"
for cluster_node in cluster_list:
    node = int(cluster_node)
    # Memberi tipe cluster berdasarkan list
    cluster_type[node] = types[node]
    # Memberi domain berdasarkan tipe cluster.
    cluster_domain[node] = assign_domain(cluster_type[node])
print("kek")
csp: CSP = CSP(cluster_list, cluster_type, cluster_domain)

#Menghasilkan constraint untuk setiap node. Tepatnya setiap node memiliki constraint terhadap tetangganya.
for cluster_node in cluster_list:
    for neighbour in cluster_graph.neighbors(cluster_node):
        csp.add_constraint(notAdjacentConstraint(cluster_node, neighbour))
        csp.add_preference(preferedValue(cluster_node, neighbour))

solution: Optional[Dict[str, str]] = csp.backtracking_search()
if solution is None:
    print("No solution found!")
else:
    print(solution)
    # Membangun graph sesungguhnya dari hasil
    result_graph: nx.Graph = build_output(types)
if result_graph is not None:
    # Menggambar graph hasil dengan warna sesuai assignment CSP
    nx.draw_networkx(result_graph, node_color=assign_colour(cluster_type, solution))

    # Mengatur margin pada sumbu gambar menjadi nol
    plt.margins(0)

    # Menghilangkan garis tepi (spine) pada sumbu
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Mengatur parameter bbox_inches menjadi 'tight' saat menyimpan gambar
    plt.savefig('D:\kb_ets\solution.png', bbox_inches='tight')
    # plt.show()
#END
