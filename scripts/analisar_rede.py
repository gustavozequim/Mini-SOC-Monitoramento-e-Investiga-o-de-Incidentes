#!/usr/bin/env python3

import argparse
import ipaddress
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ARQUIVO_PADRAO = (
    Path(__file__).resolve().parent.parent
    / "investigations"
    / "003-atividade-suspeita"
    / "eventos_rede.jsonl"
)

CAMPOS_OBRIGATORIOS = {
    "timestamp",
    "hostname",
    "process",
    "destination_ip",
    "destination_port",
    "protocol",
    "action",
}

PORTAS_DE_ATENCAO = {4444, 9001}


def validar_evento(evento):
    """Valida a estrutura e os valores de um evento de rede."""

    if not isinstance(evento, dict):
        raise ValueError("O registro precisa ser um objeto JSON.")

    ausentes = CAMPOS_OBRIGATORIOS - evento.keys()
    if ausentes:
        raise ValueError(
            f"Campos obrigatórios ausentes: {', '.join(sorted(ausentes))}"
        )

    for campo in ("hostname", "process", "protocol", "action"):
        if not isinstance(evento[campo], str) or not evento[campo].strip():
            raise ValueError(f"Campo '{campo}' precisa ser um texto não vazio.")

    valor_timestamp = evento["timestamp"]

    if not isinstance(valor_timestamp, str) or not valor_timestamp.strip():
        raise ValueError("Timestamp precisa ser um texto não vazio.")

    try:
        timestamp = datetime.fromisoformat(
            valor_timestamp.replace("Z", "+00:00")
        )
    except ValueError as erro:
        raise ValueError("Timestamp inválido.") from erro

    if timestamp.tzinfo is None:
        raise ValueError("Timestamp sem informação de fuso horário.")

    evento["timestamp"] = timestamp.astimezone(timezone.utc)

    ip_destino = evento["destination_ip"]

    if not isinstance(ip_destino, str) or not ip_destino.strip():
        raise ValueError("O endereço IP de destino precisa ser um texto não vazio.")

    try:
        ip_destino = str(ipaddress.ip_address(ip_destino))
    except ValueError as erro:
        raise ValueError("Endereço IP de destino inválido.") from erro

    evento["destination_ip"] = ip_destino

    porta = evento["destination_port"]
    if isinstance(porta, bool) or not isinstance(porta, int):
        raise ValueError("A porta de destino precisa ser um número inteiro.")

    if not 1 <= porta <= 65535:
        raise ValueError("Porta fora do intervalo válido (1–65535).")

    evento["protocol"] = evento["protocol"].upper()
    if evento["protocol"] not in {"TCP", "UDP"}:
        raise ValueError("Protocolo não suportado. Utilize TCP ou UDP.")

    evento["action"] = evento["action"].lower()
    if evento["action"] not in {"allowed", "blocked"}:
        raise ValueError("Ação inválida. Utilize 'allowed' ou 'blocked'.")

    return evento


def carregar_eventos(caminho):
    """Lê o arquivo JSONL e separa eventos válidos e inválidos."""

    eventos = []
    invalidos = 0

    with caminho.open("r", encoding="utf-8") as arquivo:
        for numero, linha in enumerate(arquivo, start=1):
            if not linha.strip():
                continue

            try:
                evento = json.loads(linha)
                eventos.append(validar_evento(evento))
            except (json.JSONDecodeError, ValueError) as erro:
                invalidos += 1
                print(f"[ERRO] Linha {numero}: {erro}")

    return eventos, invalidos


