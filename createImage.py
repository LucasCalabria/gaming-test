import importlib
from PIL import Image, ImageOps, ImageFont, ImageDraw

from data import global_variables

path_assets = 'assets/'  # TODO trocar caminho para diretorio do jogo
# path_assets = 'D:/Documents/tcc/flappybird/'
path_variables = 'data/'

difSize = global_variables.WINDOW_WIDTH / global_variables.VIRTUAL_WIDTH


def draw_background_image(canvas, draw, image):
    x = int(float(image.get('x')) * difSize)
    y = int(float(image.get('y')) * difSize)

    image_path = path_assets + image.get('path')

    # Carrega a figura
    background = Image.open(image_path).convert("RGBA")
    background_ratio = background.width / background.height

    # Calcula as novas dimensoes da figura
    background_height = int(global_variables.WINDOW_HEIGHT - y)
    background_width = int(background_height * background_ratio)

    # Redimensiona a figura
    background_size = (background_width, background_height)
    background = background.resize(background_size)

    # Cola a figura na imagem da tela
    canvas.paste(background, (x, y))

    return canvas, draw


def draw_images(canvas, draw, images):
    for image in images:
        x = float(image.get('x')) * difSize
        y = float(image.get('y')) * difSize

        image_path = path_assets + image.get('path')

        new_image = Image.open(image_path).convert("RGBA")

        if image.get("scale_x") == '-1':
            new_image = new_image.transpose(Image.ROTATE_90)

        if image.get("scale_y") == '-1':
            new_image = new_image.transpose(Image.ROTATE_180)
            new_image = ImageOps.mirror(new_image)

            y = y - global_variables.WINDOW_HEIGHT

        if image.get("rotation") == '1':
            new_image = new_image.transpose(Image.ROTATE_180)
            new_image = ImageOps.mirror(new_image)

        new_image_height = int(new_image.height * difSize)
        new_image_width = int(new_image.width * difSize)

        new_image_size = (new_image_width, new_image_height)
        new_image = new_image.resize(new_image_size)

        canvas.paste(new_image, (int(x), int(y)), new_image)

    return canvas, draw


def draw_texts(draw, prints):
    for text in prints:
        font = None
        for font_input in global_variables.fonts:
            if font_input.get('name') == text.get('font'):
                path_font = path_assets + font_input.get('path')
                font = ImageFont.truetype(path_font, int(float(font_input.get('size')) * difSize))

        if font is None:
            exit('Fonte nao encontrada')

        if text.get('align') == 'center':
            _, _, w, h = draw.textbbox((0, 0), text.get('text'), font=font)
            x = (global_variables.WINDOW_WIDTH - w) / 2
        else:
            x = text.get('x')

        draw.text((x, float(text.get('y')) * difSize), text.get('text'), font=font)


def create_image():
    for i in range(1, global_variables.SAMPLES_NUM + 1):
        # Importando as variáveis dos módulos
        images = importlib.import_module("data." + str(i) + ".images")
        prints = importlib.import_module("data." + str(i) + ".prints")

        # Criando Canvas
        canvas = Image.new(mode="RGB", size=(
            global_variables.WINDOW_WIDTH, global_variables.WINDOW_HEIGHT))

        draw = ImageDraw.Draw(canvas)

        canvas, draw = draw_background_image(
            canvas, draw, images.background_images[0])

        canvas, draw = draw_images(
            canvas, draw, images.images)

        canvas, draw = draw_background_image(
            canvas, draw, images.background_images[1])

        draw_texts(draw, prints.prints)

        canvas.save('data/' + str(i) + '/imagem_recriada-' + str(i) + '.png')
        print("Imagem gerada: " + str(i))


if __name__ == "__main__":
    create_image()
