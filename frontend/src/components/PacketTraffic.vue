<template>
  <div class="packet-traffic">
    <h2 class="chart-title">Visualização de Tráfego de Pacotes</h2>
    <canvas ref="packetChart" width="400" height="300"></canvas>
  </div>
</template>

<script>
import { Chart } from 'chart.js';

export default {
  name: 'PacketTraffic',
  props: {
    packetData: {
      type: Array,
      required: true
    }
  },
  mounted() {
    this.renderPacketChart();
  },
  methods: {
    renderPacketChart() {
      const ctx = this.$refs.packetChart.getContext('2d');

      // Preparar dados para o gráfico
      const labels = this.packetData.map(packet => packet.timestamp);
      const data = this.packetData.map(packet => packet.packetSize); // Suponhamos que 'packetSize' seja um atributo disponível nos dados

      // Configurações do gráfico
      const config = {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Tamanho do Pacote',
            data: data,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }]
        },
        options: {
          scales: {
            x: {
              type: 'time',
              time: {
                unit: 'second'
              }
            },
            y: {
              beginAtZero: true
            }
          }
        }
      };

      // Renderizar o gráfico usando Chart.js
      this.packetChart = new Chart(ctx, config);
    }
  },
  watch: {
    packetData: {
      handler() {
        // Atualizar o gráfico quando os dados mudarem
        this.packetChart.destroy(); // Destruir o gráfico antigo
        this.renderPacketChart(); // Renderizar novamente com os novos dados
      },
      deep: true
    }
  },
  beforeDestroy() {
    if (this.packetChart) {
      this.packetChart.destroy();
    }
  }
};
</script>

<style scoped>
.packet-traffic {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.chart-title {
  text-align: center;
  margin-bottom: 10px;
  font-size: 18px;
  color: #333;
}
</style>
