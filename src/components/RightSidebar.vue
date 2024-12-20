<template>
  <div class="right-sidebar" :class="{ open: isOpen }">
    <div class="config-options">
      <component
        v-if="store.rightSidebarContent.value"
        :is="store.rightSidebarContent.value"
        @export="handleExport"
        @import="handleImport"
        @about-modal="handleAbout"
        @how-to-use="handleHowToUse"
        @create-election="handleCreateElection"
      />
      <slot v-else>
        <!-- Default content -->
        <p>No actions available</p>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { store } from '../store'

  const { isOpen } = defineProps<{ isOpen: boolean }>()

  function handleExport() {
    store.exportJSON?.()
  }

  function handleImport(event: Event) {
    store.importJSON?.(event)
  }

  // Add these new handlers:
  function handleAbout() {
    store.openAboutModal?.()
  }

  function handleHowToUse() {
    store.openHowToUseModal?.()
  }

  function handleCreateElection() {
    store.openNewElectionModal?.()
  }
</script>

<style scoped>
  .right-sidebar {
    position: fixed;
    top: 60px;
    bottom: 60px;
    right: -250px;
    width: 250px;
    background-color: #f4f4f4;
    overflow-y: auto;
    transition: right 0.3s;
    z-index: 11000; /* Ensure it's higher than other elements */
    box-shadow: -2px 0 5px rgba(0, 0, 0, 0.3); /* Add shadow on the left side */
  }

  .right-sidebar.open {
    right: 0;
  }
</style>
