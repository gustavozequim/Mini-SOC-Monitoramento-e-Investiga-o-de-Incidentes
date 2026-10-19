# Mini SOC — Monitoramento e Investigação de Incidentes

## 1. Sobre o projeto

Este projeto tem como objetivo construir um ambiente controlado de monitoramento de segurança, investigar eventos simulados e produzir relatórios técnicos de incidentes, aplicando conceitos fundamentais de **Blue Team, SOC (Security Operations Center), análise de logs e resposta a incidentes**.

O laboratório simula atividades comuns, incluindo monitoramento de eventos, identificação de comportamentos suspeitos, triagem de alertas e documentação dos resultados.

O ambiente será utilizado exclusivamente para fins educacionais, com sistemas e eventos controlados.

## 2. Objetivos

- Configurar um ambiente de monitoramento de segurança.
- Centralizar e analisar logs de sistemas Windows e/ou Linux.
- Utilizar um SIEM para identificar eventos potencialmente suspeitos.
- Investigar alertas e diferenciar comportamentos legítimos de possíveis incidentes.
- Desenvolver scripts em Python para automatizar tarefas de análise.
- Correlacionar eventos com técnicas documentadas no MITRE ATT&CK.
- Produzir relatórios técnicos com evidências, conclusões e recomendações.

## 3. Tecnologias e ferramentas

| Tecnologia | Finalidade |
|---|---|
| Wazuh | Monitoramento, análise de eventos e gerenciamento de alertas |
| Linux | Administração do ambiente e análise de logs |
| Windows | Geração e investigação de eventos do sistema |
| Python | Automação e processamento de logs |
| Wireshark | Análise de tráfego de rede, quando aplicável |
| MITRE ATT&CK | Classificação de táticas e técnicas adversárias |
| Git e GitHub | Versionamento e documentação do projeto |

*As ferramentas serão incorporadas conforme a evolução do laboratório. A lista não significa que todas já estejam configuradas.*

## 4. Arquitetura do laboratório

A arquitetura inicial prevê uma máquina responsável pelo monitoramento e um ou mais endpoints gerando eventos para análise.

```text
             +----------------------+
             |   Analista SOC N1    |
             +----------+-----------+
                        |
                        v
             +----------------------+
             |    Wazuh SIEM        |
             | Alertas e eventos    |
             +----------+-----------+
                        |
              +---------+---------+
              |                   |
              v                   v
     +----------------+  +----------------+
     | Endpoint Linux |  | Endpoint Windows|
     | Logs e eventos |  | Logs e eventos  |
     +----------------+  +----------------+

             +----------------------+
             | Scripts em Python    |
             | Análise automatizada |
             +----------------------+
```

A topologia poderá ser adaptada de acordo com os recursos disponíveis no computador e com a evolução do laboratório.

## 5. Cenários de investigação

### Cenário 1 — Tentativas repetidas de autenticação

**Objetivo:** identificar possíveis padrões de força bruta ou password spraying.

Atividades:
- Coletar eventos de falha de autenticação.
- Identificar endereços IP, usuários e horários envolvidos.
- Agrupar ocorrências por intervalo de tempo.
- Avaliar se o comportamento pode indicar uma tentativa de acesso indevido.
- Registrar evidências e recomendar ações de mitigação.

**Resultado esperado:** relatório de triagem com eventos relevantes, hipótese investigativa e conclusão fundamentada.

### Cenário 2 — Processo incomum em um endpoint

**Objetivo:** investigar a execução de um processo potencialmente suspeito.

Atividades:
- Identificar o nome e o caminho do processo.
- Analisar usuário, horário de execução e processo pai.
- Examinar linha de comando e hash do arquivo, quando disponíveis.
- Correlacionar os dados com outros eventos do sistema.
- Avaliar a possibilidade de falso positivo.

**Resultado esperado:** registro da investigação com evidências e justificativa para a classificação do evento.

### Cenário 3 — Conexão de rede suspeita

**Objetivo:** investigar uma conexão potencialmente relacionada a atividade maliciosa.

Atividades:
- Identificar endereço IP, domínio, porta e protocolo envolvidos.
- Consultar fontes confiáveis de reputação, quando apropriado.
- Correlacionar os dados com processos e eventos do endpoint.
- Avaliar possíveis indicadores de comprometimento (IoCs).
- Documentar a análise e as medidas recomendadas.

