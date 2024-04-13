from fastapi import FastAPI, UploadFile, File
from typing import List
import dpkt
import io
from starlette.middleware.cors import CORSMiddleware
from collections import Counter
from datetime import datetime
import requests
import uvicorn

app = FastAPI()

# Configuração do middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lista para armazenar os pacotes
pacotes = []
ips_origem = []

@app.get("/")
def read_root():
    return {"Hello world"}

@app.post("/listar_pacotes")
async def listar_pacotes(arquivo_pcap: UploadFile = File(...)):
    global pacotes
    pacotes = []
    conteudo = await arquivo_pcap.read()
    captura = dpkt.pcapng.Reader(io.BytesIO(conteudo))

    for timestamp, buf in captura:
        # Decodificar o pacote Ethernet
        pacote_eth = dpkt.ethernet.Ethernet(buf)

        # Verificar se o pacote é do tipo IPv4
        if isinstance(pacote_eth.data, dpkt.ip.IP):
            ip = pacote_eth.data

            # Adicionar informações do pacote à lista
            pacotes.append({
                "timestamp": timestamp,
                "ip_origem": dpkt.utils.inet_to_str(ip.src),
                "ip_destino": dpkt.utils.inet_to_str(ip.dst),
                "mac_origem": ":".join("{:02x}".format(b) for b in pacote_eth.src),
                "mac_destino": ":".join("{:02x}".format(b) for b in pacote_eth.dst),
                "protocolo": ip.p,
                "tipo_ethernet": pacote_eth.type
            })

    return {"mensagem": "Pacotes processados com sucesso", "pacotes": pacotes }

@app.get("/contar_ip/{endereco_ip}")
async def contar_ip(endereco_ip: str):
    global pacotes
    contador = Counter([pacote["ip_origem"] for pacote in pacotes])

    return {"endereco_ip": endereco_ip, "ocorrencias": contador[endereco_ip]}

@app.get("/listar_enderecos_ip")
async def listar_enderecos_ip():
    global pacotes

    # Extrair endereços IP únicos da lista de pacotes
    enderecos_ip_unicos = set(pacote["ip_origem"] for pacote in pacotes)

    return {"enderecos_ip": list(enderecos_ip_unicos)}