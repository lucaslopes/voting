<template>
  <div class="bottom-navbar-buttons">
    <span class="stats-info">
      Total Elections: {{ totalElections }} | Total Votes: {{ totalVotes }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { store } from "../store";

const totalElections = computed(() => store.totalElections.value || 0);
const totalVotes = computed(() => store.totalVotes.value || 0);
</script>

<style scoped>
.stats-info {
  color: #fff;
  font-weight: bold;
}
</style>
