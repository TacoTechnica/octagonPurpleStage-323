def read_file(fname):
    f = open(fname)
    s = f.read()
    f.close()
    return s

def get_list(s,index):
    s = s.split("\n")
    return s[index].split(",")

def make_dic(s):#For Usernames and Passwords
    q = s.split("\n")
    result = {}
    for i in range(len(q)-1):
        w = q[i].split(",")
        result[w[0]] = w[1]
    return result

#######mode 'w' = write. mode 'a' = append (adds on to text file instead of replacing it).
def write_file(f,t):
    f = open(f,'a')
    f.write(t)
    f.close()
#print w
