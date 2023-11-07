
# Meme-GPT / GPT表情包生成器

This is a simple meme generator built with Flask, which utilizes OpenAI's API to generate descriptions and captions for uploaded images.

这是一个使用 Flask 构建的简单表情包生成器，它利用 OpenAI 的 API 为上传的图片生成描述和标题。

<p float="left">
  <img src="sample0.png" alt="sample0" width="45%" />
  <img src="sample1.png" alt="sample1" width="45%" />
</p>

## Features / 功能

1. Upload an image and get a descriptive caption / 上传图片并获得描述性标题
2. Generate interesting meme text based on the image description / 根据图片描述生成有趣的表情包文案
3. Download or share the final meme / 下载或分享最终的表情包

## Dependencies / 依赖

- Flask
- OpenAI
- Pillow

## Installation / 安装

1. Clone this repository / 克隆此仓库
2. Create a `.env` file in the project root directory with the following environment variables / 在项目根目录下创建 `.env` 文件并设置以下环境变量：

```
OPENAI_API_KEY=your_openai_api_key
```

3. Install dependencies / 安装依赖：
```
pip install -r requirements.txt
```
4. Run the application / 运行应用：
```
python app.py
```
5. Access in your browser / 在浏览器中访问：[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Usage / 使用方法

1. Upload an image on the homepage / 在首页上传一张图片
2. Click the "Generate Meme" button / 点击“生成表情包”按钮
3. View the generated meme text and image, download or share / 查看生成的表情包文案和图片，下载或分享

## File Structure / 文件结构

- `app.py`: Contains the main Flask application code / 包含主要的 Flask 应用程序代码
- `templates/`: Directory containing HTML templates for the application / 包含应用程序 HTML 模板的目录
   - `index.html`: For image upload / 用于图片上传
   - `result.html`: For displaying the generated meme / 用于展示生成的表情包

## Notes / 注意事项

1. Ensure you have the OpenAI API key before running the application / 运行应用程序前请确保您拥有 OpenAI API 密钥。
2. Monitor your API usage to avoid incurring unexpected costs / 监控您的 API 使用情况以避免产生意外费用。
3. This project is for educational and personal use only. Do not use it for commercial purposes without permission / 本项目仅供教育和个人使用。未经许可，请勿用于商业用途。
