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

    

def make_postdic(s):
    s = read_file(s)
    q = s.split("\<end>\n")
    result = {}
    for i in range(len(q)-1):
        tag_list = q[i][ q[i].find("[u"):q[i].find("']")+2 ]
        q[i] = q[i].replace("," + tag_list,"")
        w = q[i].split(",")
        result[i] = {"title":w[0],"user":w[1],"tags":tag_list,"content":w[2]}
    return result

def get_tags(s):
    result = []
    tag_list = []
    for i in range(len(s)-1):
        q = s["tags"]
        tag_list = q[ q.find("[u"):q.find("']")+2 ]
        tag_list.replace("u'","")
        tag_list.replace("[","")
        tag_list.replace("]","")
        tag_list.replace("'","")
        tag_list = tag_list.split(",")
        result.append(tag_list) 
    return tag_list


#######mode 'w' = write. mode 'a' = append (adds on to text file instead of replacing it).
def write_file(f,t):
    f = open(f,'a')
    f.write(t)
    f.close()
#print w
