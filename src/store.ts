import {
  defineComponent,
  markRaw,
  reactive,
  ref,
  type Component,
  shallowRef,
} from "vue";
import { eventBus } from "./eventBus";

export interface TreeNode {
  name: string;
  slices: TreeNode[];
  parent: TreeNode | null;
  color?: string;
  percentage?: number;
}

const rootNode = reactive<TreeNode>({
  name: "Total Budget",
  slices: [],
  parent: null,
});

const currentNode = ref(rootNode);

const VotingComponent = markRaw(
  defineComponent({
    template: `<div>Voting</div>`,
  }),
);

function removeCircularReferences(node: TreeNode) {
  return JSON.parse(
    JSON.stringify(node, (key, value) =>
      key === "parent" ? undefined : value,
    ),
  );
}

export const store = {
  topNavbarContent: shallowRef<Component | null>(VotingComponent),
  bottomNavbarContent: shallowRef<any>(null),
  rightSidebarContent: shallowRef<any>(null),
  openAboutModal: undefined as (() => void) | undefined,
  openHowToUseModal: undefined as (() => void) | undefined,
  openNewElectionModal: undefined as (() => void) | undefined,
  navigateTo: null as ((node: TreeNode) => void) | null,
  goUpLevel: null as (() => void) | null,
  rootNode,
  currentNode,
  totalElections: ref(0),
  totalVotes: ref(0),
  exportJSON() {
    if (!this.rootNode) {
      console.error("No root node found for export");
      return;
    }
    const cleanRoot = removeCircularReferences(this.rootNode);
    const dataStr = JSON.stringify(cleanRoot, null, 2);
    const blob = new Blob([dataStr], { type: "application/json" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "participatory_budget.json";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  },
  importJSON(event: Event) {
    const target = event.target as HTMLInputElement;
    const file = target?.files && target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const result = e.target?.result as string;
          const importedNode = JSON.parse(result);
          this.recreateParentReferences(importedNode, null);
          Object.assign(this.rootNode, importedNode);
          this.currentNode.value = this.rootNode;
          eventBus.emit("data-imported");
        } catch (error) {
          console.error(error);
          alert("Invalid JSON file");
        }
      };
      reader.readAsText(file);
    }
  },
  recreateParentReferences(node: any, parent: any) {
    node.parent = parent;
    if (node.slices && node.slices.length > 0) {
      node.slices.forEach((slice: any) => {
        this.recreateParentReferences(slice, node);
      });
    }
  },
};
