#!/usr/bin/env python3
"""Monitoramento de integridade de arquivos usando SHA-256."""

import argparse
import hashlib
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_TARGET = BASE_DIR / "investigations/002-integridade-arquivos/amostra"
DEFAULT_BASELINE = BASE_DIR / "investigations/002-integridade-arquivos/baseline_sha256.json"


def calcular_sha256(caminho):
    """Calcula o SHA-256 lendo o arquivo em blocos."""
    digest = hashlib.sha256()

    with caminho.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(65536), b""):
            digest.update(bloco)

    return digest.hexdigest()


def coletar_hashes(diretorio):
    """Retorna os hashes dos arquivos regulares, identificados por caminho relativo."""
    if not diretorio.is_dir():
        raise ValueError(f"Diretorio inexistente: {diretorio}")

    hashes = {}

    for caminho in sorted(diretorio.rglob("*")):
        if caminho.is_symlink():
            raise ValueError(f"Link simbolico nao permitido: {caminho}")

        if caminho.is_file():
            relativo = caminho.relative_to(diretorio).as_posix()
            hashes[relativo] = calcular_sha256(caminho)

    return hashes


def salvar_baseline(caminhos, arquivo_baseline):
    """Salva uma linha de base JSON com hashes SHA-256."""
    documento = {
        "algoritmo": "SHA-256",
        "arquivos": caminhos,
    }

    arquivo_baseline.parent.mkdir(parents=True, exist_ok=True)
    arquivo_baseline.write_text(
        json.dumps(documento, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def carregar_baseline(arquivo_baseline):
    """Carrega e valida a estrutura da linha de base."""
    try:
        documento = json.loads(arquivo_baseline.read_text(encoding="utf-8"))
    except FileNotFoundError as erro:
        raise ValueError(f"Linha de base nao encontrada: {arquivo_baseline}") from erro
    except (json.JSONDecodeError, UnicodeDecodeError) as erro:
        raise ValueError("Linha de base invalida: JSON ilegivel.") from erro

    if not isinstance(documento, dict):
        raise ValueError("Linha de base invalida: esperado um objeto JSON.")

    if documento.get("algoritmo") != "SHA-256":
        raise ValueError("Linha de base invalida: algoritmo ausente ou nao suportado.")

    arquivos = documento.get("arquivos")
    if not isinstance(arquivos, dict):
        raise ValueError("Linha de base invalida: campo 'arquivos' invalido.")

    for nome, digest in arquivos.items():
        if (
            not isinstance(nome, str)
            or not nome
            or nome.startswith("/")
            or ".." in Path(nome).parts
            or not isinstance(digest, str)
            or len(digest) != 64
            or any(caractere not in "0123456789abcdef" for caractere in digest)
        ):
            raise ValueError("Linha de base invalida: caminho ou hash incorreto.")

    return arquivos


def verificar_integridade(atuais, baseline):
    """Classifica arquivos novos, removidos e modificados."""
    novos = sorted(atuais.keys() - baseline.keys())
    removidos = sorted(baseline.keys() - atuais.keys())
    modificados = sorted(
        nome
        for nome in atuais.keys() & baseline.keys()
        if atuais[nome] != baseline[nome]
    )

    return novos, removidos, modificados


def criar_parser():
    parser = argparse.ArgumentParser(
        description="Monitora a integridade de arquivos usando hashes SHA-256."
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    for nome in ("baseline", "verificar"):
        subparser = subparsers.add_parser(nome)
        subparser.add_argument(
            "--diretorio",
            type=Path,
            default=DEFAULT_TARGET,
            help="Diretorio de arquivos monitorados.",
        )
        subparser.add_argument(
            "--baseline",
            type=Path,
            default=DEFAULT_BASELINE,
            help="Arquivo JSON da linha de base.",
        )

    return parser


def main():
    args = criar_parser().parse_args()

    try:
        atuais = coletar_hashes(args.diretorio)

        if not atuais:
            raise ValueError("Nenhum arquivo regular encontrado no diretorio.")

        if args.comando == "baseline":
            salvar_baseline(atuais, args.baseline)
            print(f"Linha de base criada: {args.baseline}")
            print(f"Arquivos registrados: {len(atuais)}")
            return 0

        baseline = carregar_baseline(args.baseline)
        novos, removidos, modificados = verificar_integridade(atuais, baseline)

    except (OSError, ValueError) as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 2

    print("=== Verificacao de integridade ===")
    print(f"Arquivos atuais: {len(atuais)}")
    print(f"Arquivos na linha de base: {len(baseline)}")
    print(f"Novos: {len(novos)}")
    print(f"Removidos: {len(removidos)}")
    print(f"Modificados: {len(modificados)}")

    for categoria, nomes in (
        ("NOVO", novos),
        ("REMOVIDO", removidos),
        ("MODIFICADO", modificados),
    ):
        for nome in nomes:
            print(f"[{categoria}] {nome}")

    if novos or removidos or modificados:
        print("RESULTADO: ALTERACOES DETECTADAS")
        return 1

    print("RESULTADO: NENHUMA ALTERACAO DETECTADA")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
