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

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))

while True:

    #message
    str =  input("Give the command: ")
    if str=="done":
        break
    mode = input("Give the mode: ")

    args = str.split(" ")

    # crypt layer
    crypt_str = encrypt(str,mode)
    client.send(crypt_str.encode())
    client.send(mode.encode())

    if(args[0]=="cwd"):
        en_path = client.recv(SIZE).decode()
        path = decrypt(en_path,mode)
        print(path)
    
    if(args[0]=="ls"):
        en_str = client.recv(SIZE).decode()
        str = decrypt(en_str,mode)
        list_dir = str.split(",")
        print(list_dir)
    
    if(args[0]=="cd"):
        en_dir = client.recv(SIZE).decode()
        curr_dir = decrypt(en_dir,mode)
        if(curr_dir=="NOK"):
            print("NOK")
        else:
            print(curr_dir)

    if(args[0]=='upd'):
        file_path = args[1]

        # file path sending
        file = open(file_path,'r')
        data = file.read()
        en_data = encrypt(data,mode)
        file.close()
        client.send(en_data.encode())

    elif(args[0]=='dwd'):
        file_path = args[1]
        file_name = os.path.basename(file_path)

        # recieve the data
        en_data = client.recv(SIZE).decode()
        data = decrypt(en_data,mode)

        new_file = open(file_name,'w')
        new_file.write(data)
        new_file.close()

client.close()
