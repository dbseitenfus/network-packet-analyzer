import { createApp } from 'vue'
import App from './App.vue'
import Chart from 'chart.js/auto';
import router from '../src/router.js'; 

// Importe os controladores e escalas necessários
import { BarController, CategoryScale, LinearScale, Title, Tooltip } from 'chart.js';

// Registre os controladores e escalas necessários
Chart.register(BarController, CategoryScale, LinearScale, Title, Tooltip);

createApp(App)
    .use(router)
    .provide('Chart', Chart)
    .mount('#app')