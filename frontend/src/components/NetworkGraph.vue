<template>
  <div class="graph">
    <v-network-graph
      :nodes="nodes"
      :edges="edges"
      :configs="configs"
      :event-handlers="eventHandlers"
    >
      <template #override-node="{ nodeId, scale, config, ...slotProps }">
        <circle
          v-bind="slotProps"
          :ref="nodeId"
          :r="config.radius * scale"
          fill="white"
          stroke="lightgrey"
          :stroke-width="size.default"
        />
      </template>
    </v-network-graph>
    
    <div v-if="packets.type === 0 && selectedNode" class="node-info">
      <p><strong>ID:</strong> {{ selectedPacket.identificacao }}</p>
      <p><strong>IP:</strong> {{ nodes[selectedNode].name }}</p>
      <p><strong>TTL:</strong> {{ selectedPacket.ttl }}</p>
      <p><strong>Protocolo:</strong> {{ selectedPacket.protocolo == 6 ? "TCP" : selectedPacket.protocolo == 2 ? "ICMP" : "UDP"}}</p>
    </div>
  </div>
</template>

<script>
import { nodes, edges, size, hues } from "./data";
import { configs } from "./configs";

export default {
  props: {
    packets: Object
  },
  data() {
    return {
      nodes,
      edges,
      hues,
      size,
      selectedNode: null,
      selectedPacket: null,
    };
  },

  computed: {
    configs,
    eventHandlers() {
      return {
        "node:pointerover": ({ node }) => {
          this.handleHoverNode(node, "hover");
        },

        "node:pointerout": ({ node }) => {
          this.handleHoverNode(node, "default", "lightgrey");
        },

        "edge:pointerover": ({ edge }) => {
          this.handleHoverEdge(edge, "hover");
        },

        "edge:pointerout": ({ edge }) => {
          this.handleHoverEdge(edge, "default", "lightgrey");
        },

        "node:click": ({ node }) => {
          if(this.packets.type == 0) {
            this.handleClickNode(node);
          }
        },
      };
    }
  },

  watch: {
    packets: {
      handler(newPackets) {
        if (newPackets.data.length > 0) {
          this.generateNodes();
        }
      },
      deep: true
    },
    selectedNode(newVal) {
      if (newVal !== null) {
        this.updateSelectedPacket(newVal);
      }
    }
  },

  methods: {
    handleHoverNode(node, size, color) {
      const isSource = this.edges.some((edge) => edge.source === node);
      const type = isSource ? "source" : "target";

      this.edges.forEach((edge) => {
        if (edge[type] === node) {
          const defaultColor = `hsl(${edge.hue}, 50%, 50%)`;
          this.$refs[edge.source].style.stroke = color ?? defaultColor;
          this.$refs[edge.source].style.strokeWidth = this.size[size];

          this.$refs[edge.target].style.stroke = color ?? defaultColor;
          this.$refs[edge.target].style.strokeWidth = this.size[size];
        }
      });
    },

    handleClickNode(nodeId) {
      if (this.selectedNode !== null) {
        this.resetNodeStyles(this.selectedNode);
      }

      this.selectedNode = nodeId;
      this.applyNodeStyles(nodeId);
    },

    resetNodeStyles(nodeId) {
      const defaultColor = "lightgrey";
      this.$refs[nodeId].style.stroke = defaultColor;
      this.$refs[nodeId].style.strokeWidth = this.size.default;
    },
    
    applyNodeStyles(nodeId) {
      const selectedColor = "blue";
      this.$refs[nodeId].style.stroke = selectedColor;
      this.$refs[nodeId].style.strokeWidth = this.size.default + 2;
    },

    handleHoverEdge(edge, size, color) {
      const edgeData = this.edges[edge]; // Acessa o objeto de edge diretamente

      if (edgeData) { // Verifica se edgeData está definido
        const { source, target, hue } = edgeData;
        const defaultColor = `hsl(${hue}, 50%, 50%)`;

        if (this.$refs[source]) {
          this.$refs[source].style.strokeWidth = this.size[size];
          this.$refs[source].style.stroke = color ?? defaultColor;
        }

        if (this.$refs[target]) {
          this.$refs[target].style.strokeWidth = this.size[size];
          this.$refs[target].style.stroke = color ?? defaultColor;
        }
      }
    },

    generateNodes() {
      if (this.packets.type === 0) {
        this.generateIpv4Nodes();
      } else if (this.packets.type === 1) {
        this.generateArpNodes();
      } 
    },

    generateIpv4Nodes() {
      this.generateIpsList();

      this.nodes = [];
      this.edges = [];

      this.ips.forEach((ip, index) => {
        const nodeIndex = index + 1;
        const nodeName = `node${nodeIndex}`;
        this.nodes[nodeName] = { name: ip, edgeWidth: 1, hue: 200 };
      });
      
      this.packets.data.forEach((pacote, index) => {
        const sourceNodeIndex = index + 1;
        const sourceNodeName = `node${sourceNodeIndex}`;
        const targetNodeIndex = this.packets.data.findIndex(p => p.ip_origem === pacote.ip_destino) + 1;
        const targetNodeName = `node${targetNodeIndex}`;
        const edgeName = `edge${index + 1}`;
        this.edges[edgeName] = { 
          source: sourceNodeName, 
          target: targetNodeName, 
          edgeWidth: 1, 
          hue: hues[Math.floor(Math.random() * hues.length)],
          dashed: sourceNodeIndex !== targetNodeIndex, 
        };
      });
    },

    generateArpNodes() {
      this.generateUniqueMacsList();

      this.nodes = [];
      this.edges = [];

      this.ips.forEach((ip, index) => {
        const nodeIndex = index + 1;
        const nodeName = `node${nodeIndex}`;
        this.nodes[nodeName] = { name: ip, edgeWidth: 1, hue: 200 };
      });

      // Criação das edges com base nos pacotes ARP
      this.packets.data.forEach((pacote, index) => {
        const sourceNodeIndex = this.ips.indexOf(pacote.sender_hardware_address) + 1;
        const sourceNodeName = `node${sourceNodeIndex}`;
        const targetNodeIndex = this.ips.indexOf(pacote.target_hardware_address) + 1;
        const targetNodeName = `node${targetNodeIndex}`;
        const edgeName = `edge${index + 1}`;
        
        // Verificação se os nodes de origem e destino são válidos
        //if (sourceNodeIndex > 0 && targetNodeIndex > 0) {
          this.edges[edgeName] = {
            source: sourceNodeName,
            target: targetNodeName,
            edgeWidth: 1,
            hue: hues[Math.floor(Math.random() * hues.length)],
          };
        //} else {
          //console.warn(`Pacote ${index + 1}: endereço MAC não encontrado.`);
        //}
      });
    },

    generateIpsList() {
      const ipsOrigem = this.packets.data.map(pacote => pacote.ip_origem);
      const ipsDestino = this.packets.data.map(pacote => pacote.ip_destino);

      // Combina os dois arrays
      const todosIps = [...ipsOrigem, ...ipsDestino];

      // Remove os valores duplicados
      this.ips = todosIps.filter((ip, index) => todosIps.indexOf(ip) === index);
    },

    generateUniqueMacsList() {
      const ipsOrigem = this.packets.data.map(packet => packet.sender_hardware_address);
      const ipsDestino = this.packets.data.map(packet => packet.target_hardware_address);

      // Combina os dois arrays
      const todosIps = [...ipsOrigem, ...ipsDestino];

      // Remove os valores duplicados
      this.ips = todosIps.filter((ip, index) => todosIps.indexOf(ip) === index);
    },

    updateSelectedPacket(nodeId) {
      const selectedIP = this.nodes[nodeId].name;
      this.selectedPacket = this.packets.data.find(packet => 
        packet.ip_origem === selectedIP || packet.ip_destino === selectedIP
      );
    },
  }
};
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
}

.graph {
  width: 100vw;
  height: 100vh;
  position: relative;
}

.node-info {
  position: fixed;
  top: 10px;
  right: 20px;
  background: white;
  padding: 5px 10px;
  border: 1px solid lightgrey;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: justify;
}


</style>
