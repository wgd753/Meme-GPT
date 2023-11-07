import os
from dotenv import load_dotenv
import base64
import requests
from io import BytesIO

from flask import Flask, request, render_template, flash, redirect
import openai
from PIL import Image
from werkzeug.utils import secure_filename
import imghdr

app = Flask(__name__)

# Configure OpenAI API tokens and set Flask configurations
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
app.secret_key = 'your_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20MB limit

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image_stream(stream):
    header = stream.read(512)  # read the first 512 bytes
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('image')
        if file is None or file.filename == '':
            flash('没有选择文件')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            extension = validate_image_stream(file.stream)
            if not extension:
                flash('无效的图像格式')
                return redirect(request.url)
            filename = secure_filename(file.filename)
            image_data = file.read()
            image_description = get_image_description(image_data) or "未能识别出图片内容。"
            base64_image = convert_image_to_base64(image_data)
            return render_template("result.html", base64_image=base64_image, meme_text=image_description)
        else:
            flash('文件类型不被允许')
            return redirect(request.url)
    return render_template('index.html')

def get_image_description(image_data):
    base64_image = base64.b64encode(image_data).decode('utf-8')
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "你现在是一个表情包文案生成器，你需要根据图片描述直接给出反讽，有趣的表情包文案，直接给出一句文案即可，字数简短，不需要多余的描述。"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        # 将响应的内容打印出来，以便调试
        print("API response:", response.json())
        return response.json().get('choices', [{}])[0].get('message', {}).get('content')
    else:
        # 打印出错误的响应状态码和信息，以便调试
        print(f"Error: {response.status_code}, Response: {response.text}")
        return None

def convert_image_to_base64(image_data):
    buffered = BytesIO()
    image = Image.open(BytesIO(image_data))
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

if __name__ == "__main__":
    app.run()