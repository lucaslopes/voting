<script lang="ts" setup>
import { defineEmits } from "vue";

defineEmits(["export", "import"]);
</script>

<template>
  <ul class="sidebar-actions">
    <li @click="$emit('export')">
      <font-awesome-icon icon="download" />
      Export Budget
    </li>
    <li>
      <label>
        <font-awesome-icon icon="upload" />
        <span>Import Budget</span>
        <input
          type="file"
          accept=".json"
          @change="$emit('import', $event)"
          style="display: none"
        />
      </label>
    </li>
  </ul>
</template>

<style scoped>
.sidebar-actions {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar-actions li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.sidebar-actions li:hover {
  background-color: #e8f5e9;
}
</style>
