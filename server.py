import sys,socket,os

SIZE = 4096

def encrypt(str, mode):
    new_str = ""
    if(mode=='1'):
        new_str = str
    elif(mode=='2'):
        offset=2
        for i in str:
            if(48<=ord(i) and ord(i)<=57):
                new_str += chr((ord(i)+offset-48)%10 + 48)
            elif(65<=ord(i) and ord(i)<=90):
                new_str += chr((ord(i)+offset-65)%26 + 65)
            elif(97<=ord(i) and ord(i)<=122):
                new_str += chr((ord(i)+offset-97)%26 + 97)
            else:
                new_str+=i
    
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
        offset=2
        for i in str:
            if(48<=ord(i) and ord(i)<=57):
                new_str += chr((ord(i)-offset-48+10)%10 + 48)
            elif(65<=ord(i) and ord(i)<=90):
                new_str += chr((ord(i)-offset-65+26)%26 + 65)
            elif(97<=ord(i) and ord(i)<=122):
                new_str += chr((ord(i)-offset-97+26)%26 + 97)
            else:
                new_str+=i
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

        try:
            file = open(file_path,'r')
            data = file.read()
            en_data = encrypt(data,mode)
            file.close()
        except:
            en_data = encrypt("NOK",mode)

        connec.send(en_data.encode())
        

    elif(args[0]=="upd"):
        file_path = args[1]
        file_name = os.path.basename(file_path)

        en_data = connec.recv(SIZE).decode()
        data = decrypt(en_data,mode)
        
        if(data!="NOK"):
            new_file = open(file_name,'w')
            new_file.write(data)
            new_file.close()

server.close()
