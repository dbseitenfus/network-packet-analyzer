<template>
  <div>
    <label for="fileInput" class="float-button btn-floating">
      <div class="icon-container">
        <n-icon size="24">
          <cloud-upload/>
        </n-icon>
      </div>
    </label>
    <input id="fileInput" ref="fileInput" type="file" style="display: none" @change="uploadArquivo">
    <graphics-page :pacotes="pacotes"/>
    <div class="graph-container">
      <network-graph  :pacotes="pacotes" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import GraphicsPage from './GraphicsPage.vue';
import { NIcon } from "naive-ui";
import { CloudUpload } from "@vicons/ionicons5";
import NetworkGraph from "./NetworkGraph.vue";

export default {
  name: 'DashboardPackages',
  components: {
    GraphicsPage,
    NIcon,
    CloudUpload,
    NetworkGraph
  },
  data() {
    return {
      pacotes: [],
      enderecosIP: [],
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
      } catch (error) {
        console.error("Erro ao enviar arquivo:", error);
      }
    },
    async listarEnderecosIP() {
      try {
        const response = await axios.get("http://localhost:8000/listar_enderecos_ip");
        this.enderecosIP = response.data.enderecos_ip;
      } catch (error) {
        console.error("Erro ao listar endereços IP:", error);
      }
    }
  },
  mounted() {
    this.listarEnderecosIP();
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

.icon-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}

.graph-container {
  width: 100vw; /* Largura igual à largura da tela */
  height: 100vh; /* Altura igual à altura da tela */
  background-color:#D4F3FA;
}
</style>
