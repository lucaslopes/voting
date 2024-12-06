<template>
  <ul class="sidebar-actions">
    <li @click="$emit('how-to-use')">
      <font-awesome-icon icon="info-circle" />
      How to Use
    </li>
    <li @click="$emit('create-election')">
      <font-awesome-icon icon="plus-circle" />
      Create Election
    </li>
  </ul>
</template>

<script setup lang="ts">
import { defineEmits } from "vue";
defineEmits(["how-to-use", "create-election"]);
</script>

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
  border-bottom: 1px solid #ddd;
}

.sidebar-actions li:hover {
  background-color: #e8f5e9;
}

.sidebar-actions li font-awesome-icon {
  color: #4caf50;
}
</style>
