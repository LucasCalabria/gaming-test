import cv2
import numpy as np

from data import global_variables


def mse(img1, img2):
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff ** 2)
    result = err / (float(h * w))
    return result, diff


def compare_images():
    for i in range(1, global_variables.SAMPLES_NUM + 1):
        print("Importando imagem: " + str(i))
        images_path = 'data/' + str(i) + '/'

        name_image_original = 'imagem_original-' + str(i) + '.png'
        name_image_recreated = 'imagem_recriada-' + str(i) + '.png'

        image_original = cv2.imread(images_path + name_image_original)
        image_recreated = cv2.imread(images_path + name_image_recreated)

        image_original = cv2.cvtColor(image_original, cv2.COLOR_BGR2GRAY)
        image_recreated = cv2.cvtColor(image_recreated, cv2.COLOR_BGR2GRAY)

        error, diff = mse(image_original, image_recreated)

        print("Image matching Error between the two images:", error)

        if i == 10:
            cv2.imshow("difference", diff)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__ == '__main__':
    compare_images()
