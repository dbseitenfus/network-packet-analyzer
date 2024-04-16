<template>
    <v-network-graph
    class="graph"
    :nodes="nodes"
    :edges="edges"
  />
</template>

<script>

export default {
  name: 'GraphTest',
  components: {
    
  },
  props: {
    pacotes: Array
  },
  mounted() {

  },
  watch: {
    pacotes: {
      handler(newPacotes) {
        if (newPacotes.length > 0) {
          this.test();
        }
      },
      deep: true
    }
  },
  data() {
    return {
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
    test() {
        console.log(pacotes);
    }
  }
};
</script>

<style scoped>
.graph {
  width: 600px; /* ajuste conforme necessário */
  height: 400px; /* ajuste conforme necessário */
}
</style>
