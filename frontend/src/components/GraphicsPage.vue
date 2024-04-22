<template>
  <div class="chart-container">
    <!-- Gráfico de IP de Origem -->
    <div class="chart">
      <h2 class="chart-title">Ocorrências de IP de Origem</h2>
      <canvas id="grafico-ip-origem"></canvas>
    </div>

    <!-- Gráfico de IP de Destino -->
    <div class="chart">
      <h2 class="chart-title">Ocorrências de IP de Destino</h2>
      <canvas id="grafico-ip-destino"></canvas>
    </div>
  </div>
</template>
<script>
import { Chart } from "chart.js";

export default {
  name: 'GraphicsPage',
  props: {
    pacotes: Array
  },
  mounted() {
    this.criarGraficoIP();
  },  
  watch: {
    pacotes: {
      handler(newPacotes) {
        if (newPacotes.length > 0) {
          this.atualizarGraficos();
        }
      },
      deep: true
    }
  },
  methods: {
    criarGraficoIP() {
      // Extrai os endereços IP de origem e destino dos pacotes
      const ipsOrigem = this.pacotes.map(pacote => pacote.ip_origem);
      const ipsDestino = this.pacotes.map(pacote => pacote.ip_destino);

      // Conta a ocorrência de cada endereço IP
      const contadorOrigem = this.contarOcorrencias(ipsOrigem);
      const contadorDestino = this.contarOcorrencias(ipsDestino);

      // Dados do gráfico de IP de origem
      const dataOrigem = {
        labels: Object.keys(contadorOrigem),
        datasets: [{
          label: 'IP de Origem',
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
          data: Object.values(contadorOrigem)
        }]
      };

      // Dados do gráfico de IP de destino
      const dataDestino = {
        labels: Object.keys(contadorDestino),
        datasets: [{
          label: 'IP de Destino',
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
          data: Object.values(contadorDestino)
        }]
      };

      // Opções dos gráficos
      const options = {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      };

      // Renderiza o gráfico de IP de origem
      const ctxOrigem = document.getElementById('grafico-ip-origem').getContext('2d');
      this.chartOrigem = new Chart(ctxOrigem, {
        type: 'bar',
        data: dataOrigem,
        options: options
      });

      // Renderiza o gráfico de IP de destino
      const ctxDestino = document.getElementById('grafico-ip-destino').getContext('2d');
      this.chartDestino = new Chart(ctxDestino, {
        type: 'bar',
        data: dataDestino,
        options: options
      });
    },
    contarOcorrencias(arr) {
      return arr.reduce((acc, curr) => {
        acc[curr] ? acc[curr]++ : (acc[curr] = 1);
        return acc;
      }, {});
    },
    atualizarGraficos() {
      // Atualiza os gráficos com os novos dados
      const ipsOrigem = this.pacotes.map(pacote => pacote.ip_origem);
      const ipsDestino = this.pacotes.map(pacote => pacote.ip_destino);

      const contadorOrigem = this.contarOcorrencias(ipsOrigem);
      const contadorDestino = this.contarOcorrencias(ipsDestino);

      // Atualiza os dados do gráfico de IP de origem
      this.chartOrigem.data.labels = Object.keys(contadorOrigem);
      this.chartOrigem.data.datasets[0].data = Object.values(contadorOrigem);
      this.chartOrigem.update();

      // Atualiza os dados do gráfico de IP de destino
      this.chartDestino.data.labels = Object.keys(contadorDestino);
      this.chartDestino.data.datasets[0].data = Object.values(contadorDestino);
      this.chartDestino.update();
    }
  }
};
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column; 
}

.chart {
  margin-bottom: 50px;
}

.chart-title {
  text-align: center;
  margin-top: 10px;
  font-size: 16px;
  color: #333;
  text-transform: uppercase;
}
</style>