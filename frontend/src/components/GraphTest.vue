<template>
    <v-network-graph
    class="graph"
    :nodes="nodes"
    :edges="edges"
    :configs="configs"
  />
</template>

<script>
import * as vNG from "v-network-graph"

export default {
  name: 'GraphTest',
  components: {
    
  },
  props: {
    pacotes: Array
  },
  mounted() {
    this.generateNodes()
  },
  watch: {
    pacotes: {
      handler(newPacotes) {
        if (newPacotes.length > 0) {
          this.generateNodes();
        }
      },
      deep: true
    }
  },
  data() {
    return {
        ips: [],
        configs: vNG.defineConfigs({
        view: {
            layoutHandler: new vNG.GridLayout({ grid: 15 }),
        },
        }),
         nodes: {
            node1: { name: "Node 1" },
            node2: { name: "Node 2" },
            node3: { name: "Node 3" },
            node4: { name: "Node 4" },
        },

         edges: {
            edge1: { source: "node1", target: "node2" },
            edge2: { source: "node2", target: "node3" },
            edge3: { source: "node3", target: "node4" },
            edge4: { source: "node2", target: "node4" }
        }
    };
  },
  methods: {

    generateIps() {
      const ipsOrigem = this.pacotes.map(pacote => pacote.ip_origem);
      const ipsDestino = this.pacotes.map(pacote => pacote.ip_destino);

      // Combina os dois arrays
      const todosIps = [...ipsOrigem, ...ipsDestino];

      // Remove os valores duplicados
      this.ips = todosIps.filter((ip, index) => todosIps.indexOf(ip) === index);
    },
  
    generateNodes() {
      this.generateIps();

      this.ips.forEach((ip, index) => {
            console.log("pacote ", index);
            var nodeIndex = index + 1;
            const nodeName = `node${nodeIndex}`;
            this.nodes[nodeName] = { name: ip };
        });
      
        console.log("gerando os pacotes...");

        this.pacotes.forEach((pacote, index) => {
            var sourceNodeIndex = index + 1;
            var sourceNodeName = `node${sourceNodeIndex}`;
            var targetNodeIndex = this.pacotes.findIndex(p => p.ip_origem === pacote.ip_destino) + 1;
            var targetNodeName = `node${targetNodeIndex}`;
            var edgeName = `edge${index + 1}`;
            this.edges[edgeName] = { source: sourceNodeName, target: targetNodeName };
        });
        

    // Criando as arestas com base nos nós de origem e destino
   
    },
  }
};
</script>

<style scoped>
.graph {
  width: 100vw; /* ajuste conforme necessário */
  height: 100vh; /* ajuste conforme necessário */
}
</style>
