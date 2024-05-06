from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # フロントエンドのオリジンを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダを許可
)

# 画像を一時的に保存し、ピクセルサイズを受け取って処理する
@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...), pixelSize: int = Form(10)):
    # 画像を一時的に保存
    contents = await file.read()
    with open("temp_image.png", "wb") as f:
        f.write(contents)

    # 画像をドット絵に変換して保存
    pixel_art_stream = convert_to_pixel_art("temp_image.png", pixelSize)
    with open("pixel_art_image.png", "wb") as f:
        f.write(pixel_art_stream.getbuffer())

    return {"message": "File uploaded and processed"}

# 特定のピクセルサイズで変換された画像を返す
@app.get("/image/")
async def get_image():
    # 変換された画像を返す
    return FileResponse("pixel_art_image.png", media_type="image/png")

def convert_to_pixel_art(image_path: str, pixelSize: int):
    with Image.open(image_path) as img:
        original_size = img.size
        small_img = img.resize(
            (original_size[0] // pixelSize, original_size[1] // pixelSize),
            Image.Resampling.NEAREST
        )
        pixel_art_img = small_img.resize(original_size, Image.Resampling.NEAREST)
        img_byte_arr = io.BytesIO()
        pixel_art_img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr
