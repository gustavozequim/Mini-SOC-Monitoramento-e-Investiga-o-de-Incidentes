# Mini-SOC — Monitoramento e Investigação de Incidentes

## 1. Sobre o projeto

O Mini-SOC é um laboratório educacional de segurança defensiva (Blue Team) voltado à análise de eventos, identificação de comportamentos suspeitos, automação de tarefas com Python e documentação de investigações técnicas.

O projeto utiliza dados sintéticos e arquivos controlados para reproduzir situações que podem ser relevantes em atividades de um SOC (Security Operations Center), permitindo desenvolver e testar procedimentos de análise sem depender, neste estágio, de uma infraestrutura de monitoramento em produção.

Atualmente, o repositório contém dois cenários implementados: análise de falhas de autenticação e monitoramento da integridade de arquivos por meio de hashes SHA-256.

## 2. Objetivos do laboratório

- Analisar eventos de autenticação e identificar padrões de falhas repetidas.
- Agrupar ocorrências por endereço IP, usuário e intervalo de tempo.
- Implementar verificações automatizadas com Python.
- Monitorar a integridade de arquivos utilizando hashes SHA-256.
- Armazenar evidências dos testes e das análises realizadas.
- Documentar procedimentos e resultados de forma reproduzível.
- Desenvolver competências práticas relacionadas à investigação inicial de eventos de segurança.

## 3. Tecnologias e ferramentas utilizadas

| Tecnologia ou ferramenta | Utilização atual |
|---|---|
| Python | Implementação dos scripts de análise e monitoramento |
| JSONL | Armazenamento de eventos sintéticos de autenticação |
| JSON | Armazenamento de dados estruturados, incluindo hashes de referência |
| SHA-256 | Verificação da integridade dos arquivos |
| Linux / Fedora | Ambiente de desenvolvimento do laboratório |
| Git e GitHub | Versionamento e documentação do projeto |
| KVM/QEMU e libvirt | Preparação e gerenciamento da máquina virtual destinada ao laboratório |

**Wazuh ainda não está instalado e validado.** Sua utilização como SIEM permanece uma etapa futura. A infraestrutura de virtualização já foi preparada, mas isso não representa a conclusão da configuração do SIEM.

## 4. Estrutura atual do repositório

```text
Mini-SOC-Monitoramento-e-Investiga-o-de-Incidentes/
├── README.md
├── docs/
│   ├── arquitetura.md
│   └── procedimentos.md
├── scripts/
│   ├── analisar_alertas.py
│   └── monitorar_integridade.py
├── investigations/
│   ├── 001-falhas-autenticacao/
│   │   ├── eventos_auth.jsonl
│   │   └── relatorio.md
│   ├── 002-integridade-arquivos/
│   │   ├── baseline_sha256.json
│   │   └── relatorio.md
│   └── 003-atividade-suspeita/
│       └── relatorio.md
└── evidence/
    ├── 001-falhas-autenticacao/
    └── 002-integridade-arquivos/
```

Os diretórios de evidências contêm registros associados aos cenários executados. Os arquivos exatos presentes em cada diretório podem evoluir conforme novos testes forem realizados.

O terceiro cenário possui um relatório, mas ainda não conta com uma implementação equivalente aos dois primeiros cenários.

## 5. Cenário 001 — Análise de falhas de autenticação

**Status:** implementado e testado com eventos sintéticos.

### Objetivo

Identificar padrões de falhas repetidas de autenticação que possam justificar uma investigação inicial, como possíveis tentativas de força bruta.

### Implementação

O arquivo `investigations/001-falhas-autenticacao/eventos_auth.jsonl` contém eventos sintéticos utilizados como entrada para o script `scripts/analisar_alertas.py`.

O script realiza a leitura e a análise dos eventos, contabiliza falhas por endereço IP e usuário e identifica ocorrências que atendem aos critérios configurados.

Entre as funcionalidades implementadas estão:

- Leitura de eventos em formato JSONL.
- Contabilização de falhas por IP e por usuário.
- Avaliação de ocorrências em janelas temporais.
- Geração de alertas quando os limiares configurados são atingidos.
- Validação de parâmetros de execução, incluindo rejeição de valores inválidos para a janela temporal.

### Evidências dos testes

Nos dados sintéticos utilizados nos testes iniciais, foram processados 10 eventos válidos, sem registros inválidos.

As falhas foram distribuídas da seguinte forma:

| Indicador | Resultado |
|---|---:|
| Eventos válidos | 10 |
| Eventos inválidos | 0 |
| Falhas associadas ao IP `192.0.2.10` | 5 |
| Falhas associadas ao IP `192.0.2.20` | 2 |
| Falhas associadas ao IP `192.0.2.30` | 1 |
| Falhas associadas ao usuário `ana` | 5 |
| Falhas associadas ao usuário `bruno` | 2 |
| Falhas associadas ao usuário `carla` | 1 |

O cenário utiliza limiares configurados para identificar múltiplas falhas de autenticação por IP e por usuário. Esses resultados demonstram o funcionamento da análise sobre a amostra utilizada, mas não representam uma detecção realizada em uma rede real.

As evidências registram resultados das análises, testes com janelas temporais e validação de parâmetros.

## 6. Cenário 002 — Monitoramento da integridade de arquivos

**Status:** implementado, com baseline SHA-256 e relatório de investigação.

### Objetivo

Verificar a integridade de arquivos comparando seus hashes SHA-256 com valores de referência previamente registrados.

### Implementação

