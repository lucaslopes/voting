<template>
  <nav class="top-navbar">
    <div class="left-buttons">
      <button @click="toggleLeftSidebar">☰</button>
    </div>
    <div class="navbar-content">
      <component
        v-if="store.topNavbarContent.value"
        :is="store.topNavbarContent.value"
      />
      <slot v-else>
        <h1>Loading...</h1>
        <!-- Fallback content -->
      </slot>
    </div>
    <div class="nav-buttons">
      <button @click="toggleRightSidebar">⚙</button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { store } from "../store";
import { defineEmits } from "vue";

const emit = defineEmits(["toggle-left-sidebar", "toggle-right-sidebar"]);

function toggleLeftSidebar() {
  emit("toggle-left-sidebar");
}

function toggleRightSidebar() {
  emit("toggle-right-sidebar");
}
</script>

<style scoped>
.top-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background-color: #333;
  color: #fff;
  display: flex;
  align-items: center;
  padding: 0 1rem;
  z-index: 1000;
}

.left-buttons,
.nav-buttons {
  display: flex;
  align-items: center;
}

.navbar-content {
  flex: 1;
  display: flex;
  justify-content: center;
}

.navbar-content h1 {
  margin: 0;
  font-size: 20px;
}

.navbar-content h1 a {
  color: #4caf50; /* first link is green */
  text-decoration: none;
  margin: 0 5px;
}

.navbar-content h1 a:nth-child(2) {
  color: #ffa500; /* second link is orange */
}

.navbar-content h1 a:hover {
  text-decoration: underline;
}

.left-buttons button,
.nav-buttons button {
  background-color: #015cc8;
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  margin: 0 5px;
  cursor: pointer;
  font-size: 14px;
}

.left-buttons button:hover,
.nav-buttons button:hover {
  background-color: #4c9fff;
}
</style>
