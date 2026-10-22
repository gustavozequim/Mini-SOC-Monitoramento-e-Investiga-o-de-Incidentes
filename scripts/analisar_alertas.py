#!/usr/bin/env python3
"""Analisador didático de autenticação para o projeto Mini-SOC."""

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


CAMPOS_OBRIGATORIOS = {
    "timestamp",
    "event_type",
    "username",
    "source_ip",
}
TIPOS_VALIDOS = {"login_failed", "login_success"}


def carregar_eventos(caminho):
    """Carrega JSONL e registra erros sem interromper a análise."""
    eventos = []
    erros = []

    with caminho.open("r", encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            if not linha.strip():
                continue

            try:
                evento = json.loads(linha)
            except json.JSONDecodeError:
                erros.append(f"Linha {numero_linha}: JSON inválido.")
                continue

            if not isinstance(evento, dict):
                erros.append(
                    f"Linha {numero_linha}: esperado um objeto JSON."
                )
                continue

            faltantes = CAMPOS_OBRIGATORIOS - evento.keys()
            if faltantes:
                nomes = ", ".join(sorted(faltantes))
                erros.append(
                    f"Linha {numero_linha}: campos ausentes: {nomes}."
                )
                continue

            if not all(
                isinstance(evento[campo], str) and evento[campo].strip()
                for campo in CAMPOS_OBRIGATORIOS
            ):
                erros.append(
                    f"Linha {numero_linha}: os campos obrigatórios "
                    "devem ser textos não vazios."
                )
                continue

            if evento["event_type"] not in TIPOS_VALIDOS:
                erros.append(
                    f"Linha {numero_linha}: tipo de evento desconhecido."
                )
                continue

            try:
                timestamp_texto = evento["timestamp"]
                if timestamp_texto.endswith("Z"):
                    timestamp_texto = timestamp_texto[:-1] + "+00:00"

                timestamp = datetime.fromisoformat(timestamp_texto)

                # Timestamps sem fuso são interpretados como UTC neste laboratório.
                if timestamp.tzinfo is None:
                    timestamp = timestamp.replace(tzinfo=timezone.utc)
                else:
                    timestamp = timestamp.astimezone(timezone.utc)

            except ValueError:
                erros.append(
                    f"Linha {numero_linha}: timestamp inválido."
                )
                continue

            evento["_timestamp_dt"] = timestamp
            eventos.append(evento)

    return eventos, erros


def detectar_por_chave(eventos, chave, tipo_alerta, limite, janela):
    """Detecta limiares em janelas deslizantes, agrupando por uma chave."""
    grupos = defaultdict(list)

    for evento in eventos:
        if evento["event_type"] == "login_failed":
            grupos[evento[chave]].append(evento["_timestamp_dt"])

    alertas = []

    for alvo, timestamps in sorted(grupos.items()):
        timestamps.sort()
        inicio = 0

        for fim, instante_atual in enumerate(timestamps):
            while (
                instante_atual - timestamps[inicio] > janela
            ):
                inicio += 1

            quantidade = fim - inicio + 1

            if quantidade >= limite:
                alertas.append({
                    "tipo": tipo_alerta,
                    "alvo": alvo,
                    "quantidade": quantidade,
                    "limite": limite,
                    "janela_minutos": int(janela.total_seconds() // 60),
                    "inicio": timestamps[inicio],
                    "fim": instante_atual,
                })
                # Um alerta por alvo nesta versão inicial.
                break

    return alertas


def analisar_eventos(eventos, limite, janela_minutos):
    """Resume falhas e detecta padrões por IP e por usuário."""
    falhas_por_ip = Counter()
    falhas_por_usuario = Counter()

    for evento in eventos:
        if evento["event_type"] == "login_failed":
            falhas_por_ip[evento["source_ip"]] += 1
            falhas_por_usuario[evento["username"]] += 1

    janela = timedelta(minutes=janela_minutos)

    alertas = detectar_por_chave(
        eventos,
        "source_ip",
        "MULTIPLAS_FALHAS_POR_IP",
        limite,
        janela,
    )
    alertas += detectar_por_chave(
        eventos,
        "username",
        "MULTIPLAS_FALHAS_POR_USUARIO",
        limite,
        janela,
    )

    return falhas_por_ip, falhas_por_usuario, alertas


def main():
    parser = argparse.ArgumentParser(
        description="Analisa eventos de autenticação em formato JSONL."
    )
    parser.add_argument(
        "--arquivo",
        type=Path,
        default=Path(
            "investigations/001-falhas-autenticacao/eventos_auth.jsonl"
        ),
        help="Caminho do arquivo JSONL.",
    )
    parser.add_argument(
        "--limite",
        type=int,
        default=5,
        help="Falhas mínimas para gerar alerta (padrão: 5).",
    )
    parser.add_argument(
        "--janela-minutos",
        type=int,
        default=5,
        help="Duração da janela de detecção em minutos (padrão: 5).",
    )
    args = parser.parse_args()

    if args.limite < 1:
        parser.error("--limite deve ser maior ou igual a 1.")
    if args.janela_minutos < 1:
        parser.error("--janela-minutos deve ser maior ou igual a 1.")
    if not args.arquivo.is_file():
        parser.error(f"Arquivo não encontrado: {args.arquivo}")

    eventos, erros = carregar_eventos(args.arquivo)

    falhas_por_ip, falhas_por_usuario, alertas = analisar_eventos(
        eventos, args.limite, args.janela_minutos
    )

    print("=== Mini-SOC | Análise de autenticação ===")
    print(f"Arquivo: {args.arquivo}")
    print(f"Eventos válidos: {len(eventos)}")
    print(f"Registros inválidos: {len(erros)}")

    for erro in erros:
        print(f"[ERRO] {erro}")

    print("\n--- Total de falhas por IP (arquivo inteiro) ---")
    for ip, quantidade in sorted(falhas_por_ip.items()):
        print(f"{ip}: {quantidade}")

    print("\n--- Total de falhas por usuário (arquivo inteiro) ---")
    for usuario, quantidade in sorted(falhas_por_usuario.items()):
        print(f"{usuario}: {quantidade}")

    print(
        f"\n--- Alertas: limite {args.limite}, "
        f"janela {args.janela_minutos} minuto(s) ---"
    )

    if not alertas:
        print("Nenhum alerta gerado.")
    else:
        for alerta in alertas:
            inicio = alerta["inicio"].isoformat()
            fim = alerta["fim"].isoformat()
            print(
                f"[ALERTA] {alerta['tipo']} | "
                f"alvo={alerta['alvo']} | "
                f"falhas_na_janela={alerta['quantidade']} | "
                f"limite={alerta['limite']} | "
                f"inicio={inicio} | fim={fim}"
            )


if __name__ == "__main__":
    main()