**Resultado esperado:** relatório com contexto da conexão, evidências disponíveis e avaliação de risco.

> Os cenários serão executados em ambiente controlado. A presença de um indicador isolado não será tratada automaticamente como prova de comprometimento.

## 6. Automação com Python

O projeto também prevê o desenvolvimento de scripts para auxiliar na análise de eventos.

Funcionalidades planejadas:
- Leitura e processamento de arquivos de log.
- Identificação de falhas de autenticação.
- Agrupamento de eventos por IP, usuário e horário.
- Identificação de padrões que mereçam investigação.
- Exportação de resultados para CSV ou JSON.
- Geração de resumos para apoiar a documentação dos incidentes.

Os scripts funcionarão como ferramentas auxiliares de triagem, sem substituir a validação manual ou os mecanismos de detecção do SIEM.

## 7. Metodologia de investigação

Cada cenário seguirá um fluxo de trabalho inspirado nas atividades de um SOC:

1. **Detecção:** identificar o alerta ou comportamento relevante.
2. **Triagem:** avaliar severidade, contexto e prioridade.
3. **Coleta de evidências:** reunir logs e informações relacionadas.
4. **Investigação:** correlacionar eventos e testar hipóteses.
5. **Classificação:** registrar a conclusão e a confiança da análise.
6. **Escalonamento:** recomendar encaminhamento quando necessário.
7. **Documentação:** produzir um relatório técnico com evidências e próximos passos.

As ações de contenção serão realizadas somente em ambientes próprios ou autorizados e conforme o escopo definido para o laboratório.

## 8. Estrutura planejada do repositório

```text
mini-soc-lab/
├── README.md
├── docs/
│   ├── arquitetura.md
│   ├── metodologia.md
│   └── relatorios/
│       ├── incidente-001.md
│       ├── incidente-002.md
│       └── incidente-003.md
├── scripts/
│   ├── log_analyzer.py
│   └── requirements.txt
├── samples/
│   └── README.md
└── screenshots/
    └── README.md
```

Os diretórios e arquivos serão adicionados conforme o desenvolvimento. Os nomes acima representam uma estrutura proposta, não arquivos necessariamente já existentes.

## 9. Modelo de relatório de incidente

Cada investigação deverá registrar:

- **ID do incidente:**
- **Data e horário:**
- **Tipo de evento:**
- **Origem do alerta:**
- **Severidade inicial:**
- **Ativo ou endpoint envolvido:**
- **Descrição do evento:**
- **Evidências coletadas:**
- **Análise realizada:**
- **Possível técnica MITRE ATT&CK:**
- **Conclusão:** verdadeiro positivo, falso positivo ou inconclusivo.
- **Recomendações:**
- **Necessidade de escalonamento:**

Nenhuma conclusão será registrada como fato sem evidências suficientes para sustentá-la.

## 10. Competências desenvolvidas

Este laboratório busca desenvolver competências relevantes para posições de entrada em segurança defensiva:

- Fundamentos de redes e protocolos.
- Análise de logs Windows e Linux.
- Monitoramento e triagem de alertas.
- Operação básica de SIEM.
- Investigação inicial de eventos suspeitos.
- Identificação e contextualização de IoCs.
- Noções de resposta a incidentes.
- Automação de tarefas com Python.
- Documentação e comunicação técnica.
- Aplicação do MITRE ATT&CK.

## 11. Status do projeto

**Status atual:** planejamento e implementação incremental.

| Etapa | Status |
|---|---|
| Definição dos objetivos e cenários | Planejado |
| Preparação do ambiente de laboratório | Pendente |
| Configuração do Wazuh | Pendente |
| Coleta e análise de logs | Pendente |
| Desenvolvimento dos scripts Python | Pendente |
| Execução dos cenários investigativos | Pendente |
| Produção dos relatórios técnicos | Pendente |
| Documentação dos resultados no GitHub | Pendente |

O status deverá ser atualizado conforme cada etapa for concluída e validada.

## 12. Considerações finais

O Mini SOC foi concebido como um projeto prático de aprendizagem em segurança defensiva. A proposta é transformar conhecimentos de redes, sistemas operacionais, análise de logs e programação em um fluxo de investigação documentado e reproduzível.

O objetivo final é demonstrar, por meio de configurações, scripts, evidências e relatórios reais do laboratório, a capacidade de executar tarefas introdutórias relacionadas à rotina de um analista SOC N1.

---
