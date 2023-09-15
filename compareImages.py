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
        images_path = 'data/' + str(i) + '/'
        name_image_original = \
            'imagem_original-' + str(i) + '.png'
        name_image_recreated = \
            'imagem_recriada-' + str(i) + '.png'

        test_image = cv2.imread(
            images_path + name_image_original)
        reference_image = cv2.imread(
            images_path + name_image_recreated)

        diff_image = cv2.absdiff(reference_image, test_image)
        if gray:
            gray_diff = cv2.cvtColor(
                diff_image, cv2.COLOR_BGR2GRAY)

            _, thresholded = cv2.threshold(
                gray_diff, threshold, 255, cv2.THRESH_BINARY)
        else:
            _, thresholded = cv2.threshold(
                diff_image, threshold, 255, cv2.THRESH_BINARY)

        kernel = np.ones((5, 5), np.uint8)
        eroded = cv2.erode(thresholded, kernel, iterations=1)

        opening_kernel = np.ones((10, 10), np.uint8)
        opened = cv2.morphologyEx(
            eroded, cv2.MORPH_OPEN, opening_kernel)

        num_different_pixels = np.count_nonzero(opened)
        all_diffs[i] = num_different_pixels
        if num_different_pixels > threshold_bug:
            bug_diffs[f'{i}'] = num_different_pixels

    return all_diffs, bug_diffs


def divide_image_into_areas(image, area_size):
    height, width, _ = image.shape
    areas = []

    for y in range(0, height, area_size):
        for x in range(0, width, area_size):
            area = image[y:y + area_size, x:x + area_size]
            areas.append(area)

    return areas


def has_consecutive_keys(dictionary):
    keys = dictionary.keys()
    keys = [int(element) for element in keys]
    keys = sorted(keys)

    for i in range(len(keys) - 2):
        if keys[i] + 1 == keys[i + 1] and keys[i + 1] + 1 == keys[i + 2]:
            return True

    return False


def check_all_distortion(square_size=50,
                         distortion_threshold=95):
    results = []
    results_bug = {}
    for i in range(1, global_variables.SAMPLES_NUM + 1):
        images_path = 'data/' + str(i) + '/'
        name_image_original = \
            'imagem_original-' + str(i) + '.png'

        image = cv2.imread(
            images_path + name_image_original)

        squares = divide_image_into_areas(
            image, square_size)
        has_artifact = detect_distortion_in_squares(
            squares, distortion_threshold)

        results.append(has_artifact)
        if has_artifact:
            results_bug[f'{i}'] = has_artifact

    return results, results_bug


def detect_distortion_in_squares(squares, distortion_threshold=95):
    for idx, square in enumerate(squares):
        gray_square = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray_square, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray_square, cv2.CV_64F, 0, 1, ksize=3)
        gradient_magnitude = np.sqrt(sobelx ** 2 + sobely ** 2)
        mean_gradient = np.mean(gradient_magnitude)

        if mean_gradient > distortion_threshold:
            return True

    return False


def main():
    bug_found = False

    # Teste das formas
    all_diffs, bug_diffs = compare_all(75, 750, True)
    if has_consecutive_keys(bug_diffs):
        print("Bug visual encontrado - teste de forma")
        print(bug_diffs)
        bug_found = True

    # Teste com cores
    all_diffs, bug_diffs = compare_all(75, 750)
    if has_consecutive_keys(bug_diffs):
        print("Bug visual encontrado - teste de cor")
        print(bug_diffs)
        bug_found = True

    # Teste de distorcao
    results, results_bug = check_all_distortion(square_size=100, distortion_threshold=80)
    if has_consecutive_keys(results_bug):
        print("Bug visual encontrado - teste de distorcao")
        print(results_bug.keys())
        bug_found = True

    if not bug_found:
        print("Nenhum bug encontrado")


if __name__ == '__main__':
    main()

# cv2.imshow("Artifact Area", result_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
