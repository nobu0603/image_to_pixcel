<script setup lang="ts">
import { ref } from 'vue'
const leftDrawerOpen = ref(false)
</script>

<template>
  <q-layout view="lHh Lpr lFf" class="bg-white">
    <q-header elevated class="bg-grey-2 text-primary">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          @click="leftDrawerOpen = !leftDrawerOpen"
          aria-label="Menu"
          icon="menu"
        />

        <q-toolbar-title> Image to Pixcel App </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered class="bg-grey-2">
      <q-list>
        <q-item-label header>Navigation</q-item-label>
        <q-item clickable rel="noopener" to="/">
          <q-item-section avatar>
            <q-icon name="home" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Home</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable rel="noopener" to="/convert_image">
          <q-item-section avatar>
            <q-icon name="change_circle" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Convert Image</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable rel="noopener" to="/how_to_use">
          <q-item-section avatar>
            <q-icon name="question_mark" />
          </q-item-section>
          <q-item-section>
            <q-item-label>How to use</q-item-label>
          </q-item-section>
        </q-item>
        <q-item
          clickable
          target="_blank"
          rel="noopener"
          href="https://github.com/nobu0603/image_to_pixcel"
        >
          <q-item-section avatar>
            <q-icon name="code" />
          </q-item-section>
          <q-item-section>
            <q-item-label>GitHub</q-item-label>
            <q-item-label caption>github.com/nobu0603/image_to_pixcel</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>
