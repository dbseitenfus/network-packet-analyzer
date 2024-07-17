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

      const ctx = this.$refs.httpSequenceChart.getContext('2d');
      if (ctx) {
        this.renderHttpSequenceChart(labels, dataPoints, ctx);
      }
    },

    formatTimestamp(timestamp) {
      const date = new Date(timestamp * 1000);
      return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
    },

    generateHttpSizeHistogram(pacotes) {
      const sizes = pacotes.map(packet => packet.size);

      const ctx = this.$refs.httpSizeHistogram.getContext('2d');
      if (ctx) {
        this.renderHttpSizeHistogram(sizes, ctx);
      }
    },

    renderHttpSequenceChart(labels, dataPoints, ctx) {
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

    renderHttpSizeHistogram(sizes, ctx) {
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
  flex-direction: column; 
  justify-content: center;
  align-items: center;
}

.chart-container {
  width: 100%;
  height: 400px; 
  margin: 10px 0;
  max-height: 50vh; 
}

canvas {
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 100%;
  margin: auto; 
}
</style>
