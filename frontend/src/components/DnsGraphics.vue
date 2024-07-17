<template>
  <div class="dns-graphics">
    <canvas ref="dnsQueriesPieChart"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  name: 'DnsGraphics',
  props: {
    packets: Object
  },
  watch: {
    packets: {
      handler(newPackets) {
        if (newPackets && newPackets.data && newPackets.data.length > 0) {
          this.renderPieChart(newPackets.data);
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    renderPieChart(packets) {
      const canvas = this.$refs.dnsQueriesPieChart;
      if (!canvas) return;

      const ctx = canvas.getContext('2d');

      // Contagem de tipos únicos de consultas DNS
      const queryCounts = {};
      packets.forEach(packet => {
        packet.queries.forEach(query => {
          const key = `${query.name}_${query.type}_${query.cls}`;
          if (!queryCounts[key]) {
            queryCounts[key] = {
              label: `${query.name} (${query.type})`,
              count: 0,
              color: this.generateRandomColor()
            };
          }
          queryCounts[key].count++;
        });
      });

      const labels = [];
      const data = [];
      const backgroundColors = [];

      // Montando os dados para o gráfico de pizza
      Object.keys(queryCounts).forEach(key => {
        labels.push(queryCounts[key].label);
        data.push(queryCounts[key].count);
        backgroundColors.push(queryCounts[key].color);
      });

      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            label: 'Distribuição de Consultas DNS',
            data: data,
            backgroundColor: backgroundColors,
            borderColor: backgroundColors.map(color => color.replace('0.6', '1')), // Ajustando a transparência para a borda
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
            },
            tooltip: {
              callbacks: {
                label: function(tooltipItem) {
                  return `${tooltipItem.label}: ${tooltipItem.raw}`;
                }
              }
            }
          }
        }
      });
    },
    generateRandomColor() {
      // Função para gerar uma cor aleatória em formato RGBA
      const r = Math.floor(Math.random() * 256);
      const g = Math.floor(Math.random() * 256);
      const b = Math.floor(Math.random() * 256);
      return `rgba(${r}, ${g}, ${b}, 0.6)`;
    }
  }
};
</script>

<style scoped>
.dns-graphics {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

canvas {
  max-width: 100%;
  max-height: 100%;
  margin: auto; /* Para centralizar o canvas */
}
</style>
