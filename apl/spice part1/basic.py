import sys
x = sys.argv                                #taking command line argument (name of file)

if(len(x) != 2):                            #checking for corret file name
    print('pass file name as a single argument')
    sys.exit()
try: 
    f = open(x[1],'r')                      #reading data from file
    data = f.read().splitlines()   
    start = data.index(".circuit")
    end = data.index(".end")
    f.close()
    
    
    for i in data[start+1:end]:
    
        m = i.split()
        if(list(m[0])[0] == "R"):
            print("%s resistor from node %s to node %s"%(m[3],m[1],m[2]))
            
        elif(list(m[0])[0] == "L"):
            print("%s inductor from node %s to node %s"%(m[3],m[1],m[2]))
            
        elif(list(m[0])[0] == "C"):
            print("%s capacitor from node %s to node %s"%(m[3],m[1],m[2]))
        
        elif(list(m[0])[0] == "V"):
            print("%s battery from node %s to node %s"%(m[3],m[1],m[2]))
        
        elif(list(m[0])[0] == "I"):
            print("%s current source from node %s to node %s"%(m[3],m[1],m[2]))
        else:
            print('invalid device')
    
        
except IOError: 
    print("the %s doesn't exist"%x[1])
    sys.exit()
