<template>
  <div class="content">
    <!-- Chart -->
    <div class="chart-container">
      <canvas id="pieChart" ref="pieChartCanvas"></canvas>
    </div>

    <!-- Slice List -->
    <ul class="slice-list">
      <li
        class="slice-item"
        v-for="(slice, index) in currentNode.slices"
        :key="index"
      >
        <button class="move-up" title="Move Up" @click="moveUp(index)">
          <font-awesome-icon icon="arrow-up" />
        </button>
        <button class="move-down" title="Move Down" @click="moveDown(index)">
          <font-awesome-icon icon="arrow-down" />
        </button>
        <input
          type="color"
          class="slice-color"
          v-model="slice.color"
          @input="updateChart"
        />
        <input
          type="text"
          class="slice-label"
          v-model="slice.name"
          @input="updateChart"
          placeholder="Project Name"
        />
        <input
          type="range"
          class="slice-percentage"
          min="0"
          max="100"
          v-model.number="slice.percentage"
          @input="updateChart"
        />
        <span class="percentage-display">{{ slice.percentage }}%</span>
        <button class="drill-down" @click="drillDown(slice)">
          <font-awesome-icon icon="search-plus" />
        </button>
        <button class="remove-slice" @click="removeSlice(index)">
          <font-awesome-icon icon="trash" />
        </button>
      </li>
    </ul>

    <!-- Add Slice -->
    <div class="add-slice-container">
      <button @click="addSlice">Add Project</button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {
  defineComponent,
  ref,
  reactive,
  onMounted,
  onUnmounted,
  markRaw,
  h,
} from "vue";
import Chart from "chart.js/auto";
import { eventBus } from "../eventBus";
import { store, type TreeNode } from "../store";
import ParticipatorySidebar from "../components/ParticipatorySidebar.vue";
import Breadcrumb from "../components/BreadcrumbComponent.vue";

const ParticipatoryHeader = markRaw(
  defineComponent({
    name: "ParticipatoryHeader",
    render() {
      return h("h1", "Participatory Budgeting");
    },
  }),
);

const rootNode = store.rootNode;
const currentNode = store.currentNode;

const pieChartCanvas = ref<HTMLCanvasElement | null>(null);
let pieChart: Chart | null = null;

function updateView() {
  updateChart();
}

function updateChart() {
  if (pieChart) {
    const labels = [];
    const data = [];
    const backgroundColor = [];
    let remaining = 100;

    currentNode.value.slices.forEach((slice: TreeNode, index: number) => {
      if (!slice.name.startsWith("Project")) {
        slice.name = `Project ${currentNode.value.name.split(" ")[1]}-${String.fromCharCode(65 + index)}`;
      }
      labels.push(slice.name);
      const value = remaining * ((slice.percentage ?? 0) / 100);
      data.push(value);
      remaining -= value;
      backgroundColor.push(slice.color || "#cccccc");
    });

    if (remaining > 0) {
      labels.push("Remaining");
      data.push(remaining);
      backgroundColor.push("#cccccc");
    }

    pieChart.data.labels = labels;
    pieChart.data.datasets[0].data = data;
    pieChart.data.datasets[0].backgroundColor = backgroundColor;
    pieChart.update();
  }
}

function addSlice() {
  const newName = `Project ${currentNode.value.name.split(" ")[1]}-${String.fromCharCode(65 + currentNode.value.slices.length)}`;
  const newSlice = reactive({
    name: newName,
    percentage: 100,
    color: "#" + Math.floor(Math.random() * 16777215).toString(16),
    slices: [],
    parent: currentNode.value,
  });
  currentNode.value.slices.push(newSlice);
  updateView();
}

function moveUp(index: number) {
  if (index > 0) {
    const slices = currentNode.value.slices;
    const temp = slices[index - 1];
    slices[index - 1] = slices[index];
    slices[index] = temp;
    updateView();
  }
}

function moveDown(index: number) {
  const slices = currentNode.value.slices;
  if (index < slices.length - 1) {
    const temp = slices[index + 1];
    slices[index + 1] = slices[index];
    slices[index] = temp;
    updateView();
  }
}

function drillDown(slice: TreeNode) {
  currentNode.value = slice;
  updateView();
}

function removeSlice(index: number) {
  currentNode.value.slices.splice(index, 1);
  updateView();
}

function goUpLevel() {
  if (currentNode.value.parent) {
    currentNode.value = currentNode.value.parent;
    updateView();
  }
}

function navigateTo(node: any) {
  currentNode.value = node;
  updateView();
}

onMounted(() => {
  if (pieChartCanvas.value) {
    const ctx = pieChartCanvas.value.getContext("2d");
    if (ctx) {
      pieChart = new Chart(ctx, {
        type: "pie",
        data: {
          labels: [],
          datasets: [
            {
              data: [],
              backgroundColor: [],
            },
          ],
        },
        options: {
          onClick: (event, elements) => {
            if (elements.length > 0) {
              const index = elements[0].index;
              const slice = currentNode.value.slices[index];
              if (slice) {
                currentNode.value = slice;
                updateView();
              }
            }
          },
        },
      });
      updateView();
    }
  }
  eventBus.on("data-imported", updateView);
  if (store.topNavbarContent) {
    store.topNavbarContent.value = ParticipatoryHeader; // Set the specific header
  }
  store.bottomNavbarContent.value = Breadcrumb;
  store.rightSidebarContent.value = ParticipatorySidebar;
  currentNode.value = store.rootNode;
  store.navigateTo = navigateTo;
  store.goUpLevel = goUpLevel;
  updateView();
});

onUnmounted(() => {
  store.rightSidebarContent.value = null;
  store.bottomNavbarContent.value = null;
  if (store.topNavbarContent) {
    store.topNavbarContent.value = null; // Reset on unmount
  }
  eventBus.off("data-imported", updateView);
});
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  background-color: #f0f0f5;
}

.content {
  margin-top: 60px;
  margin-bottom: 60px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.controls {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.controls button {
  background: none;
  border: none;
  color: black;
  font-size: 20px;
  cursor: pointer;
}

.chart-container {
  width: 400px;
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.slice-list {
  list-style-type: none;
  padding: 0;
  width: 100%;
  max-width: 600px;
}

.slice-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background: #d8e2dc;
  margin-bottom: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.slice-item i {
  font-size: 20px;
  cursor: pointer;
}

.add-slice-container {
  margin-top: 20px;
}

.percentage-display {
  width: 50px;
  text-align: right;
}

.breadcrumb {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.breadcrumb button {
  background: none;
  border: none;
  color: white;
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
  color: white;
}

.breadcrumb span {
  cursor: pointer;
  color: white;
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

.move-up,
.move-down,
.drill-down,
.remove-slice {
  background: none;
  border: none;
  cursor: pointer;
}

.slice-color,
.slice-label,
.slice-percentage {
  flex: 1;
}

.slice-label {
  width: 150px;
}

.slice-percentage {
  flex: 1;
}

/* Sidebar styles for the new content */
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
