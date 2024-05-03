<script setup lang="ts">
import { ref } from 'vue'
const model = ref(null)
const imageUrl = ref('')
const OnImage: boolean = false

const showItem = () => {
  const file = model.value
  if (file) {
    imageUrl.value = URL.createObjectURL(file)
  }
}

const clearItem = () => {
  imageUrl.value = ''
}
</script>

<template>
  <div class="convert-image">
    <h2>This is a convert image page</h2>
    <q-file
      filled
      bottom-slots
      accept=".jpg, .jpeg, .JPEG, .png"
      v-model="model"
      label="Label"
      counter
      class="w-30"
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
    <q-btn color="primary" icon-right="image" label="Show Image" @click="showItem" />
    <div class="w-30">
      <img v-if="imageUrl" :src="imageUrl" alt="" class="w-100" />
    </div>
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
}
.w-100 {
  width: 100%;
}
.w-30 {
  min-width: 300px;
  width: 30%;
}
/* } */
</style>