O script `scripts/monitorar_integridade.py` implementa a funcionalidade de monitoramento de integridade utilizada no cenário.

O arquivo `investigations/002-integridade-arquivos/baseline_sha256.json` armazena os hashes de referência utilizados na verificação.

O cenário está organizado em torno de:

- Registro de uma referência de integridade (*baseline*).
- Cálculo e comparação de hashes SHA-256.
- Verificação de alterações em relação aos valores de referência.
- Registro dos resultados da análise e de suas evidências.

A comparação de hashes permite identificar diferenças no conteúdo dos arquivos monitorados. Por si só, uma alteração não comprova atividade maliciosa: é necessário avaliar o contexto e determinar se a mudança era esperada.

O relatório do cenário e os registros de evidências documentam o trabalho realizado.

## 7. Cenário 003 — Atividade suspeita

**Status:** documentação existente; implementação técnica pendente.

O diretório `investigations/003-atividade-suspeita/` contém um arquivo `relatorio.md`.

Até o momento, esse cenário não deve ser considerado uma investigação automatizada concluída. A implementação de mecanismos de detecção, a execução dos testes e a coleta de evidências correspondentes ainda precisam ser desenvolvidas e validadas.

## 8. Documentação e evidências

O repositório contém documentação técnica em `docs/` e registros associados às investigações em `evidence/`.

- `docs/arquitetura.md`: documentação da arquitetura do laboratório.
- `docs/procedimentos.md`: documentação dos procedimentos de trabalho.
- `evidence/001-falhas-autenticacao/`: evidências relacionadas à análise de autenticação.
- `evidence/002-integridade-arquivos/`: evidências relacionadas ao monitoramento de integridade.

Os relatórios das investigações registram o contexto, os procedimentos e os resultados dos respectivos cenários. As evidências devem ser interpretadas de acordo com a origem dos dados e o escopo de cada teste.

## 9. Ambiente de virtualização

O ambiente de desenvolvimento utiliza Fedora Workstation 44 e ferramentas de virtualização KVM/QEMU, gerenciadas por libvirt.

A máquina virtual `wazuh-soc` já foi criada e possui a seguinte configuração registrada:

| Recurso | Configuração |
|---|---|
| Virtualização | KVM/QEMU |
| Gerenciamento | libvirt |
| Memória configurada | 8 GiB |
| CPUs virtuais configuradas | 4 |
| Estado registrado | Desligada |

A máquina virtual está preparada para receber a instalação do ambiente de monitoramento. A instalação e a validação operacional do Wazuh ainda não foram concluídas.

## 10. Status atual do projeto

| Componente ou etapa | Status |
|---|---|
| Definição inicial dos objetivos e cenários | Concluída |
| Estrutura do repositório e versionamento | Implementados |
| Documentação da arquitetura e dos procedimentos | Existente |
| Cenário 001 — Falhas de autenticação | Implementado e testado com dados sintéticos |
| Evidências do cenário 001 | Existentes |
| Cenário 002 — Integridade de arquivos | Implementado |
| Baseline SHA-256 e relatório do cenário 002 | Existentes |
| Evidências do cenário 002 | Existentes |
| Cenário 003 — Atividade suspeita | Relatório existente; implementação pendente |
| Preparação da infraestrutura de virtualização | Concluída |
| Instalação e validação do Wazuh | Pendente |
| Coleta e análise centralizada de logs por SIEM | Pendente |
| Integração dos scripts com o Wazuh | Pendente |
| Correlação com MITRE ATT&CK | Não documentada como funcionalidade implementada |
| Coleta de logs reais de endpoints | Pendente de implementação e validação |
| Relatórios e evidências dos próximos cenários | Em desenvolvimento |

## 11. Competências técnicas demonstradas

O estado atual do projeto permite demonstrar prática em:

- Desenvolvimento de scripts de análise com Python.
- Leitura e processamento de dados estruturados.
- Análise de falhas de autenticação.
- Contabilização de eventos por IP e usuário.
- Aplicação de critérios temporais para identificação de padrões.
- Verificação de integridade por hashes SHA-256.
- Organização de investigações e evidências técnicas.
- Documentação de procedimentos e resultados.
- Versionamento de código com Git e GitHub.
- Preparação de infraestrutura Linux para virtualização.

O projeto ainda não demonstra, por si só, experiência operacional com um SIEM em funcionamento, monitoramento contínuo de endpoints ou investigação baseada em telemetria real.

## 12. Próximas etapas

As próximas etapas previstas para a evolução do laboratório são:

1. Instalar e validar o Wazuh no ambiente virtual.
2. Configurar a coleta de eventos e validar sua visualização no SIEM.
3. Integrar a coleta de logs aos procedimentos de análise.
4. Desenvolver e executar a implementação técnica do cenário 003.
5. Ampliar os testes, registrando entradas, resultados e evidências reproduzíveis.
6. Evoluir a documentação conforme cada funcionalidade for implementada e validada.

Essas etapas são objetivos futuros, não funcionalidades já concluídas.

## 13. Considerações finais

O Mini-SOC está em desenvolvimento incremental e já possui implementações práticas de análise de falhas de autenticação e monitoramento de integridade de arquivos.

O foco atual é construir uma base técnica reproduzível, com scripts funcionais, testes documentados e evidências organizadas. A integração com o Wazuh e a ampliação para coleta centralizada de eventos serão os próximos passos para aproximar o laboratório de um fluxo de trabalho típico de um SOC N1.

O projeto tem finalidade educacional e utiliza dados sintéticos e ambientes controlados sempre que aplicável.
