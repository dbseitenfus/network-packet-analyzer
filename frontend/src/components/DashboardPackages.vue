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
      <network-graph class="graph" :packets="packets" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import NetworkGraph from "./NetworkGraph.vue";
import { NIcon } from "naive-ui";
import { CloudUpload } from "@vicons/ionicons5";

export default {
  name: 'DashboardPackages',
  components: {
    NetworkGraph,
    NIcon,
    CloudUpload,
  },
  data() {
    return {
      packets: {
        type: -1,
        data: []
      }
    };
  },
  methods: {
    async uploadArquivo(event) {
      const arquivo = event.target.files[0];
      
      if (!arquivo) {
        console.error("Nenhum arquivo selecionado.");
        return;
      }

      const formData = new FormData();
      formData.append("pcap_file", arquivo);

      try {
        const fileExtension = this.getFileExtension(arquivo.name);

        if (fileExtension === "pcapng") {
          this.packets.type = 0; // IPv4
          const response = await this.getIpv4Packets(formData);
          console.log(response);
          this.packets.data = response.data.pacotes;
        } else if (fileExtension === "pcap") {
          const protocolName = this.getProtocolName(arquivo.name);
          if (protocolName === "ipv4") {
            this.packets.type = 0; // IPv4
            const response = await this.getIpv4Packets(formData);
            console.log(response);
            this.packets.data = response.data.pacotes;
          } else if (protocolName === "arp") {
            this.packets.type = 1; // ARP
            const response = await this.getArpPackets(formData);
            console.log(response);
            this.packets.data = response.data.pacotes;
          } else if (protocolName === "rip") {
            this.packets.type = 2; // RIP (exemplo)
            const response = await this.getRipPackets(formData);
            console.log(response);
            this.packets.data = response.data.pacotes;
          } else if (protocolName === "udp") {
            this.packets.type = 3; // UDP (exemplo)
            const response = await this.getUdpPackets(formData);
            console.log(response);
            this.packets.data = response.data.pacotes;
          } else {
            throw new Error("Protocolo não suportado: " + protocolName);
          }
        } else {
          throw new Error("Formato de arquivo não suportado.");
        }
      } catch (error) {
        console.error("Erro ao enviar arquivo:", error);
      }
    },

    getFileExtension(fileName) {
      return fileName.split(".").pop().toLowerCase();
    },

    getProtocolName(fileName) {
      const baseName = fileName.split(".")[0].toLowerCase();
      if (baseName.includes("ipv4")) {
        return "ipv4";
      } else if (baseName.includes("arp")) {
        return "arp";
      } else if (baseName.includes("rip")) {
        return "rip";
      } else if (baseName.includes("udp")) {
        return "udp";
      } else {
        throw new Error("Protocolo não identificado pelo nome do arquivo.");
      }
    },


    async getIpv4Packets(formData) {
      return await axios.post("http://localhost:8000/ipv4/list_packages", formData, {
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

    // getFileExtension(fileName) {
    //   const array = fileName.split('.');
    //   return array.slice(-1)[0];
    // },
  }
};
</script>

<style scoped>
.page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

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
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.graph {
  width: 100%;
  height: 100%;
  background-color: aqua;
}
</style>
