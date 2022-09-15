import sys,socket,os

SIZE = 4096

def encrypt(str, mode):
    new_str = ""
    if(mode=='1'):
        new_str = str
    elif(mode=='2'):
        for i in str:
            new_str+= chr(ord(i)+2)
    elif(mode=='3'):
        list = str.split(" ")
        for i in list:
            new_str+=i[::-1]
            new_str+=" "
        new_str = new_str[:len(new_str)-1]
    return new_str

def decrypt(str, mode):
    new_str = ""
    if(mode=='1'):
        new_str = str
    elif(mode=='2'):
        for i in str:
            new_str+= chr(ord(i)-2)
    elif(mode=='3'):
        list = str.split(" ")
        for i in list:
            new_str+=i[::-1]
            new_str+=" "
        new_str = new_str[:len(new_str)-1]
    
    return new_str


host = socket.gethostname()
port = 40000

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((host,port))
server.listen(5)

#accept new connection
connec, addr = server.accept()

print("Conn from:"+str(addr))

while True:
    en_str = connec.recv(SIZE).decode()
    mode = connec.recv(SIZE).decode()

    if not en_str:
        break

    str = decrypt(en_str,mode)
    print(str)
    args = str.split(" ")
    
    if(args[0]=="cwd"):
        cdir = os.getcwd()
        en_dir = encrypt(cdir,mode)
        connec.send(en_dir.encode())

    elif(args[0]=="ls"):
        list_dir = os.listdir()
        # print(list_dir)
        str = ""
        for i in list_dir:
            str+=i
            str+=","
        new_str = str[:len(str)-1]
        en_str = encrypt(new_str,mode)
        connec.send(en_str.encode())

    elif(args[0]=="cd"):
        try:
            newdir= args[1]
            os.chdir(newdir)
            curr_dir = os.getcwd()
            en_dir = encrypt(curr_dir,mode)
            connec.send(en_dir.encode())
        except:
            str = "NOK"
            en_str = encrypt(str,mode)
            connec.send(en_str.encode())

    elif(args[0]=="dwd"):
        file_path = args[1]
        file_name = os.path.basename(file_path)

        file = open(file_path,'r')
        data = file.read()
        en_data = encrypt(data,mode)
        file.close()
        connec.send(en_data.encode())

    elif(args[0]=="upd"):
        file_path = args[1]
        file_name = os.path.basename(file_path)

        new_file = open(file_name,'w')
        en_data = connec.recv(SIZE).decode()
        data = decrypt(en_data,mode)
        new_file.write(data)
        new_file.close()

server.close()
