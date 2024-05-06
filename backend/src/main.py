from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
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

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    # 画像を一時的に保存
    contents = await file.read()
    with open("temp_image.png", "wb") as f:
        f.write(contents)
    return {"filename": file.filename}

def convert_to_pixel_art(image_path: str, pixel_size: int):
    # 画像を開く
    with Image.open(image_path) as img:
        # 元のサイズを記録
        original_size = img.size

        # ピクセルサイズに合わせてサイズを小さくする
        small_img = img.resize(
            (original_size[0] // pixel_size, original_size[1] // pixel_size),
            Image.Resampling.NEAREST  # Pillow 7.0.0以降はこちらを使用
        )

        # 元のサイズに戻す
        pixel_art_img = small_img.resize(original_size, Image.Resampling.NEAREST)

        # 結果を一時的なバイナリストリームに保存
        img_byte_arr = io.BytesIO()
        pixel_art_img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return img_byte_arr

@app.get("/image/")
async def get_image():
    # 画像をドット絵に変換
    pixel_art_stream = convert_to_pixel_art("temp_image.png", 10)  # pixel_sizeは適宜調整
    return StreamingResponse(pixel_art_stream, media_type="image/png")