def analisar_eventos(eventos, limite_repeticoes):
    """Agrupa conexões e identifica indicadores para investigação."""

    por_processo = Counter(evento["process"] for evento in eventos)
    por_porta = Counter(evento["destination_port"] for evento in eventos)

    grupos = defaultdict(list)

    for evento in eventos:
        chave = (
            evento["hostname"],
            evento["process"],
            evento["destination_ip"],
            evento["destination_port"],
            evento["protocol"],
            evento["action"],
        )
        grupos[chave].append(evento)

    portas_convencionais = {22, 53, 80, 443}
    alertas = []

    for (hostname, processo, ip, porta, protocolo, acao), registros in sorted(grupos.items()):
        quantidade = len(registros)
        motivos = []

        if porta in PORTAS_DE_ATENCAO:
            motivos.append(
                f"Conexão com porta previamente definida para revisão ({porta})."
            )

        if quantidade >= limite_repeticoes and porta not in portas_convencionais:
            motivos.append(
                f"{quantidade} conexões para o mesmo destino pelo mesmo processo."
            )

        if motivos:
            regras = []
            if porta in PORTAS_DE_ATENCAO:
                regras.append("NET-001")
            if quantidade >= limite_repeticoes and porta not in portas_convencionais:
                regras.append("NET-002")

            alertas.append({
                "regra": "/".join(regras),
                "prioridade": "MEDIA",
                "hostname": hostname,
                "processo": processo,
                "destino": ip,
                "porta": porta,
                "protocolo": protocolo,
                "acao": acao,
                "quantidade": quantidade,
                "motivo": " ".join(motivos),
            })

    return por_processo, por_porta, alertas

def main():
    parser = argparse.ArgumentParser(
        description="Analisa eventos de conexão de rede em formato JSONL."
    )
    parser.add_argument(
        "--arquivo",
        type=Path,
        default=ARQUIVO_PADRAO,
        help="Caminho do arquivo JSONL.",
    )
    parser.add_argument(
        "--limite-repeticoes",
        type=int,
        default=3,
        help="Quantidade mínima de conexões repetidas para gerar alerta.",
    )

    args = parser.parse_args()

    if args.limite_repeticoes < 1:
        parser.error("--limite-repeticoes precisa ser maior que zero.")

    if not args.arquivo.is_file():
        print(f"[ERRO] Arquivo não encontrado: {args.arquivo}", file=sys.stderr)
        return 2

    try:
        eventos, invalidos = carregar_eventos(args.arquivo)
    except OSError as erro:
        print(f"[ERRO] Não foi possível ler o arquivo: {erro}", file=sys.stderr)
        return 2

    por_processo, por_porta, alertas = analisar_eventos(
        eventos, args.limite_repeticoes
    )

    print("========== ANÁLISE DE EVENTOS DE REDE ==========")
    print(f"Arquivo: {args.arquivo}")
    print(f"Eventos válidos: {len(eventos)}")
    print(f"Eventos inválidos: {invalidos}")

    print("\n========== CONEXÕES POR PROCESSO ==========")
    for processo, quantidade in sorted(por_processo.items()):
        print(f"{processo}: {quantidade}")

    print("\n========== CONEXÕES POR PORTA ==========")
    for porta, quantidade in sorted(por_porta.items()):
        print(f"{porta}: {quantidade}")

    print("\n========== ALERTAS ==========")

    if not alertas:
        print("Nenhum indicador identificado pelas regras configuradas.")
    else:
        for numero, alerta in enumerate(alertas, start=1):
            print(f"\nAlerta {numero} — {alerta['regra']}")
            print(f"Prioridade: {alerta['prioridade']}")
            print(f"Host: {alerta['hostname']}")
            print(f"Processo: {alerta['processo']}")
            print(f"Ação: {alerta['acao']}")
            print(f"Destino: {alerta['destino']}:{alerta['porta']}")
            print(f"Protocolo: {alerta['protocolo']}")
            print(f"Conexões observadas: {alerta['quantidade']}")
            print(f"Motivo: {alerta['motivo']}")

    print("\n========== RESULTADO ==========")
    print(f"Total de alertas: {len(alertas)}")

    if invalidos:
        print("Atenção: existem registros inválidos que foram descartados.")

    return 1 if alertas else 0


if __name__ == "__main__":
    sys.exit(main())
