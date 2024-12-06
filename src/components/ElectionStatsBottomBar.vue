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

// Assuming store or props can give us the data. If not, we can pass it as props.
// In RatedEVoting.vue, you have `elections` ref that we can pass in.
// We'll pass it from RatedEVoting via store or props. Let's do store trick:
// We'll store these counts in store or use a global variable.
// For a quick solution, let's have store or a global variable set onMounted.

const totalElections = computed(() => store.totalElections || 0);
const totalVotes = computed(() => store.totalVotes || 0);
</script>

<style scoped>
.stats-info {
  color: #fff;
  font-weight: bold;
}
</style>
