<template>
  <div class="http-sequence">
    <div class="chart-container">
      <canvas ref="httpSequenceChart"></canvas>
    </div>
    <div class="chart-container">
      <canvas ref="httpSizeHistogram"></canvas>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto';

export default {
  props: {
    packets: {
      type: Object,
      default: () => ({ data: [] }) 
    }
  },
  watch: {
    packets: {
      handler(newPackets) {
        if (newPackets && newPackets.data && newPackets.data.length > 0) {
          this.generateHttpSequenceData(newPackets.data);
          this.generateHttpSizeHistogram(newPackets.data);
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    generateHttpSequenceData(pacotes) {
      const events = [];

      pacotes.forEach(packet => {
        const event = {
          timestamp: packet.timestamp,
          ipOrigem: packet.ip_origem,
          ipDestino: packet.ip_destino,
          metodo: packet.metodo,
          uri: packet.uri,
          versao: packet.versao,
          status: packet.status
        };
        events.push(event);
      });

      events.sort((a, b) => a.timestamp - b.timestamp);

      const labels = events.map(event => this.formatTimestamp(event.timestamp));
      const dataPoints = events.map(event => ({
        x: this.formatTimestamp(event.timestamp),
        y: event.metodo ? 'Requisição: ' + event.metodo + ' ' + event.uri : 'Resposta: ' + event.status
      }));

      this.renderHttpSequenceChart(labels, dataPoints);
    },

    formatTimestamp(timestamp) {
      const date = new Date(timestamp * 1000);
      return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
    },

    generateHttpChartsData(pacotes) {
      const methodCounts = {};
      const statusCounts = {};

      pacotes.forEach(packet => {
        const method = packet.metodo;
        if (method) {
          if (!methodCounts[method]) {
            methodCounts[method] = 0;
          }
          methodCounts[method]++;
        }

        const status = packet.status;
        if (status) {
          if (!statusCounts[status]) {
            statusCounts[status] = 0;
          }
          statusCounts[status]++;
        }
      });

      const methodLabels = Object.keys(methodCounts);
      const methodData = Object.values(methodCounts);

      const statusLabels = Object.keys(statusCounts);
      const statusData = Object.values(statusCounts);

      this.renderHttpBarCharts(methodLabels, methodData, statusLabels, statusData);
    },

    generateHttpSizeHistogram(pacotes) {
      const sizes = pacotes.map(packet => packet.size);

      this.renderHttpSizeHistogram(sizes);
    },

    renderHttpBarCharts(methodLabels, methodData, statusLabels, statusData) {
      const methodCtx = this.$refs.httpMethodChart.getContext('2d');
      new Chart(methodCtx, {
        type: 'bar',
        data: {
          labels: methodLabels,
          datasets: [{
            label: 'Número de Requisições por Método HTTP',
            data: methodData,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });

      const statusCtx = this.$refs.httpStatusChart.getContext('2d');
      new Chart(statusCtx, {
        type: 'bar',
        data: {
          labels: statusLabels,
          datasets: [{
            label: 'Número de Requisições por Código de Status HTTP',
            data: statusData,
            backgroundColor: 'rgba(255, 159, 64, 0.2)',
            borderColor: 'rgba(255, 159, 64, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    },

    renderHttpSequenceChart(labels, dataPoints) {
      const ctx = this.$refs.httpSequenceChart.getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Sequência de Interações HTTP',
            data: dataPoints.map(point => ({ x: labels.indexOf(point.x), y: point.y })),
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            fill: false,
            tension: 0.1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              type: 'category',
              title: {
                display: true,
                text: 'Tempo'
              }
            },
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Evento'
              },
              ticks: {
                callback: function(value, index) {
                  return dataPoints[index] ? dataPoints[index].y : value;
                }
              }
            }
          },
          plugins: {
            tooltip: {
              callbacks: {
                label: function(tooltipItem) {
                  return tooltipItem.raw.y;
                }
              }
            }
          }
        }
      });
    },

    renderHttpSizeHistogram(sizes) {
      const ctx = this.$refs.httpSizeHistogram.getContext('2d');
      const binSize = 100; 
      const maxBin = Math.max(...sizes);
      const bins = Math.ceil(maxBin / binSize);
      const histogramData = new Array(bins).fill(0);

      sizes.forEach(size => {
        const binIndex = Math.floor(size / binSize);
        histogramData[binIndex]++;
      });

      const labels = histogramData.map((_, index) => `${index * binSize} - ${(index + 1) * binSize}`);

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Distribuição do Tamanho das Requisições HTTP',
            data: histogramData,
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }
  }
};
</script>

<style scoped>
.http-sequence {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column; /* Organiza os gráficos em coluna */
  justify-content: center;
  align-items: center;
}

.chart-container {
  width: 100%;
  height: 400px; /* Ajuste a altura desejada para cada gráfico */
  margin: 10px 0; /* Espaçamento entre os gráficos */
  max-height: 50vh; /* Limita a altura máxima dos gráficos */
}

canvas {
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 100%;
  margin: auto; /* Para centralizar o canvas */
}
</style>
