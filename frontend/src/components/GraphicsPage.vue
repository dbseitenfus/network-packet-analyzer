<template>
  <div>
    <input type="file" @change="uploadArquivo">
    <h1>Listagem de Pacotes</h1>
    <ul>
      <li v-for="pacote in pacotes" :key="pacote.timestamp">
        <p>Timestamp: {{ pacote.timestamp }}</p>
        <p>MAC de Origem: {{ pacote.mac_origem }}</p>
        <p>MAC de Destino: {{ pacote.mac_destino }}</p>
        <p>IP de Origem: {{ pacote.ip_origem }}</p>
        <p>IP de Destino: {{ pacote.ip_destino }}</p>
        <p>Protocolo: {{ pacote.protocolo }}</p>
        <p>Tipo de Ethernet: {{ pacote.tipo_ethernet }}</p>
      </li>
    </ul>
    <div class="float-button">
      <button @click="scrollTop" class="btn-floating">↑</button>
    </div>

    <!-- Gráfico de IP de Origem -->
    <canvas id="grafico-ip-origem"></canvas>

    <!-- Gráfico de IP de Destino -->
    <canvas id="grafico-ip-destino"></canvas>
  </div>
</template>

<script>
import axios from "axios";
import { Chart } from "chart.js";

export default {
  name: 'GraphicsPage',
  data() {
    return {
      pacotes: []
    };
  },
  methods: {
    async uploadArquivo(event) {
      const arquivo = event.target.files[0];
      const formData = new FormData();
      formData.append("arquivo_pcap", arquivo);

      try {
        const response = await axios.post("http://localhost:8000/listar_pacotes", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        });

        // Atualiza os pacotes com os dados recebidos
        this.pacotes = response.data.pacotes;

        // Chama a função para criar os gráficos de IP
        this.criarGraficoIP();
      } catch (error) {
        console.error("Erro ao enviar arquivo:", error);
      }
    },
    scrollTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    criarGraficoIP() {
      // Extrai os endereços IP de origem e destino dos pacotes
      const ipsOrigem = this.pacotes.map(pacote => pacote.ip_origem);
      const ipsDestino = this.pacotes.map(pacote => pacote.ip_destino);

      console.log(ipsOrigem, ipsDestino);

      // Conta a ocorrência de cada endereço IP
      const contadorOrigem = this.contarOcorrencias(ipsOrigem);
      const contadorDestino = this.contarOcorrencias(ipsDestino);

      // Objetos para armazenar os dados do gráfico
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

      // Opções do gráfico
      const options = {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      };

      // Renderiza o gráfico de IP de origem
      const ctxOrigem = document.getElementById('grafico-ip-origem').getContext('2d');
      new Chart(ctxOrigem, {
        type: 'bar',
        data: dataOrigem,
        options: options
      });

      // Renderiza o gráfico de IP de destino
      const ctxDestino = document.getElementById('grafico-ip-destino').getContext('2d');
      new Chart(ctxDestino, {
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
    }
  }
};
</script>

<style scoped>
.float-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
}

.btn-floating {
  background-color: #232343;
  color: white;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0px 0px 5px rgba(112, 106, 106, 0.5);
}
</style>

