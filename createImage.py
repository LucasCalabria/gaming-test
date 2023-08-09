import compareImages

from PIL import Image
from PIL import ImageFont, ImageDraw

from data import global_variables
from data import images
from data import prints

difSize = global_variables.WINDOW_WIDTH / global_variables.VIRTUAL_WIDTH

path_assets = 'assets/'

# TODO
#  Corrigir variaveis hardcoded,
#  Fazer masi comparacoes das imagens,
#  Pegar um numero maior de amostras
#  Aplicar para outras telas do jogo


def draw_background():
    canvas = Image.new(mode="RGB", size=(global_variables.WINDOW_WIDTH, global_variables.WINDOW_HEIGHT))
    draw = ImageDraw.Draw(canvas)

    for background_image in images.background_images:
        x = int(float(background_image.get('x')) * difSize)
        y = int(float(background_image.get('y')) * difSize)
        image_path = path_assets + 'imagens/' + background_image.get('path')

        background = Image.open(image_path)
        background_ratio = background.width / background.height

        background_height = int(global_variables.WINDOW_HEIGHT - y)
        background_width = int(background_height * background_ratio)

        background_size = (background_width, background_height)
        background = background.resize(background_size)

        canvas.paste(background, (x, y))

    return canvas, draw


def draw_texts(draw):
    for text in prints.prints:
        font = None
        for font_input in global_variables.fonts:
            if font_input.get('name') == text.get('font'):
                path_font = path_assets + font_input.get('path')
                font = ImageFont.truetype(path_font, int(int(font_input.get('size')) * difSize))

        if font is None:
            exit('Fonte nao encontrada')

        if text.get('align') == 'center':
            _, _, w, h = draw.textbbox((0, 0), text.get('text'), font=font)
            x = (global_variables.WINDOW_WIDTH - w) / 2
        else:
            x = text.get('x')

        draw.text((x, int(text.get('y')) * difSize), text.get('text'), font=font)


def create_image():
    canvas, draw = draw_background()
    draw_texts(draw)
    canvas.save('data/imagem_recriada.png')
    print("Imagem gerada!")


if __name__ == "__main__":
    create_image()
