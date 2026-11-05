# Evidências — Investigação 003: Atividade de Rede Suspeita

## Objetivo

Registrar os resultados dos testes do analisador de eventos de rede
implementado em Python.

## Arquivos

- `compilacao.txt`: validação sintática do script.
- `analise-padrao.txt`: execução com limite padrão de três conexões.
- `analise-limite-4.txt`: teste com limite de quatro conexões.
- `teste-parametro-invalido.txt`: validação de parâmetro inválido.
- `teste-validacao-ip.txt`: testes de validação de endereços IP.
- `teste-normalizacao-ip.txt`: teste de normalização de endereços IP.
- `teste-validacao-timestamp.txt`: testes de validação de timestamps.
- `teste-agrupamento-host-acao.txt`: teste de agrupamento por hostname e ação.

## Resultados

A amostra contém dez eventos sintéticos, todos válidos.

A análise padrão identificou dois fluxos que merecem revisão:

- Processo `curl`, destino `198.51.100.77`, porta TCP 9001.
- Processo `python3`, destino `203.0.113.50`, porta TCP 4444.

Os alertas apresentam informações de contexto, incluindo hostname,
processo, destino, porta, protocolo e ação.

O segundo fluxo também atingiu o limite de três conexões repetidas,
gerando os indicadores NET-001 e NET-002 consolidados em um alerta.

O teste com limite quatro manteve os dois alertas de porta, pois a regra
NET-001 não depende da quantidade de conexões.

O parâmetro zero foi rejeitado pelo programa, com código de saída 2.

## Validação de IP

Foram testados os seguintes cenários:

- IPv4 válido: aceito.
- IP numérico: rejeitado.
- IP vazio: rejeitado.
- Endereço IP inválido: rejeitado.

Resultado: 4 de 4 testes aprovados.

## Normalização de endereços IP

Além de validar os endereços IP, o analisador converte os valores
para sua representação canônica utilizando o módulo `ipaddress`.

No teste com IPv6, foram comparadas duas representações do mesmo
endereço:

- Formato expandido: `2001:0db8:0000:0000:0000:0000:0000:0001`.
- Formato abreviado: `2001:db8::1`.

Ambas foram normalizadas para `2001:db8::1`, permitindo que
representações equivalentes sejam agrupadas corretamente durante
a análise.

Resultado: teste aprovado.

Evidência: `teste-normalizacao-ip.txt`.

## Validação de timestamps

Foram testados seis cenários de validação:

- Timestamp ISO 8601 em UTC: aceito.
- Timestamp ISO 8601 com offset: aceito e normalizado para UTC.
- Timestamp sem fuso horário: rejeitado.
- Formato inválido: rejeitado.
- Valor numérico: rejeitado.
- String vazia: rejeitada.

Resultado: 6 de 6 testes aprovados.
Evidência: `teste-validacao-timestamp.txt`.

## Agrupamento dos eventos

Foi realizado um teste específico com três eventos que possuem o mesmo
processo, IP de destino, porta e protocolo, mas apresentam diferenças
de hostname e/ou ação.

O objetivo foi verificar se eventos distintos são mantidos em grupos
separados durante a análise.

Resultado: 3 alertas para 3 combinações distintas.

Evidência: `teste-agrupamento-host-acao.txt`.

Teste aprovado.

## Limitações

Os eventos são sintéticos. A regra NET-002 não considera uma janela
temporal e os alertas representam indicadores para investigação,
não confirmação de atividade maliciosa.

## Reprodutibilidade

Na raiz do repositório:

```bash
python3 -m py_compile scripts/analisar_rede.py

python3 scripts/analisar_rede.py \
  --arquivo investigations/003-atividade-suspeita/eventos_rede.jsonl

python3 scripts/analisar_rede.py \
  --arquivo investigations/003-atividade-suspeita/eventos_rede.jsonl \
  --limite-repeticoes 4

python3 scripts/analisar_rede.py \
  --arquivo investigations/003-atividade-suspeita/eventos_rede.jsonl \
  --limite-repeticoes 0
```
