<template>
  <div class="content">
    <!-- Chart -->
    <div class="chart-container">
      <canvas id="pieChart" ref="pieChartCanvas"></canvas>
    </div>

    <!-- Slice List -->
    <ul class="slice-list">
      <li class="slice-item" v-for="(slice, index) in currentNode.slices" :key="index">
        <button class="move-up" title="Move Up" @click="moveUp(index)">
          <font-awesome-icon icon="arrow-up" />
        </button>
        <button class="move-down" title="Move Down" @click="moveDown(index)">
          <font-awesome-icon icon="arrow-down" />
        </button>
        <input type="color" class="slice-color" v-model="slice.color" @input="updateChart" />
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

  <!-- About Modal -->
  <div id="about-modal" v-if="showAboutModal" class="modal-overlay">
    <div class="modal-content">
      <button type="button" class="close-button" @click="closeAboutModal">&times;</button>
      <div class="modal-body">
        <p>
          This project was developed by
          <a href="https://lucaslopes.me/" target="_blank">Lucas Lopes</a> during the
          <a
            href="https://syftbox.openmined.org/datasites/lucaslopesf2@gmail.com/30DaysOfFLCode.html"
            target="_blank"
            >#30DaysOfFLCode</a
          >
          challenge organized by
          <a href="https://openmined.org/" target="_blank">OpenMined</a>.
        </p>
      </div>
    </div>
  </div>

  <!-- How to Use Modal -->
  <div id="how-to-use-modal" v-if="showHowToUseModal" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h2>How to Use</h2>
        <button type="button" class="close-button" @click="closeHowToUseModal">&times;</button>
      </div>
      <div class="modal-body">
        <ol>
          <li>
            <h3>
              Install
              <a
                href="https://syftbox-documentation.openmined.org/#installing-a-syftbox-api"
                target="_blank"
                >SyftBox</a
              >
            </h3>
            <p>
              Ensure <code>curl</code> is installed (refer to
              <a href="https://everything.curl.dev/install/linux.html" target="_blank">Linux</a>,
              <a href="https://everything.curl.dev/install/macos.html" target="_blank">MacOS</a>, or
              <a href="https://everything.curl.dev/install/windows/index.html" target="_blank"
                >Windows</a
              >
              guides if needed), then run this command in your terminal:
            </p>
            <div class="command-container">
              <div class="command">
                <code>curl -LsSf https://syftbox.openmined.org/install.sh | sh</code>
                <button @click="copyToClipboard(installCommand)">Copy</button>
              </div>
            </div>
          </li>
          <li>
            <h3>Set Up Voting API</h3>
            <p>Install the Voting API directly in your SyftBox by running:</p>
            <div class="command-container">
              <div class="command">
                <code>syftbox app install lucaslopes/voting</code>
                <button @click="copyToClipboard('syftbox app install lucaslopes/voting')">
                  Copy
                </button>
              </div>
            </div>
          </li>
          <li>
            <h3>Submit Budget</h3>
            <p>
              Move the exported <code>JSON</code> file in the folder:
              <strong
                ><code
                  >SyftBox/datasites/&lt;your@email.org&gt;/api_data/voting/budgets</code
                ></strong
              >
            </p>
          </li>
        </ol>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
  import { defineComponent, ref, reactive, onMounted, onUnmounted, markRaw, h } from 'vue'
  import Chart from 'chart.js/auto'
  import { eventBus } from '../eventBus'
  import { store, type TreeNode } from '../store'
  import ParticipatorySidebar from '../components/ParticipatorySidebar.vue'
  import Breadcrumb from '../components/BreadcrumbComponent.vue'

  const showAboutModal = ref(false)
  const showHowToUseModal = ref(false)
  const installCommand = ref('curl -LsSf https://syftbox.openmined.org/install.sh | sh')

  function openAboutModal() {
    console.log('openAboutModal')
    showAboutModal.value = true
  }

  function closeAboutModal() {
    showAboutModal.value = false
  }

  const openHowToUseModal = () => {
    showHowToUseModal.value = true
  }

  const closeHowToUseModal = () => {
    showHowToUseModal.value = false
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard
      .writeText(text)
      .then(() => {
        alert('Copied to clipboard!')
      })
      .catch((err) => {
        alert('Failed to copy: ' + err)
      })
  }

  const ParticipatoryHeader = markRaw(
    defineComponent({
      name: 'ParticipatoryHeader',
      render() {
        return h('h1', 'Participatory Budgeting')
      }
    })
  )

  const rootNode = store.rootNode
  const currentNode = store.currentNode

  const pieChartCanvas = ref<HTMLCanvasElement | null>(null)
  let pieChart: Chart | null = null

  function updateView() {
    updateChart()
  }

  function updateChart() {
    if (pieChart) {
      const labels = []
      const data = []
      const backgroundColor = []
      let remaining = 100

      currentNode.value.slices.forEach((slice: TreeNode, index: number) => {
        if (!slice.name.startsWith('Project')) {
          slice.name = `Project ${currentNode.value.name.split(' ')[1]}-${String.fromCharCode(65 + index)}`
        }
        labels.push(slice.name)
        const value = remaining * ((slice.percentage ?? 0) / 100)
        data.push(value)
        remaining -= value
        backgroundColor.push(slice.color || '#cccccc')
      })

      if (remaining > 0) {
        labels.push('Remaining')
        data.push(remaining)
        backgroundColor.push('#cccccc')
      }

      pieChart.data.labels = labels
      pieChart.data.datasets[0].data = data
      pieChart.data.datasets[0].backgroundColor = backgroundColor
      pieChart.update()
    }
  }

  function addSlice() {
    const newName = `Project ${currentNode.value.name.split(' ')[1]}-${String.fromCharCode(65 + currentNode.value.slices.length)}`
    const newSlice = reactive({
      name: newName,
      percentage: 100,
      color: '#' + Math.floor(Math.random() * 16777215).toString(16),
      slices: [],
      parent: currentNode.value
    })
    currentNode.value.slices.push(newSlice)
    updateView()
  }

  function moveUp(index: number) {
    if (index > 0) {
      const slices = currentNode.value.slices
      const temp = slices[index - 1]
      slices[index - 1] = slices[index]
      slices[index] = temp
      updateView()
    }
  }

  function moveDown(index: number) {
    const slices = currentNode.value.slices
    if (index < slices.length - 1) {
      const temp = slices[index + 1]
      slices[index + 1] = slices[index]
      slices[index] = temp
      updateView()
    }
  }

  function drillDown(slice: TreeNode) {
    currentNode.value = slice
    updateView()
  }

  function removeSlice(index: number) {
    currentNode.value.slices.splice(index, 1)
    updateView()
  }

  function goUpLevel() {
    if (currentNode.value.parent) {
      currentNode.value = currentNode.value.parent
      updateView()
    }
  }

  function navigateTo(node: any) {
    currentNode.value = node
    updateView()
  }

  onMounted(() => {
    if (pieChartCanvas.value) {
      const ctx = pieChartCanvas.value.getContext('2d')
      if (ctx) {
        pieChart = new Chart(ctx, {
          type: 'pie',
          data: {
            labels: [],
            datasets: [
              {
                data: [],
                backgroundColor: []
              }
            ]
          },
          options: {
            onClick: (event, elements) => {
              if (elements.length > 0) {
                const index = elements[0].index
                const slice = currentNode.value.slices[index]
                if (slice) {
                  currentNode.value = slice
                  updateView()
                }
              }
            }
          }
        })
        updateView()
      }
    }
    eventBus.on('data-imported', updateView)
    if (store.topNavbarContent) {
      store.topNavbarContent.value = ParticipatoryHeader // Set the specific header
    }
    store.openAboutModal = openAboutModal
    store.openHowToUseModal = openHowToUseModal
    store.bottomNavbarContent.value = Breadcrumb
    store.rightSidebarContent.value = ParticipatorySidebar
    currentNode.value = store.rootNode
    store.navigateTo = navigateTo
    store.goUpLevel = goUpLevel
    updateView()
    console.log('Handlers set:', {
      openAboutModal: store.openAboutModal,
      openHowToUseModal: store.openHowToUseModal
    })
  })

  onUnmounted(() => {
    store.rightSidebarContent.value = null
    store.bottomNavbarContent.value = null
    if (store.topNavbarContent) {
      store.topNavbarContent.value = null // Reset on unmount
    }
    // Clean up methods from the store
    store.openAboutModal = undefined
    store.openHowToUseModal = undefined
    eventBus.off('data-imported', updateView)
  })
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
    font-family: 'Font Awesome 5 Free';
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

  .modal-overlay {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 12000;
  }

  .modal-content {
    background: white;
    padding: 20px;
    max-width: 600px;
    margin: 20px auto;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #ddd;
    padding-bottom: 10px;
    margin-bottom: 20px;
  }

  .modal-header h2 {
    font-size: 24px;
    margin: 0;
  }

  .modal-body ol {
    list-style: decimal;
    padding-left: 20px;
  }

  .modal-body h3 {
    font-size: 18px;
    color: #333;
    margin-bottom: 10px;
  }

  .close-button {
    background: #ff5a5f;
    color: white;
    border: none;
    padding: 1px;
    border-radius: 5px;
    width: 30px;
    height: 30px;
    font-size: 30px;
    line-height: 30px;
    text-align: center;
    cursor: pointer;
  }

  .close-button:hover {
    /* background-color: darkred; */
    background: #ff3b3f;
  }

  .command-container {
    display: flex;
    align-items: center;
    margin-top: 10px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background: #f9f9f9;
  }

  .command-container pre {
    margin: 0;
    padding: 10px;
    background: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 5px;
    flex: 1;
  }

  .command-container button {
    cursor: pointer;
    padding: 5px 10px;
    font-size: 14px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
  }

  .command {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .command code {
    font-family: monospace;
    font-size: 14px;
    color: #333;
    white-space: nowrap;
  }

  .command button {
    background: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 5px 10px;
    cursor: pointer;
  }

  .command button:hover {
    background: #0056b3;
  }
</style>
