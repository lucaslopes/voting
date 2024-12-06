<template>
  <div id="app">
    <TopNavbar
      @toggle-left-sidebar="toggleLeftSidebar"
      @toggle-right-sidebar="toggleRightSidebar"
    />

    <LeftSidebar :isOpen="isLeftSidebarOpen" />
    <RightSidebar :isOpen="isRightSidebarOpen" />

    <div class="main-content">
      <div class="content">
        <!-- The main content will be rendered here -->
        <RouterView />
      </div>
    </div>

    <BottomNavbar />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { RouterView } from "vue-router";
import LeftSidebar from "./components/LeftSidebar.vue";
import RightSidebar from "./components/RightSidebar.vue";
import TopNavbar from "./components/TopNavbar.vue";
import BottomNavbar from "./components/BottomNavbar.vue";

const isLeftSidebarOpen = ref(false);
const isRightSidebarOpen = ref(false);

function toggleLeftSidebar() {
  isLeftSidebarOpen.value = !isLeftSidebarOpen.value;
}

function toggleRightSidebar() {
  isRightSidebarOpen.value = !isRightSidebarOpen.value;
}
</script>

<style scoped>
#app {
  position: relative;
  overflow-x: hidden;
}

.main-content {
  /* Adjusted to remove flex display */
  display: flex;
}

.content {
  min-height: 100vh;
  flex: 1;
}
</style>
