import os
import base64
from io import BytesIO

from flask import Flask, request, render_template, send_file
import openai
import replicate
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# Configure OpenAI and Replicate API tokens
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_data = request.files['image'].read()
        image_description = get_image_description(image_data)
        meme_text = generate_meme_text(image_description)

        # 将 image_data 转换为 Image 对象
        image = Image.open(BytesIO(image_data))

        final_image = add_text_to_image(image, meme_text)
        
        # 将生成的图片转换为Base64编码的字符串
        base64_image = convert_image_to_base64(final_image)
        
        # 将图片的Base64编码作为变量传递给 render_template 函数
        return render_template("result.html", base64_image=base64_image)

    return render_template('index.html')




def get_image_description(image_data):
    client = replicate.Client(api_token=REPLICATE_API_TOKEN)
    output = client.run(
        "andreasjansson/blip-2:4b32258c42e9efd4288bb9910bc532a69727f9acd26aa08e175713a0a857a608",
        input={"image": BytesIO(image_data)}
    )
    return output  # 直接返回 output 字符串



def generate_meme_text(image_description):
    prompt = f"你现在是一个表情包文案生成器，你需要根据图片描述直接给出反讽，有趣的表情包文案，直接给出一句文案即可，字数简短，不需要多余的描述。 图片描述: {image_description}"
    query = "给我一句有趣的表情包文案。"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": query},
        ],
    )

    meme_text = response.choices[0].message.content.strip()
    return meme_text


def wrap_text(text, font, max_width):
    lines = []
    if not text:
        return lines

    current_line = ''
    for char in text:
        width, _ = font.getsize(current_line + char)
        if width <= max_width:
            current_line += char
        else:
            lines.append(current_line)
            current_line = char
            width, _ = font.getsize(current_line)  # 重新计算宽度
    if current_line:
        lines.append(current_line)
    return lines

def add_text_to_image(image, text):
    width, height = image.size

    # 动态设置字体大小
    font_size = int(min(width, height) * 0.06)  # 根据图像尺寸计算字体大小，可以调整0.06这个系数
    font = ImageFont.truetype("simhei.ttf", font_size)

    draw = ImageDraw.Draw(image)

    max_text_width = int(width * 0.8)
    lines = wrap_text(text, font, max_text_width)
    text_height = font.getsize(lines[0])[1]

    max_line_width = 0
    for line in lines:
        line_width, _ = font.getsize(line)
        max_line_width = max(max_line_width, line_width)

    # 添加白色背景矩形
    rectangle_x = int(width * 0.02)
    rectangle_y = int(height * 0.05)
    rectangle_width = int(max_line_width + text_height * 0.4)
    rectangle_height = int((text_height * 1.2) * len(lines) + text_height * 0.2)
    draw.rectangle(
        [rectangle_x, rectangle_y, rectangle_x + rectangle_width, rectangle_y + rectangle_height],
        alpha = 64  # 透明度，范围为 0 至 255，128 表示半透明
        fill=(255, 255, 255, alpha)
    )

    # 添加黑色文本
    text_x = int(rectangle_x + text_height * 0.2)
    text_y = int(rectangle_y + text_height * 0.1)
    for line in lines:
        draw.text((text_x, text_y), line, font=font, fill=(0, 0, 0))
        text_y += text_height * 1.2
    return image

def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode("utf-8")


if __name__ == "__main__":
    app.run()
