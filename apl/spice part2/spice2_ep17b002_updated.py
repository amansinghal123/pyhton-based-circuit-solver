from numpy import * 
import sys
from cmath import * 
#===============================================this is assignment 1 module ===============================================
x = sys.argv                                         
if(len(x) != 2):                                    
    print('pass file name as a single argument')
    sys.exit()
try: 
    f = open(x[1],'r')
    data = f.read().splitlines()    
    data_no_comment = []                          
    for i in data:
        comment = i.split('#')
        data_no_comment.append(comment[0])    
    data = data_no_comment
    
    if(".circuit" and ".end" in data and data.index(".circuit") < data.index(".end")):  
        start = data.index(".circuit")
        end = data.index(".end")
    else:
        print("invalid data in file")
        sys.exit()
    f.close()    
    e = []
    for i in data[start+1:end]:
        c = i.split()
        e.append(c)
    data = e        
except IOError: 
    print("file doesnt exist")
    sys.exit()

#=================================detectig the .ac part and reading the frequency====================================
for _ in data_no_comment:
    if(".ac" in _):  
        ac = data_no_comment[data_no_comment.index(_)]
        f = float(ac.split()[-1])
        freq = 2*pi*f

#==============================function for calcultin values of components from string(1e3)==========================------------------------------
def exp(s):
    a = s.split("e")
    if(len(a) == 2):
        return float(a[0])*(10**float(a[1]))
    else:
        return float(s)

#========================================classes for components of circuit ===========================================
class component:
    def __init__(self,n, n1, n2, v):
        self.name = n
        self.node1 = node_dict[n1]
        self.node2 = node_dict[n2]
        self.value = exp(v)
        self.count = 0        
        
    def imp_cal(self,freq):
# calculting impedance for dc
        if(freq == 0):
            if(self.name[0] == "L"):
                self.imp = 10**-6  #very small impedance of inductor for dc instead of 0
            elif(self.name[0] == "C"):
                self.imp = inf     #infinite impedance of capacitor for dc
            elif(self.name[0] == "R"):
                self.imp = self.value
# calculting impedance for ac
        else:        
            if(self.name[0] == "L"):
                self.imp = complex(0,self.value*freq) 
            elif(self.name[0] == "C"):
                self.imp = complex(0,-1/(self.value*freq))
            elif(self.name[0] == "R"):
                self.imp = self.value

class curr_source:
    def __init__(self,n, n1, n2, *v):   #*v has value and phase for ac and only value for dc
        self.name = n
        self.node1 = node_dict[n1]
        self.node2 = node_dict[n2]
        if(v[0] == "dc"):
            self.value = exp(v[1])  
        if(v[0] == "ac"):
            self.value = exp(v[1])
            self.phase = exp(v[2])    
        self.count = 0
                
class volt_source:
    def __init__(self,n, n1, n2, *v):   #*v has value and phase for ac and only value for dc
        self.name = n
        self.node1 = node_dict[n1]
        self.node2 = node_dict[n2]
        self.value = exp(v[1])
        if(v[0] == "dc"):
            self.kind = "dc"
        if(v[0] == "ac"):
            self.kind = "ac"
            self.phase = exp(v[2])
        
#========================================dictionary of node in circuit============================================
#list of all nodes in circuit
node = []
for i in data:
    node.append(i[1])
    node.append(i[2])
node = list(set(node))    

node_dict={}
#assigning values to nodes
for i,j in enumerate(sorted(node),start = 1):
    if(j == "GND"):
        node_dict[j] = 0
    else:
        node_dict[j] = i

#======================================list of objects on the basis of name=======================================
comp_objs = []
volt_objs = []
voltac_objs = []
curr_objs = []
currac_objs = []
#k is list of [V1,1,2,10]
for k in data:
    if(list(k[0])[0] == "R" or list(k[0])[0] == "C" or list(k[0])[0] == "L"):
        obj = component(*k)
        comp_objs.append(obj)
    elif(list(k[0])[0] == "V" and k[3] == "dc"):
        obj = volt_source(*k)
        volt_objs.append(obj)
    elif(list(k[0])[0] == "V" and k[3] == "ac"):
        obj = volt_source(*k)
        voltac_objs.append(obj)
    elif(list(k[0])[0] == "I" and k[3] == "dc"):
        obj = curr_source(*k)
        curr_objs.append(obj)
    elif(list(k[0])[0] == "I" and k[3] == "ac"):
        obj = curr_source(*k)
        currac_objs.append(obj)
    else:
        print("no cont_sources yet")
        sys.exit()

#==================function defined for taking in objects in the ciruit and outputing the result vector============
def solver(comp_objs, volt_objs, curr_objs,f):
    freq = f    
    
