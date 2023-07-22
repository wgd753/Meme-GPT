import os
from dotenv import load_dotenv
import base64
from io import BytesIO

from flask import Flask, request, render_template, send_file
import openai
import replicate
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# Configure OpenAI and Replicate API tokens
load_dotenv()
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

        # 将生成的图片转换为Base64编码的字符串
        base64_image = convert_image_to_base64(image)
        
        # 将图片的Base64编码和生成的文本作为变量传递给 render_template 函数
        return render_template("result.html", base64_image=base64_image, meme_text=meme_text)

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

def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode("utf-8")

if __name__ == "__main__":
    app.run()
