<template>
  <nav class="bottom-navbar">
    <div class="bottom-navbar-buttons">
      <slot v-if="!store.bottomNavbarContent.value">
        <p>Information related to the current subapp selected.</p>
      </slot>
      <component
        v-else
        :is="store.bottomNavbarContent.value"
        @how-to-use="emitHowToUse"
        @create-election="emitCreateElection"
      />
    </div>
  </nav>
</template>

<script setup lang="ts">
import { store } from "../store";

function emitHowToUse() {
  // Call the method from the store
  store.openHowToUseModal?.();
}

function emitCreateElection() {
  // Call the method from the store
  store.openNewElectionModal?.();
}
</script>

<style scoped>
.bottom-navbar {
  position: fixed;
  bottom: 0;
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

.bottom-navbar-buttons {
  display: flex;
  justify-content: space-around;
  width: 100%;
}

.bottom-navbar-buttons button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.bottom-navbar-buttons button:hover {
  background-color: #45a049;
}

.bottom-navbar-buttons button:nth-child(1) {
  background-color: #ffa500; /* Matches top how-to-use button */
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.bottom-navbar-buttons button:nth-child(1):hover {
  background-color: #ff9900;
}

.bottom-navbar-buttons button:nth-child(2) {
  background-color: #4caf50; /* Matches top create-election button */
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  margin-left: 10px;
}

.bottom-navbar-buttons button:nth-child(2):hover {
  background-color: #45a049;
}
</style>
