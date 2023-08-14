import os
import shutil

path = 'C:/Users/lucas/PycharmProjects/tcc/data/'

num_folders = 10
delete_folder = False

if delete_folder:
    if os.path.exists(path):
        print("Removendo pasta data")
        shutil.rmtree(path)

    print("Criando pasta data")
    os.makedirs(path)

for i in range(1, num_folders+1):
    if not os.path.exists(path + str(i)):
        os.makedirs(path + str(i))
        print("Criada pasta: " + str(i))
