<template>
  <div class="breadcrumb">
    <button id="go-up-level" title="Go Back" @click="goUpLevel && goUpLevel()">
      <font-awesome-icon icon="arrow-left" />
    </button>
    <div class="breadcrumb-path">
      <template v-for="(node, index) in breadcrumbPath" :key="index">
        <span @click="node.name && navigateTo && navigateTo(node)">{{
          node.name
        }}</span>
        <span v-if="index < breadcrumbPath.length - 1" class="separator">
          <font-awesome-icon icon="angle-right" />
        </span>
      </template>
    </div>
  </div>
</template>

<!-- BreadcrumbComponent.vue -->
<script lang="ts" setup>
import { computed } from "vue";
import { store, type TreeNode } from "../store";

// Use store variables
const currentNode = computed(() => store.currentNode.value);
const navigateTo = store.navigateTo;
const goUpLevel = store.goUpLevel;

const breadcrumbPath = computed(() => {
  if (!currentNode.value) return [];
  let node: TreeNode | null = currentNode.value;
  const path: TreeNode[] = [];
  while (node) {
    path.unshift(node);
    node = node.parent;
  }
  return path;
});
</script>

<style scoped>
/* Breadcrumb styles from ParticipatoryBudgeting.vue */
.breadcrumb {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.breadcrumb button {
  background: none;
  border: none;
  color: black;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.breadcrumb-path {
  display: flex;
  align-items: center;
  gap: 10px;
}

.breadcrumb .separator {
  font-family: "Font Awesome 5 Free";
  font-weight: 900;
  color: black;
}

.breadcrumb span {
  cursor: pointer;
  color: black;
  padding: 5px 10px;
  border-radius: 5px;
  transition:
    background-color 0.3s,
    color 0.3s;
}

.breadcrumb span:hover {
  background-color: #94d2bd;
  color: #005f73;
}
</style>
