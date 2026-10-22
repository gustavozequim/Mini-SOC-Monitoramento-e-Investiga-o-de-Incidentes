# Investigação 001 — Falhas de autenticação

## 1. Identificação

- **Projeto:** Mini-SOC — Monitoramento e Investigação de Incidentes
- **Caso:** 001 — Falhas de autenticação
- **Categoria:** Monitoramento de eventos e análise de autenticação
- **Severidade inicial:** Média — classificação didática, sujeita a revisão
- **Status:** Investigação inicial documentada
- **Ambiente:** Laboratório local controlado
- **Fonte:** Dataset sintético em `eventos_auth.jsonl`

## 2. Objetivo

Identificar padrões de falhas repetidas de autenticação por endereço IP
e por usuário, utilizando um script Python para analisar eventos JSONL
e gerar alertas com base em um limiar configurável dentro de uma janela
temporal.

## 3. Escopo e limitações

A análise foi realizada exclusivamente sobre eventos sintéticos criados
para este laboratório. Nenhum sistema de produção foi acessado.

O dataset contém 10 eventos de autenticação, incluindo falhas e
autenticações bem-sucedidas. Os endereços IP e nomes de usuário são
fictícios.

A investigação não comprova atividade maliciosa nem comprometimento
de uma conta.

## 4. Metodologia

Foi utilizado o script `scripts/analisar_alertas.py`, com os seguintes
critérios:

- Leitura dos eventos em formato JSON Lines (JSONL).
- Validação da estrutura JSON, dos campos obrigatórios, dos tipos de
  evento e dos timestamps.
- Contagem de falhas por endereço IP e por usuário.
- Detecção por janela temporal deslizante.
- Limiar padrão de 5 falhas dentro de uma janela de 5 minutos.
- Teste adicional com janela de 1 minuto.

Foram executados testes de compilação, execução padrão, rejeição de
parâmetro inválido e validação da janela temporal.

## 5. Evidências e resultados

### 5.1 Integridade dos dados analisados

- Eventos válidos: 10
- Registros inválidos: 0

### 5.2 Falhas por endereço IP

| Endereço IP | Total de falhas |
|---|---:|
| 192.0.2.10 | 5 |
| 192.0.2.20 | 2 |
| 192.0.2.30 | 1 |

### 5.3 Falhas por usuário

| Usuário | Total de falhas |
|---|---:|
| ana | 5 |
| bruno | 2 |
| carla | 1 |

### 5.4 Alertas gerados

Com o limiar de 5 falhas em 5 minutos, foram gerados dois alertas:

**Alerta 1 — Múltiplas falhas por IP**
- Alvo: `192.0.2.10`
- Falhas na janela: 5
- Primeiro evento: `2026-10-21T09:00:00Z`
- Último evento: `2026-10-21T09:00:48Z`

**Alerta 2 — Múltiplas falhas por usuário**
- Alvo: `ana`
- Falhas na janela: 5
- Primeiro evento: `2026-10-21T09:00:00Z`
- Último evento: `2026-10-21T09:00:48Z`

Os dois alertas correspondem ao mesmo conjunto de eventos, analisado
sob duas perspectivas diferentes: origem e conta.

### 5.5 Teste de janela temporal

Foi criado um dataset temporário com cinco falhas distribuídas entre
09:00 e 09:04, para o mesmo usuário e endereço IP.

Com o limiar de 5 falhas em 1 minuto, nenhum alerta foi gerado.
O resultado confirma que, nesse cenário, o total de falhas no arquivo
não é suficiente para disparar o alerta: os eventos também precisam
atender ao critério temporal.

### 5.6 Validação de parâmetros

A execução com `--janela-minutos 0` foi rejeitada pelo programa,
que informou que o valor deve ser maior ou igual a 1.

## 6. Análise técnica

O conjunto de cinco falhas de autenticação em 48 segundos para a
conta `ana`, originadas de `192.0.2.10`, representa um padrão que
merece triagem em um cenário de monitoramento.

Esse comportamento pode ser compatível com tentativa de força bruta,
erro repetido de credenciais ou outra atividade legítima. Os dados
disponíveis não permitem determinar a causa.

O dataset também contém um evento de autenticação bem-sucedida para
a conta `ana`, proveniente do mesmo endereço IP, às 09:01:00Z.
A proximidade temporal justifica verificar se o acesso foi legítimo.
Esse evento, isoladamente, não comprova que as falhas anteriores
resultaram em comprometimento.

## 7. Recomendações de investigação

Em um ambiente real autorizado, as próximas ações seriam:

1. Correlacionar as falhas e o sucesso com os logs completos de
   autenticação e os identificadores de sessão disponíveis.
2. Verificar se a origem e o horário são compatíveis com o padrão
   legítimo de acesso da conta.
3. Investigar outros eventos associados ao usuário, endereço IP e
   dispositivo.
4. Verificar se existem tentativas semelhantes contra outras contas.
5. Aplicar os procedimentos de escalonamento e resposta definidos
   pela organização, caso sejam encontrados indicadores adicionais.

Nenhuma ação de bloqueio ou contenção foi executada neste laboratório.

## 8. Limitações

- Dataset pequeno e inteiramente sintético.
- Ausência de logs de sistema, endpoint, firewall, DNS ou proxy.
- Ausência de contexto sobre localização, dispositivo e histórico
  legítimo de acesso.
- A regra implementada emite no máximo um alerta por alvo em cada
  execução, nesta versão do script.
- Os limiares utilizados são didáticos e não foram calibrados com
  dados reais.
- Os resultados não representam validação de uma plataforma SIEM
  de produção.

## 9. Conclusão

O analisador identificou o padrão sintético de cinco falhas de
autenticação em 48 segundos e gerou alertas por endereço IP e por
usuário. Os testes também demonstraram a rejeição de parâmetros
inválidos e o funcionamento esperado da janela temporal no cenário
validado.

O caso demonstra uma implementação inicial de coleta de eventos
estruturados, validação de dados, detecção baseada em regras e
documentação de uma investigação.

**Resultado:** investigação sintética concluída no escopo dos testes
realizados. Não há evidência suficiente para afirmar comprometimento
de conta ou atividade maliciosa confirmada.
