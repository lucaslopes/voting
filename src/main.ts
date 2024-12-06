import "./assets/main.css";

import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { fas } from "@fortawesome/free-solid-svg-icons";
library.add(fas);

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.component("font-awesome-icon", FontAwesomeIcon);

app.use(router);

app.mount("#app");
