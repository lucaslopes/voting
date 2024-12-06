<!-- VotingApp.vue -->
<template>
  <!-- Elections Container -->
  <div id="elections-container">
    <!-- Rendered elections -->
    <div
      v-for="election in elections"
      :key="election.publicKeyMetadata"
      class="election-box"
    >
      <div class="election-header">{{ election.question }}</div>
      <input
        type="range"
        class="slider"
        :id="'vote-slider-' + election.publicKeyMetadata"
        min="0"
        max="100"
        step="1"
        v-model.number="election.currentScore"
      />
      <div class="slider-labels">
        <span style="float: left">{{ election.lowerValue }}</span>
        <span style="float: right">{{ election.upperValue }}</span>
      </div>
      <button
        class="vote-button"
        @click="encryptAndDownload(election.publicKeyMetadata)"
      >
        Vote: <span>{{ election.currentScore }}</span
        >%
      </button>
      <div class="election-info">
        <span>Public Key: {{ election.publicKeyMetadata }}</span>
        <span>Creation Date: {{ formatDate(election.creationDate) }}</span>
        <span>Last Updated: {{ formatDate(election.lastUpdateTime) }}</span>
        <span>Votes Counted: {{ election.votesCounted }}</span>
      </div>
    </div>
  </div>

  <!-- New Election Modal -->
  <div
    id="new-election-modal"
    v-if="showNewElectionModal"
    class="modal-overlay"
  >
    <div class="modal-content">
      <button type="button" class="close-button" @click="closeNewElectionModal">
        &times;
      </button>
      <form id="new-election-form" @submit.prevent="createElection">
        <h2>Create Election</h2>
        <label for="question">Election Question or Sentence:</label>
        <textarea
          id="question"
          v-model="question"
          placeholder="How easy is it to vote using this app?"
          required
        ></textarea>
        <span class="error">{{ errors.question }}</span>

        <div class="form-row">
          <div class="form-field">
            <label for="lower-value">Lower Value Description:</label>
            <input
              type="text"
              id="lower-value"
              v-model="lowerValue"
              placeholder="Very Hard"
              required
            />
            <span class="error">{{ errors.lowerValue }}</span>
          </div>
          <div class="form-field">
            <label for="upper-value">Upper Value Description:</label>
            <input
              type="text"
              id="upper-value"
              v-model="upperValue"
              placeholder="Very Easy"
              required
            />
            <span class="error">{{ errors.upperValue }}</span>
          </div>
        </div>

        <button type="submit" class="submit-button">Create Election</button>
      </form>
    </div>
  </div>

  <!-- How to Use Modal -->
  <div id="how-to-use-modal" v-if="showHowToUseModal" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h2>How to Use</h2>
        <button type="button" class="close-button" @click="closeHowToUseModal">
          &times;
        </button>
      </div>
      <div class="modal-body">
        <ol>
          <li>
            <h3>Install SyftBox</h3>
            <p>
              Paste the following command into your terminal (MacOS/Linux only):
            </p>
            <div class="command-container">
              <div class="command">
                <code
                  >curl -LsSf https://syftbox.openmined.org/install.sh |
                  sh</code
                >
                <button @click="copyToClipboard(installCommand)">Copy</button>
              </div>
            </div>
          </li>
          <li>
            <h3>Set Up Voting API</h3>
            <p>
              Open the SyftBox folder on your Desktop. Move the voting API into
              the
              <code>apis/</code> folder:
            </p>
            <ul>
              <li>
                <strong>If you have git, run:</strong>
                <div class="command-container">
                  <div class="command">
                    <code
                      >git clone https://github.com/lucaslopes/voting.git</code
                    >
                    <button @click="copyToClipboard(gitCommand)">Copy</button>
                  </div>
                </div>
              </li>
              <li>
                Alternatively, download the ZIP file:
                <a
                  href="https://github.com/lucaslopes/voting/archive/refs/heads/main.zip"
                  class="download-button"
                  >Download Repository</a
                >
              </li>
            </ul>
          </li>
          <li>
            <h3>Cast Votes or Submit Elections</h3>
            <ul>
              <li>
                Move your ballot JSON file to:
                <code
                  >SyftBox/datasites/&lt;your@email.org&gt;/api_data/voting/ballots</code
                >
              </li>
              <li>
                Move new election JSON file to:
                <code
                  >SyftBox/datasites/&lt;your@email.org&gt;/api_data/voting/elections</code
                >
              </li>
            </ul>
          </li>
        </ol>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {
  defineComponent,
  ref,
  reactive,
  onMounted,
  onUnmounted,
  markRaw,
  h,
} from "vue";
import * as paillierBigint from "paillier-bigint";
import { store } from "../store"; // Import the store
import RatedEVotingSidebar from "../components/RatedEVotingSidebar.vue";
import StatsBottomBarComponent from "../components/ElectionStatsBottomBar.vue";

