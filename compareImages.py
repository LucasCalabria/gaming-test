import cv2
import importlib
import numpy as np

from data import global_variables

escala = global_variables.WINDOW_WIDTH / global_variables.VIRTUAL_WIDTH

columns = ["total de imagens", "msr", 'diferenca de histograma', 'diferenca absoluta',
           'diferenca estruturada normalizada', 'indice de similaridade estrutural']


# Função para contar numero de imagens da amostra
def count_images(i):
    num_images = 0
    images = importlib.import_module("data." + str(i) + ".images")

    for _ in images.images:
        num_images += 1

    for _ in images.background_images:
        num_images += 1

    return num_images


def compare_all(threshold, threshold_bug, gray=False):
    all_diffs = {}
    bug_diffs = {}

    for i in range(1, global_variables.SAMPLES_NUM + 1):
        # Importando imagens
        images_path = 'data/' + str(i) + '/'

        name_image_original = 'imagem_original-' + str(i) + '.png'
        name_image_recreated = 'imagem_recriada-' + str(i) + '.png'

        # Recriação da imagem de referência (sem bugs)
        test_image = cv2.imread(images_path + name_image_original)

        # Captura da imagem de teste (possivelmente com bugs)
        reference_image = cv2.imread(images_path + name_image_recreated)

        # Calcula a diferença de fundo
        diff_image = cv2.absdiff(reference_image, test_image)

        # Converte a diferença em tons de cinza
        gray_diff = cv2.cvtColor(diff_image, cv2.COLOR_BGR2GRAY)

        # Aplica a binarização para segmentar as áreas de grande diferença
        if gray:
            _, thresholded = cv2.threshold(gray_diff, threshold, 255, cv2.THRESH_BINARY)
        else:
            _, thresholded = cv2.threshold(diff_image, threshold, 255, cv2.THRESH_BINARY)

        # Aplica uma operação de erosão para remover pequenos detalhes
        kernel = np.ones((5, 5), np.uint8)
        eroded = cv2.erode(thresholded, kernel, iterations=1)

        # Aplica uma operação de abertura para remover regiões menores
        opening_kernel = np.ones((10, 10), np.uint8)
        opened = cv2.morphologyEx(eroded, cv2.MORPH_OPEN, opening_kernel)

        # Calcula a quantidade de pixels de diferença após erosão e abertura
        num_different_pixels = np.count_nonzero(opened)

        all_diffs[i] = num_different_pixels

        # Exibe imagens com possivel bugs
        if num_different_pixels > threshold_bug:
            bug_diffs[f'{i}'] = num_different_pixels
            # print(f"Imagem: {i}\tQuantidade de pixels de diferença: {num_different_pixels}")

    return all_diffs, bug_diffs


def has_consecutive_keys(dictionary):
    keys = dictionary.keys()
    keys = [int(element) for element in keys]
    keys = sorted(keys)

    for i in range(len(keys) - 2):
        if keys[i] + 1 == keys[i + 1] and keys[i + 1] + 1 == keys[i + 2]:
            return True

    return False


def main():
    # Teste apenas das formas
    all_diffs, bug_diffs = compare_all(75, 1000, True)
    if has_consecutive_keys(bug_diffs):
        print("Bug visual encontrado")
        return

    # Teste com cores
    all_diffs, bug_diffs = compare_all(75, 750)
    if has_consecutive_keys(bug_diffs):
        print("Bug visual encontrado")
        return

    print("Nenhum bug encontrado")


if __name__ == '__main__':
    main()
