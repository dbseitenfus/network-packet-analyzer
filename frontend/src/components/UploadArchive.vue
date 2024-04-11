<template>
    <n-upload>
        <n-button
        @update="uploadArchive($event)"
        >
            <template #icon>
                <n-icon size="20" color="#232343">
                    <cloud-upload/>
                </n-icon>
            </template>
        </n-button>
    </n-upload>
</template>

<script>
import { NUpload, NButton, NIcon } from "naive-ui";
import { CloudUpload } from "@vicons/ionicons5";
import axios from 'axios';

export default {
    components: {
        NUpload,
        NButton,
        NIcon,
        CloudUpload
    },
    data() {
        return {
            packages: []
        }
    },
    methods: {
        async uploadArchive(event) {
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
                this.packages = response.data.pacotes;

                console.log(this.packages);

                // Chama a função para criar os gráficos de IP
                // this.criarGraficoIP();
            } catch (error) {
                console.error("Erro ao enviar arquivo:", error);
            }
        },
    }
}
</script>

<style scoped>

</style>