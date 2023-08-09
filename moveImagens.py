import os
import shutil


def move_image():
    path_original_image = os.path.expanduser('~') + "/AppData/Roaming/LOVE/flappybird/imagem_original.png"
    path_destination = os.path.expanduser('~') + '/PycharmProjects/tcc/data'

    destination_file = path_destination + '/imagem_original.png'

    if os.path.exists(destination_file):
        # in case of the src and dst are the same file
        if os.path.samefile(path_original_image, destination_file):
            return
        os.remove(destination_file)

    shutil.move(path_original_image, path_destination)


if __name__ == '__main__':
    move_image()
