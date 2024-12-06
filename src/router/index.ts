import { createRouter, createWebHashHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Voting",
    component: () => import("../views/RatedEVoting.vue"),
  },
  {
    path: "/voting",
    name: "RatedEVoting",
    component: () => import("../views/RatedEVoting.vue"),
  },
  {
    path: "/budgeting",
    name: "ParticipatoryBudgeting",
    component: () => import("../views/ParticipatoryBudgeting.vue"),
  },
];

const router = createRouter({
  history: createWebHashHistory(), // Switch from createWebHistory to createWebHashHistory
  routes,
});

export default router;
