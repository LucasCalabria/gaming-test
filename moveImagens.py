import os
import shutil

from data import global_variables


def move_image():
    for i in range(1, global_variables.SAMPLES_NUM + 1):
        path_original_image = os.path.expanduser('~') + '/AppData/Roaming/LOVE/flappybird/imagem_original-' + str(i) + '.png'
        path_destination = os.path.expanduser('~') + '/PycharmProjects/tcc/data/' + str(i)

        destination_file = path_destination + '/imagem_original-' + str(i) + '.png'

        if os.path.exists(destination_file):
            # in case of the src and dst are the same file
            if os.path.samefile(path_original_image, destination_file):
                break
            os.remove(destination_file)

        shutil.move(path_original_image, path_destination)

        print('Imagem movida: ' + str(i))


if __name__ == '__main__':
    move_image()
