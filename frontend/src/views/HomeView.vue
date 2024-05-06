<script setup lang="ts">
import { ref } from 'vue'
import html2canvas from 'html2canvas'

const model = ref(null)
const pixelSize = ref(1)
const imageUrl = ref('')
let imageStyle = {}
let uploadImageStyle = {}
const imageDiv = ref<HTMLElement | null>(null)
const uploadImageUrl = ref('')
const imgOuter = ref(null)

// デバイスからアップロードした画像を画面に表示する
const showItem = () => {
  const file = model.value
  if (file) {
    imageUrl.value = URL.createObjectURL(file)
    imageStyle = {
      backgroundImage: `url('${imageUrl.value}')`,
      backgroundSize: 'cover',
      backgroundPosition: 'center center'
    }
  }
}

// ピクセルサイズのラベルを生成
const fnMarkerLabel = (val: number) => `${10 * val}px`

// 画像要素をキャンバス要素にしてAPIをコールし、返された画像を取得する
const uploadImage = async () => {
  if (!imageDiv.value) return
  const canvas = await html2canvas(imageDiv.value, {
    backgroundColor: null
  })
  canvas.toBlob(async (blob) => {
    if (!blob) return
    const currentPixelSize = pixelSize.value * 10
    const formData = new FormData()
    formData.append('file', blob, 'image.png')
    formData.append('pixelSize', currentPixelSize.toString())

    await fetch('http://localhost:8000/upload/', {
      method: 'POST',
      body: formData
    })
    await loadImage()
  })
}

const loadImage = async () => {
  const response = await fetch('http://localhost:8000/image/')
  const blob = await response.blob()
  uploadImageUrl.value = URL.createObjectURL(blob)
  uploadImageStyle = {
    backgroundImage: `url('${uploadImageUrl.value}')`,
    backgroundSize: 'cover',
    backgroundPosition: 'center center'
  }
}

// インプット内のクリアボタンクリック時に画像パスを削除する
const clearItem = () => {
  imageUrl.value = ''
}

// ダウンロードボタン
const captureAndDownload = async () => {
  if (!imgOuter.value) return

  const canvas = await html2canvas(imgOuter.value, {
    backgroundColor: null
  })
  const image = canvas.toDataURL('image/png')

  // ダウンロード用のaタグを生成
  const a = document.createElement('a')
  a.href = image
  a.download = 'pixcel-image.png'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}
</script>

<template>
  <div class="convert-image">
    <q-file
      filled
      bottom-slots
      accept=".jpg, .jpeg, .JPEG, .png"
      v-model="model"
      label="Label"
      counter
      class="object-size"
    >
      <template v-slot:prepend>
        <q-icon name="cloud_upload" @click.stop.prevent />
      </template>
      <template v-slot:append>
        <q-icon
          name="close"
          @click.stop.prevent="model = null"
          @click="clearItem"
          class="cursor-pointer"
        />
      </template>

      <template v-slot:hint> Field hint </template>
    </q-file>
    <q-btn
      v-if="model != null"
      color="primary"
      icon-right="image"
      label="Show Image"
      @click="showItem"
    />
    <div v-if="imageUrl" class="img-wrap border-around">
      <div class="img-outer" ref="imageDiv" :style="imageStyle"></div>
    </div>
    <div v-if="imageUrl" class="text-h6">Pixel Size</div>
    <q-slider
      v-if="imageUrl"
      v-model="pixelSize"
      :min="1"
      :max="5"
      :marker-labels="fnMarkerLabel"
      class="object-size"
    />
    <q-btn
      v-if="imageUrl"
      color="primary"
      icon-right="sync"
      label="Convert to Pixcel"
      @click="uploadImage"
    />
    <div v-if="uploadImageUrl" class="img-wrap border-around">
      <div ref="imgOuter" class="img-outer" :style="uploadImageStyle"></div>
    </div>
    <q-btn
      v-if="uploadImageUrl"
      color="primary"
      icon-right="download"
      label="Download Image"
      @click="captureAndDownload"
    />
  </div>
</template>

<style>
/* @media (min-width: 1024px) { */
.convert-image {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 24px;
  padding: 100px 0;
}
.w-100 {
  width: 100%;
}
.object-size {
  max-width: 500px;
  min-width: 300px;
  width: 30%;
}
.img-wrap {
  max-width: 500px;
  min-width: 300px;
  width: 30%;
  aspect-ratio: 1/1;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.img-outer {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
/* .img-wrap img {
  object-fit: contain !important;
} */
/* } */
</style>
