# Investigação 003 — Atividade de Rede Suspeita

## 1. Objetivo

Analisar eventos sintéticos de conexão de rede para identificar
indicadores que merecem investigação por um analista SOC.

## 2. Ambiente

- Sistema operacional: Fedora Linux
- Linguagem: Python 3
- Formato dos eventos: JSONL
- Host analisado: linux-lab
- Total de eventos: 10

## 3. Metodologia

Os eventos foram carregados e validados individualmente.

O analisador realiza:

- Validação dos campos obrigatórios.
- Validação do formato dos timestamps e da presença de fuso horário, com normalização para UTC.
- Validação e normalização dos endereços IP para representação canônica.
- Validação das portas, com valores inteiros entre 1 e 65535.
- Identificação de protocolos TCP e UDP.
- Validação das ações allowed e blocked.
- Contabilização de conexões por processo e porta.
- Identificação de conexões destinadas a portas de atenção.
- Identificação de conexões repetidas para o mesmo destino.

As estatísticas por processo e porta são contabilizadas globalmente.
Para a geração dos alertas, os eventos são agrupados pela combinação
de hostname, processo, IP de destino, porta, protocolo e ação.

Os alertas apresentam essas informações de contexto para facilitar
a análise dos eventos.

## 4. Indicadores identificados

### NET-001 — Conexão com porta de atenção

Processo: curl

Host: linux-lab

Destino: 198.51.100.77:9001

Protocolo: TCP

Ação: allowed

Prioridade: Média

### NET-001 e NET-002 — Conexões repetidas

Processo: python3

Host: linux-lab

Destino: 203.0.113.50:4444

Protocolo: TCP

Ação: allowed

Conexões observadas: 3

Prioridade: Média

As três conexões ocorreram entre 10:03:00 e 10:03:40 UTC.

## 5. Resultados dos testes

- Eventos válidos: 10.
- Eventos inválidos: 0.
- Alertas com limite padrão: 2.
- Alertas com limite de repetição 4: 2.
- Parâmetro zero: rejeitado com código de saída 2.
- Compilação do script: aprovada.
- Validação de IP: 4 de 4 testes aprovados.
- Normalização de IP: teste de equivalência entre representações IPv6 aprovado.
- Validação de timestamps: 6 de 6 testes aprovados.
- Teste de agrupamento por hostname e ação: 3 alertas para 3 combinações distintas.

Com limite quatro, a regra NET-002 deixa de identificar
as três conexões repetidas, mas NET-001 continua identificando
a porta 4444.

### 5.1. Validação de IP

Foram testados quatro cenários:

- IPv4 válido: aceito.
- IP numérico: rejeitado.
- IP vazio: rejeitado.
- Endereço IP inválido: rejeitado.

Todos os testes apresentaram o resultado esperado.

### 5.2. Normalização de endereços IP

Além da validação, o analisador utiliza o módulo `ipaddress`
para converter os endereços IP para sua representação canônica.

Foi testada a equivalência entre duas representações do mesmo
endereço IPv6:

- Formato expandido: `2001:0db8:0000:0000:0000:0000:0000:0001`.
- Formato abreviado: `2001:db8::1`.

Ambas foram normalizadas para `2001:db8::1`, permitindo que
representações equivalentes sejam agrupadas corretamente.

Resultado: teste aprovado.

Evidência: `evidence/003-atividade-suspeita/teste-normalizacao-ip.txt`.

### 5.3. Validação do agrupamento

Foi realizado um teste específico com três eventos que possuem
o mesmo processo e destino, mas apresentam diferenças de hostname
e/ou ação.

A chave de agrupamento considera:

- Hostname;
- Processo;
- IP de destino;
- Porta de destino;
- Protocolo;
- Ação (allowed ou blocked).

O analisador produziu três alertas separados, confirmando que
eventos com diferenças nesses campos não são consolidados
indevidamente.

### 5.4. Validação de timestamps

Foram testados seis cenários:

- ISO 8601 em UTC: aceito.
- ISO 8601 com offset: aceito e normalizado para UTC.
- Timestamp sem fuso horário: rejeitado.
- Formato inválido: rejeitado.
- Valor numérico: rejeitado.
- String vazia: rejeitada.

Todos os seis testes apresentaram o resultado esperado. A evidência está registrada em `evidence/003-atividade-suspeita/teste-validacao-timestamp.txt`.

## 6. Limitações

- Os eventos são sintéticos e não representam tráfego real.
- As portas de atenção são definidas estaticamente.
- As estatísticas por processo e porta são agregadas globalmente,
  sem segmentação por host.
- A regra de repetição não considera uma janela temporal.
- A prioridade dos alertas é fixa.
- Os indicadores exigem investigação adicional e não comprovam
  atividade maliciosa.

## 7. Conclusão

A análise identificou dois fluxos que merecem revisão.

O laboratório demonstrou validação de eventos, validação de endereços IP,
agrupamento de conexões, aplicação de regras de detecção e geração
de alertas com informações de contexto.

Em um ambiente real, seria necessário correlacionar os indicadores
com outras fontes de telemetria antes de concluir pela existência
de um incidente de segurança.

## 8. Referências às evidências

As saídas dos testes estão registradas em:

`evidence/003-atividade-suspeita/`

O arquivo README.md desse diretório descreve cada evidência
e os procedimentos para reproduzir as análises.
