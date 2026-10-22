# Evidências — Investigação 001

## Objetivo

Documentar os resultados reproduzíveis da análise de falhas de autenticação
realizada no laboratório Mini-SOC.

Todos os eventos são sintéticos e não representam dados de produção.

## Arquivos

- `ambiente-e-integridade.txt`: versão do Python, quantidade de eventos e hashes SHA-256.
- `analise-padrao.txt`: análise com limiar de 5 falhas em 5 minutos.
- `analise-janela-1-minuto.txt`: análise com janela de 1 minuto.
- `teste-parametro-invalido.txt`: rejeição de uma janela igual a zero.

## Como reproduzir

Execute os comandos a partir da raiz do repositório.

Análise padrão:

    python scripts/analisar_alertas.py

Análise com janela de 1 minuto:

    python scripts/analisar_alertas.py --janela-minutos 1

Validação de parâmetro inválido:

    python scripts/analisar_alertas.py --limite 5 --janela-minutos 0

O último comando deve ser rejeitado, com código de saída 2.

## Resultados observados

- 10 eventos válidos no dataset principal.
- 0 registros inválidos no dataset principal.
- 5 falhas associadas ao IP sintético `192.0.2.10`.
- 5 falhas associadas ao usuário sintético `ana`.
- Dois alertas no cenário principal: um por IP e outro por usuário.
- Nenhum alerta no teste com cinco falhas distribuídas por quatro minutos,
  utilizando uma janela de um minuto.

## Integridade

Os hashes SHA-256 foram registrados em `ambiente-e-integridade.txt`.

Para recalcular os hashes:

    sha256sum investigations/001-falhas-autenticacao/eventos_auth.jsonl
    sha256sum scripts/analisar_alertas.py
    sha256sum investigations/001-falhas-autenticacao/relatorio.md

Os hashes identificam o conteúdo dos arquivos no momento da coleta.
Se um arquivo for alterado, seu hash poderá mudar.

## Limitações

Os resultados demonstram o comportamento do analisador nos cenários
sintéticos testados. Não comprovam eficácia contra ataques reais nem
substituem a validação em um ambiente de monitoramento de produção.
