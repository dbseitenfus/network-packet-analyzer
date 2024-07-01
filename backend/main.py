from fastapi import FastAPI, UploadFile, File
from typing import List
import dpkt
import io
from starlette.middleware.cors import CORSMiddleware
from collections import Counter
import requests
import uvicorn
from netaddr import EUI

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

@app.get("/")
def read_root():
    return {"Hello world"}

@app.post("/ipv4/list_packages")
async def listar_pacotes_ipv4(pcap_file: UploadFile = File(...)):
    global pacotes
    pacotes = []
    conteudo = await pcap_file.read()
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
                "versao": ip.v,
                "tamanho_cabecalho": ip.hl * 4,  # Tamanho do cabeçalho em bytes
                "tipo_servico": ip.tos,
                "comprimento_total": ip.len,
                "identificacao": ip.id,
                "flags": ip.off >> 13, 
                "deslocamento_fragmento": ip.off & dpkt.ip.IP_OFFMASK,
                "ttl": ip.ttl,
                "soma_verificacao": ip.sum,
                "protocolo": ip.p,
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

@app.post("/arp/list_packages")
async def listar_pacotes_arp(pcap_file: UploadFile = File(...)):
    global pacotes_arp
    pacotes_arp = []
    conteudo = await pcap_file.read()
    captura = dpkt.pcap.Reader(io.BytesIO(conteudo))

    for timestamp, buf in captura:
        # Decodificar o pacote Ethernet
        pacote_eth = dpkt.ethernet.Ethernet(buf)

        # Verificar se o pacote é do tipo ARP
        if isinstance(pacote_eth.data, dpkt.arp.ARP):
            arp = pacote_eth.data

            # Adicionar informações do pacote ARP à lista
            pacotes_arp.append({
                "timestamp": timestamp,
                "operation": arp.op,
                "sender_hardware_address": ":".join("{:02x}".format(b) for b in arp.sha),
                "sender_protocol_address": dpkt.utils.inet_to_str(arp.spa),
                "target_hardware_address": ":".join("{:02x}".format(b) for b in arp.tha),
                "target_protocol_address": dpkt.utils.inet_to_str(arp.tpa),
            })
            
    return {"mensagem": "Pacotes ARP processados com sucesso", "pacotes": pacotes_arp}
