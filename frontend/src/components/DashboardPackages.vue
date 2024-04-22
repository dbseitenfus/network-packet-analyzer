<template>
  <div class="page">
    <label for="fileInput" class="float-button btn-floating">
      <div class="icon-container">
        <n-icon size="24">
          <cloud-upload/>
        </n-icon>
      </div>
    </label>
    <input id="fileInput" ref="fileInput" type="file" style="display: none" @change="uploadArquivo">
    <div class="graph-container">
      <network-graph class="graph" :pacotes="pacotes" />
      <graphics-page class="graphics" :pacotes="pacotes"/>
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
      formData.append("pcap_file", arquivo);

      try {
        const fileExtension = this.getFileExtension(arquivo.name);
        var response;
        if(fileExtension == "pcapng") {
          response = await this.getIpv4Packets(formData);
        } else if(fileExtension == "pcap") {
          response = await this.getArpPackets(formData);
        }
         

        // Atualiza os pacotes com os dados recebidos
        this.pacotes = response.data.pacotes;
      } catch (error) {
        console.error("Erro ao enviar arquivo:", error);
      }
    },

    async getIpv4Packets(formData) {
      return await axios.post("http://localhost:8000/list_packages", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        });
    },

    async getArpPackets(formData) {
      return await axios.post("http://localhost:8000/arp/list_packages", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        });
    },

    getFileExtension(fileName) {
      const array = fileName.split('.');
      return array.slice(-1);
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

.page {
  width: 100vw;
  height: 100vh;
  background-color: #eee;
}

.graph-container {
  position: relative;
  width: 100%; 
  height: 100%;
  display: flex;
  flex-direction: column;
}

.graphics {
  position: absolute;
  background-color: #fff;
  top: 20px; /* Margem superior */
  right: 20px; /* Margem direita */
  width: 300px; /* Largura do .graphics */
  height: calc(100vh - 40px); /* Tamanho da tela menos as margens superior e inferior */
}

.graph {
  width: calc(100% - 320px); /* Largura do .graph é o restante do espaço disponível */
  height: 100%;
  background-color: aquamarine;
}
</style>
