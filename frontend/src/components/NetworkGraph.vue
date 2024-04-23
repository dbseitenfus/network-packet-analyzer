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
  </div>
</template>

<script>
import { nodes, edges, size, hues } from "./data";
import { configs } from "./configs";

export default {
  props: {
    pacotes: Array
  },

  data: () => ({
    nodes,
    edges,
    hues,
    size,
    testCaseCondition: false,
  }),

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
      };
    },
  },

  methods: {
    handleHoverNode(node, size, color) {
      const isSource = this.edges.some((edge) => edge.source === node);
      const type = isSource ? "source" : "target";

      this.edges.forEach((edge) => {
        if (edge[type] === node) {
          if (this.testCaseCondition) {
            edge.edgeWidth = this.size[size];
          }

          const defaultColor = `hsl(${edge.hue}, 50%, 50%)`;
          this.$refs[edge.source].style.stroke = color ?? defaultColor;
          this.$refs[edge.source].style.strokeWidth = this.size[size];

          this.$refs[edge.target].style.stroke = color ?? defaultColor;
          this.$refs[edge.target].style.strokeWidth = this.size[size];
        }
      });
    },

    handleHoverEdge(edge, size, color) {
      const { source, target, hue } = this.edges[edge];
      const defaultColor = `hsl(${hue}, 50%, 50%)`;

      this.$refs[source].style.strokeWidth = this.size[size];
      this.$refs[target].style.strokeWidth = this.size[size];

      this.$refs[source].style.stroke = color ?? defaultColor;
      this.$refs[target].style.stroke = color ?? defaultColor;
    },

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

      this.nodes = []
      this.edges = []

      this.ips.forEach((ip, index) => {
            console.log("pacote ", index);
            var nodeIndex = index + 1;
            const nodeName = `node${nodeIndex}`;
            this.nodes[nodeName] = { name: ip, edgeWidth: 1, hue: 200 };
        });
      
        console.log("gerando os pacotes...");

        this.pacotes.forEach((pacote, index) => {
            var sourceNodeIndex = index + 1;
            var sourceNodeName = `node${sourceNodeIndex}`;
            var targetNodeIndex = this.pacotes.findIndex(p => p.ip_origem === pacote.ip_destino) + 1;
            var targetNodeName = `node${targetNodeIndex}`;
            var edgeName = `edge${index + 1}`;
            this.edges[edgeName] = { source: sourceNodeName, target: targetNodeName, edgeWidth: 1, hue: hues[Math.floor(Math.random() * hues.length)] };
        });
    },
  },
};
</script>

<style>
html,
body {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
}

</style>