#============================making two different dictionaries: from nodes and to nodes===========================   
    from_all ={}
    to_all = {}
    for v in node_dict.values():    #v is the value of node. eg: {GND : 0} value of GND is 0
        from_node = []
        to_node = []
        for i in comp_objs:
            i.imp_cal(freq)         # calculating impedance of component by calling imp_cal
            if(i.node1 == v):       # node1 is from node
                from_node.append(i)
            if(i.node2 == v):       # node2 is to node
                to_node.append(i)
        for i in volt_objs:
            if(i.node1 == v):
                from_node.append(i)
            if(i.node2 == v):
                to_node.append(i)
        for i in curr_objs:
            if(i.node1 == v):
                from_node.append(i)
            if(i.node2 == v):
                to_node.append(i)
        from_all[v] = from_node     # for v = 1, from_all = {1:r1,c2}
        to_all[v] = to_node         # for v = 1, to_all = {1:r2,c1}
# from_all and to_all of the form: {1:r1,r2 , 2:c1,r3 .....}
#================================================making the current part of vector b=============================================== 
    b = []
    for i in range(1,len(node_dict)):  
        cur = 0
        for j in to_all[i]:
            if(j in curr_objs):
                cur += j.value
        for j in from_all[i]:
            if(j in curr_objs):
                cur -= j.value
        b.append(cur)                

#=======================================================making the matrix A=========================================
    # all zero matrix
    matrix = array([zeros(len(node_dict) + len(volt_objs) - 1,dtype = complex) for i in range(len(node_dict)+len(volt_objs) - 1)])
    '''
    matrix divided into 4 parts
    [1 2]
    [3 0]
    1 = 1/Z of components
    2 = coeff current through voltage sources
    3 = voltage across voltage sources
    '''
    # ROW represents the node number of which nodal eqaution is being worked on
    for row in range(1,len(node_dict)+len(volt_objs)):
        for col in range(1, len(node_dict) + len(volt_objs)):
            # diagnol elements of 1st part of matrix
            g = 0
            if(row == col and row <= len(node_dict)-1 and col <= len(node_dict)-1):   #selecting diagnol elements
                for j in comp_objs:
                    if(j.node1 == row or j.node2 == row):   #if component connected to row
                        g += 1/j.imp
                matrix[row-1,col-1] = array(g)
                
            # non diagnol elements of 1st of matrix
            elif(row <= len(node_dict)-1 and col <= len(node_dict)-1 and row != col):
                for j in comp_objs:
                    if((j.node1 == row or j.node2== row) and (j.node1 == col or j.node2 == col)): #if component connected to row
                        g -= 1/j.imp
                matrix[row-1,col-1] = array(g)
                
            # 2nd part of matrix           
            elif(col > len(node_dict)-1):
                for j in volt_objs:
                    if(j.node1 == row and col == len(node_dict) + volt_objs.index(j)): #b11,b12....b1k
                        matrix[row-1,col-1] = 1
                    if(j.node2 == row and col == len(node_dict) + volt_objs.index(j)):
                        matrix[row-1,col-1] = -1
                        
    # 3rd part f matrix and voltage part of b vector
    count = 0            
    for j in volt_objs:
        count += 1
        b.append(j.value)   # making voltage part of b
        if(j.node1 != 0):
            matrix[count+len(node_dict)-2,j.node1 - 1] = -1  # put -1 on the node from where the voltage source starts
        if(j.node2 != 0):
            matrix[count+len(node_dict)-2,j.node2 - 1] = 1  # put 1 on the node from where the voltage source end
    b = array(b)      
 
#====================================================solving Ax = b===================================================
    x = []
    for i in list(linalg.solve(matrix,b)):
        x.append(round(i,5))
    return x

#===========printing the vector having the nodal voltages and current through the voltage sources=================
try:
    dc = solver(comp_objs,volt_objs,curr_objs,0)
    print("dc nodal voltages are:")
    for i in dc[:len(node_dict)- 1]:
        print(i.real)
    print("current through dc voltage sources is:",end = " ")
    for i in dc[-len(volt_objs):]:
        if(abs(i)>10000):
            print(inf)
        else:
            print(round(i.real,5))
    print()
except:
    print("dc part not solvable")
    print()
    
for _ in data_no_comment:
    if(".ac" in _):  
        ac = solver(comp_objs,voltac_objs,currac_objs,freq)
        print("ac nodal voltages are:")
        for i in ac[:len(node_dict)- 1]:
            print("peak to peak:",round(abs(i),5),"phase:",round(phase(i)*180/(2*3.14),5),"degrees")
        print("ac current through voltage sources is:",end = " ")
        for i in ac[-len(voltac_objs):]:
            print(round(abs(i),5))
            
#========================================================FINISH=================================================================


        
        
        
        
        
        
        