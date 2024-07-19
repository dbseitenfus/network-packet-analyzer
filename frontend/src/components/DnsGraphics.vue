<template>
  <div class="dns-graphics">
    <h2>Distribuição de Consultas DNS por Tipo de Consulta</h2>
    <PieChart
      v-for="(chartData, index) in groupedData"
      :key="index"
      :chartData="chartData"
      :title="chartData.title"
    />
  </div>
</template>

<script>
import PieChart from './PieChart.vue';

export default {
  name: 'DnsGraphics',
  components: {
    PieChart
  },
  props: {
    packets: Object
  },
  data() {
    return {
      groupedData: []
    };
  },
  watch: {
    packets: {
      handler(newPackets) {
        if (newPackets && newPackets.data && newPackets.data.length > 0) {
          this.groupPackets(newPackets.data);
        }
      },
      deep: true,
    }
  },
  methods: {
    groupPackets(packets) {
      const serverTypeGroups = {
        Authoritative: {},
        Recursive: {},
        'Recursion Desired': {}
      };

      packets.forEach(packet => {
        packet.server_type.forEach(type => {
          if (serverTypeGroups[type] !== undefined) {
            packet.queries.forEach(query => {
              const queryName = query.name;
              if (!serverTypeGroups[type][queryName]) {
                serverTypeGroups[type][queryName] = 0;
              }
              serverTypeGroups[type][queryName]++;
            });
          }
        });
      });

      this.groupedData = Object.keys(serverTypeGroups).reduce((acc, type) => {
        const labels = Object.keys(serverTypeGroups[type]);
        const data = Object.values(serverTypeGroups[type]);

        // Verifica se há dados antes de adicionar ao acc
        if (data.some(count => count > 0)) {
          const colors = labels.map(() => this.generateRandomColor());
          acc.push({
            title: `${type} DNS Queries`,
            labels,
            data,
            colors
          });
        }
        return acc;
      }, []);
    },
    generateRandomColor() {
      const r = Math.floor(Math.random() * 256);
      const g = Math.floor(Math.random() * 256);
      const b = Math.floor(Math.random() * 256);
      return `rgba(${r}, ${g}, ${b}, 0.6)`;
    }
  }
};
</script>

<style scoped>
.dns-graphics {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
}

h2 {
  width: 100%;
  text-align: center;
}
</style>
