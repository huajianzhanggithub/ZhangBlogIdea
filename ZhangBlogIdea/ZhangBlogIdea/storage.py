from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile


def convert_image_to_file(image, name):
    temp = BytesIO()
    image.save(temp, format='PNG')
    file_size = temp.tell()
    return InMemoryUploadedFile(temp, None, name, 'image/png', file_size, None)


def watermark_with_text(file_obj, text, color, fontfamily=None):
    image = Image.open(file_obj).convert('RGBA')
    width, height = image.size
    zoom = 825.0 / width
    width, height = int(width * zoom), int(height * zoom)
    print(width, height)
    image.thumbnail((width, height), Image.ANTIALIAS)
    draw = ImageDraw.Draw(image)
    margin = 10
    if fontfamily:
        font = ImageFont.truetype(fontfamily, int(height), encoding='utf-8')
    else:
        font = None
    textWidth, textHeight = draw.textsize(text, font)
    x = width - textWidth - margin  # 计算横轴位置
    y = height - textHeight - margin
    draw.text((x, y), text, color, font)
    return image


class WatermarkStorage(FileSystemStorage):
    def save(self, name, content, max_length=None):
        if 'image' in content.content_type:
            # 加水印
            image = watermark_with_text(content, 'RememberTheLight', 'red')
            content = convert_image_to_file(image, name)

        return super().save(name, content, max_length=max_length)
