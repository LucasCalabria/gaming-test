import os

path = 'C:/Users/lucas/PycharmProjects/tcc/data/'


for i in range(1, 11):
    if not os.path.exists(path + str(i)):
        os.makedirs(path + str(i))
        print("Criada pasta: " + str(i))
