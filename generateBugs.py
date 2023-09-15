import cv2
import numpy as np

# Defina a intensidade da distorção (valores mais altos geram mais distorção)
intensity = 60
kernel_size = 15
intensity_tearing = 15
tear_width = 15
num_artifacts = 75
artifact_intensity = 30

image_path = 'assets/imagens/pipe.png'
output_path = 'pipe-art.png'

choice = 4


def apply_artifacts(img):
    height, width, channels = img.shape

    artifact_image = img.copy()

    for _ in range(num_artifacts):
        y = np.random.randint(0, height)
        x = np.random.randint(0, width)
        h = np.random.randint(5, 50)
        w = np.random.randint(5, 50)

        artifact = np.random.normal(0, artifact_intensity, (h, w, channels))

        y_end = min(y + h, height)
        x_end = min(x + w, width)

        artifact_image[y:y_end, x:x_end, :] = np.clip(
            artifact_image[y:y_end, x:x_end, :] + artifact[:y_end - y, :x_end - x, :], 0, 255)

    return np.clip(artifact_image, 0, 255).astype(np.uint8)


def apply_tearing(img):
    height, width, channels = img.shape

    torn_image = img.copy()

    for y in range(0, height, tear_width):
        offset = np.random.randint(-intensity_tearing, intensity_tearing + 1)
        torn_image[y:y + tear_width, :, :] = np.roll(torn_image[y:y + tear_width, :, :], offset, axis=1)

    return torn_image


def apply_distortion(img):
    height, width, _ = img.shape

    # Crie uma matriz de distorção usando ruído gaussiano
    distortion = np.random.normal(0, intensity, (height, width, 3))

    # Adicione a matriz de distorção à imagem original
    distorted_image = np.clip(img + distortion, 0, 255).astype(np.uint8)

    return distorted_image


# Carregue a imagem
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# Verifique se a imagem tem um canal alfa (transparência)
has_alpha_channel = image.shape[2] == 4

# Separe a parte da imagem com canal alfa (transparência) e sem
if has_alpha_channel:
    alpha_channel = image[:, :, 3]
    image_without_alpha = image[:, :, :3]
else:
    alpha_channel = None
    image_without_alpha = image

# Aplique a distorção apenas na parte sem o canal alfa
if choice == 0:
    result = apply_distortion(image_without_alpha)
elif choice == 1:
    result = apply_tearing(image_without_alpha)
else:
    result = apply_artifacts(image_without_alpha)

# Combine a parte distorcida com o canal alfa, se existir
if has_alpha_channel:
    distorted_image = np.dstack((result, alpha_channel))
else:
    distorted_image = result

# Salve a imagem distorcida em formato PNG
cv2.imwrite(output_path, distorted_image)

# Mostre a imagem original e a imagem distorcida
cv2.imshow('Imagem Original', image)
cv2.imshow('Imagem Distorcida', distorted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()