interface Election {
  question: string;
  lowerValue: string;
  upperValue: string;
  publicKey: {
    n: string;
    g: string;
  };
  privateKey?: {
    p: string;
    q: string;
    lambda: string;
    mu: string;
  };
  publicKeyMetadata: string;
  votesCounted: number;
  creationDate: string;
  lastUpdateTime: string;
  outcome: any;
  defaultValue?: number;
  currentScore?: number;
}

interface ElectionMap {
  [key: string]: Election;
}

export default defineComponent({
  name: "VotingApp",
  setup() {
    const showNewElectionModal = ref(false);
    const showHowToUseModal = ref(false);
    const elections = ref<Election[]>([]);
    const question = ref("");
    const lowerValue = ref("");
    const upperValue = ref("");
    const errors = reactive({
      question: "",
      lowerValue: "",
      upperValue: "",
    });

    const installCommand = ref(
      "curl -LsSf https://syftbox.openmined.org/install.sh | sh",
    );
    const gitCommand = ref(
      "git clone https://github.com/lucaslopes/voting.git",
    );

    const copyToClipboard = (text: string) => {
      navigator.clipboard
        .writeText(text)
        .then(() => {
          alert("Copied to clipboard!");
        })
        .catch((err) => {
          alert("Failed to copy: " + err);
        });
    };

    const openNewElectionModal = () => {
      showNewElectionModal.value = true;
    };

    const closeNewElectionModal = () => {
      showNewElectionModal.value = false;
    };

    const openHowToUseModal = () => {
      showHowToUseModal.value = true;
    };

    const closeHowToUseModal = () => {
      showHowToUseModal.value = false;
    };

    const createElection = async () => {
      let valid = true;
      if (!question.value.trim()) {
        errors.question = "Election question is required.";
        valid = false;
      } else {
        errors.question = "";
      }

      if (!lowerValue.value.trim()) {
        errors.lowerValue = "Lower slider value description is required.";
        valid = false;
      } else {
        errors.lowerValue = "";
      }

      if (!upperValue.value.trim()) {
        errors.upperValue = "Upper slider value description is required.";
        valid = false;
      } else {
        errors.upperValue = "";
      }

      if (!valid) return;

      const { publicKey, privateKey } =
        await paillierBigint.generateRandomKeys(512);

      const creationDate = new Date().toISOString();
      const publicKeyMetadata = `${publicKey.n
        .toString()
        .slice(0, 4)}_${publicKey.n.toString().slice(-4)}`;

      const election: Election = {
        question: question.value.trim(),
        lowerValue: lowerValue.value.trim(),
        upperValue: upperValue.value.trim(),
        publicKey: {
          n: publicKey.n.toString(),
          g: publicKey.g.toString(),
        },
        privateKey: {
          p: (privateKey as any)._p.toString(),
          q: (privateKey as any)._q.toString(),
          lambda: privateKey.lambda.toString(),
          mu: privateKey.mu.toString(),
        },
        publicKeyMetadata,
        votesCounted: 0,
        creationDate,
        lastUpdateTime: creationDate,
        outcome: null,
      };

      // Download election file
      const blob = new Blob([JSON.stringify(election, null, 2)], {
        type: "application/json",
      });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `election-${publicKeyMetadata}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      // Reset form
      question.value = "";
      lowerValue.value = "";
      upperValue.value = "";
      closeNewElectionModal();
      alert("Election created successfully!");
    };

    const renderElections = async () => {
      try {
        const response = await fetch("./election_outcomes.json");
        const electionsData = (await response.json()) as ElectionMap;

        elections.value = [];
        for (const electionId in electionsData) {
          const election = electionsData[electionId];
          if (
            !(
              "question" in election &&
              "lowerValue" in election &&
              "upperValue" in election &&
              "publicKey" in election &&
              "publicKeyMetadata" in election &&
              "votesCounted" in election &&
              "creationDate" in election &&
              "lastUpdateTime" in election &&
              "outcome" in election
            )
          ) {
            console.warn("Invalid election data:", election);
            continue;
          }
          election.defaultValue =
            election.outcome === null ? 50 : election.outcome.average;
          election.currentScore = election.defaultValue;
          elections.value.push(election);
        }
      } catch (error) {
        console.error("Error loading elections:", error);
      }
    };

    const updateScore = (publicKeyMetadata: string, value: number) => {
      const election = elections.value.find(
        (e) => e.publicKeyMetadata === publicKeyMetadata,
      );
      if (election) {
        election.currentScore = value;
      }
    };

    const encryptAndDownload = async (publicKeyMetadata: string) => {
      try {
        const election = elections.value.find(
          (e) => e.publicKeyMetadata === publicKeyMetadata,
        );
        if (!election) {
          throw new Error("Election not found.");
        }
        const publicKey = new paillierBigint.PublicKey(
          BigInt(election.publicKey.n),
          BigInt(election.publicKey.g),
        );
        const vote = parseFloat(election.currentScore!.toString());
        const encryptedVote = publicKey.encrypt(BigInt(Math.round(vote)));

        const encryptedData = {
          ciphertext: encryptedVote.toString(),
          publicKey: {
            n: publicKey.n.toString(),
            g: publicKey.g.toString(),
          },
          publicKeyMetadata,
          voteDate: new Date().toISOString(),
        };

        const blob = new Blob([JSON.stringify(encryptedData)], {
          type: "application/json",
        });
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = `ballot-${publicKeyMetadata}.json`;
        a.click();
      } catch (error) {
        console.error("Error encrypting vote:", error);
      }
    };

    const formatDate = (dateString: string) => {
      return new Date(dateString).toLocaleString();
    };

    const RatedEVotingHeader = markRaw(
      defineComponent({
        name: "RatedEVotingHeader",
        render() {
          return h("h1", [
            h(
              "a",
              {
                href: "https://en.wikipedia.org/wiki/Rated_voting",
                target: "_blank",
              },
              "Rated",
            ),
            " ", // Add a space text node
            h(
              "a",
              {
                href: "https://en.wikipedia.org/wiki/Electronic_voting",
                target: "_blank",
              },
              "e-Voting",
            ),
          ]);
        },
      }),
    );

    store.topNavbarContent.value = RatedEVotingHeader;

    onMounted(() => {
      renderElections();

      const totalElections = elections.value.length;
      const totalVotes = elections.value.reduce(
        (sum, e) => sum + e.votesCounted,
        0,
      );
      store.totalElections = totalElections;
      store.totalVotes = totalVotes;

      if (store.topNavbarContent) {
        store.topNavbarContent.value = RatedEVotingHeader;
      }

      store.bottomNavbarContent.value = StatsBottomBarComponent;
      store.rightSidebarContent.value = RatedEVotingSidebar;

      store.openHowToUseModal = openHowToUseModal;
      store.openNewElectionModal = openNewElectionModal;
    });

    onUnmounted(() => {
      if (store.topNavbarContent) {
        store.topNavbarContent.value = null; // Reset on unmount
      }
      store.bottomNavbarContent.value = null;
      store.rightSidebarContent.value = null;

      // Clean up methods from the store
      store.openHowToUseModal = undefined;
      store.openNewElectionModal = undefined;
    });

    return {
      showNewElectionModal,
      showHowToUseModal,
      openNewElectionModal,
      closeNewElectionModal,
      openHowToUseModal,
      closeHowToUseModal,
      createElection,
      elections,
      updateScore,
      encryptAndDownload,
      formatDate,
      question,
      lowerValue,
      upperValue,
      errors,
      installCommand,
      gitCommand,
      copyToClipboard,
    };
  },
});
</script>

<style scoped>
/* General Styles */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

.navbar {
  position: fixed;
  top: 60px;
  width: 100%;
  background-color: #333;
  color: white;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 1000;
}

.navbar h1 {
  margin: 0;
  font-size: 20px;
  text-align: center;
}

.navbar h1 a {
  color: #4caf50;
  text-decoration: none;
  margin: 0 5px;
}

.navbar h1 a:nth-child(2) {
  color: #ffa500;
}

#new-election-button,
#how-to-use-button {
  width: 11%;
  padding: 10px 15px;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 14px;
}

#new-election-button {
  background-color: #4caf50;
  margin-right: 2%;
}

#new-election-button:hover {
  background-color: #45a049;
}

#how-to-use-button {
  background-color: #ffa500;
}

#how-to-use-button:hover {
  background-color: #ff9900;
}

.election-box {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 20px;
  margin: 50px auto;
  width: 45%;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: box-shadow 0.3s;
  display: flex;
  flex-direction: column;
}

.election-box:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.election-header {
  font-weight: bold;
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.election-header {
  font-weight: bold;
  font-size: 24px;
  margin-bottom: 20px;
}

.slider-container {
  margin-bottom: 20px;
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

/* .modal-content {
  background: white;
  padding: 30px;
  max-width: 600px;
  width: 90%;
  border-radius: 10px;
  position: relative;
  overflow-y: auto;
} */

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

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input,
textarea,
button {
  width: 100%;
  margin-bottom: 15px;
  padding: 10px;
  font-size: 14px;
}

.slider {
  width: 100%;
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.vote-button {
  display: flex;
  margin-left: 43%;
  align-items: center;
  justify-content: center;
  width: 15%;
}

/* .close-button {
  background-color: red;
  color: white;
  border: none;
  padding: 10px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 5px;
  position: absolute;
  width: 40px;
  top: 10px;
  right: 10px;
} */

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

.error {
  color: red;
  font-size: 12px;
}

.election-info {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  margin-top: 15px;
  color: #555;
}

.form-row {
  display: flex;
  gap: 20px;
}

.form-field {
  flex: 1;
}

.submit-button {
  display: block;
  margin: 0 auto;
  padding: 15px 30px;
  font-size: 16px;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #45a049;
}

/* .command-container {
  display: flex;
  align-items: center;
  gap: 10px;
} */

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

/* .download-button {
  cursor: pointer;
  padding: 10px 20px;
  font-size: 14px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  text-decoration: none;
} */

.download-button {
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  text-decoration: none;
  display: inline-block;
  margin-top: 10px;
}

.download-button:hover {
  /* background-color: #0056b3; */
  background: #0056b3;
}
</style>
