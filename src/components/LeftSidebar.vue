<template>
  <div class="left-sidebar" :class="{ open: isOpen }">
    <ul class="nav-list">
      <li :class="{ active: $route.name === 'RatedEVoting' }">
        <router-link to="/voting">
          <font-awesome-icon icon="poll" />
          Rated e-Voting
        </router-link>
      </li>
      <li :class="{ active: $route.name === 'ParticipatoryBudgeting' }">
        <router-link to="/budgeting">
          <font-awesome-icon icon="hand-holding-usd" />
          Participatory Budgeting
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
const { isOpen } = defineProps<{ isOpen: boolean }>();
</script>

<style scoped>
.left-sidebar {
  position: fixed;
  top: 60px;
  bottom: 60px;
  left: -250px;
  width: 250px;
  background-color: #333;
  color: #fff;
  overflow-y: auto;
  transition: left 0.3s;
  z-index: 10000;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.3);
  font-family: Arial, sans-serif;
}

.left-sidebar.open {
  left: 0;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-list li {
  border-bottom: 1px solid #444;
}

.nav-list li a {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #fff;
  padding: 15px 20px;
  text-decoration: none;
  font-size: 16px;
  transition: background-color 0.3s;
}

.nav-list li a:hover {
  background-color: #444;
}

.nav-list li.active a {
  background-color: #4caf50;
  font-weight: bold;
  color: #fff;
}
</style>
