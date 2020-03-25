import sys
x = sys.argv                                         #taking command line argument (name of file)

if(len(x) != 2):                                     #checking for corret file name
    print('pass file name as a single argument')
    sys.exit()
try: 
    f = open(x[1],'r')                               #reading data from file
    data = f.read().splitlines()
    
    if(".circuit" and ".end" in data and data.index(".circuit") < data.index(".end")):  #checking validity of data
        start = data.index(".circuit")
        end = data.index(".end")
    else:
        print("invalid data in file")
        sys.exit()
    f.close()
    
    data_no_comment = []                             #removing comment
    for i in data:
        comment = i.split('#')
        data_no_comment.append(comment[0])    
    data = data_no_comment
    
    reqdata = []                                     #reversing order of data
    for i in list(reversed(data[start+1:end])):
        rev = list(reversed(i.split()))
        reqdata.append(" ".join(rev))
    for i in reqdata:                                # printing reversed data
        print(i)

except IOError: 
    print("file doesnt exist")
    sys.exit()
