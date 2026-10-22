# Investigação 002 — Monitoramento de Integridade de Arquivos

## 1. Objetivo

Implementar e validar um mecanismo de File Integrity Monitoring (FIM)
utilizando hashes SHA-256 para identificar arquivos adicionados, removidos
ou modificados em um diretório monitorado.

O exercício foi realizado em ambiente local e controlado, com arquivos
sintéticos. Nenhum incidente real foi investigado.

## 2. Escopo

- Diretório monitorado: `investigations/002-integridade-arquivos/amostra/`
- Script: `scripts/monitorar_integridade.py`
- Linha de base: `investigations/002-integridade-arquivos/baseline_sha256.json`
- Algoritmo de hash: SHA-256
- Dependências externas: nenhuma; foi utilizada a biblioteca padrão do Python.

## 3. Metodologia

1. Foram criados três arquivos sintéticos para a amostra.
2. O modo `baseline` calculou o hash SHA-256 de cada arquivo e armazenou
   os resultados em um documento JSON.
3. O modo `verificar` calculou novamente os hashes e comparou o estado atual
   com a linha de base.
4. Foram simulados cenários de alteração, adição e remoção de arquivos.
5. Os resultados de cada execução foram salvos no diretório de evidências.

O SHA-256 produz um resumo criptográfico do conteúdo. Uma alteração no
conteúdo normalmente resulta em um hash diferente, permitindo detectar
divergências em relação à linha de base.

## 4. Resultados

| Cenário | Resultado observado | Código de saída |
|---|---|---:|
| Sem alterações | Nenhuma divergência detectada | 0 |
| Arquivo modificado | `servico.txt` identificado | 1 |
| Arquivo novo | `novo_arquivo.txt` identificado | 1 |
| Arquivo removido | `politica_acesso.txt` identificado | 1 |

Nos testes de adição e remoção, `servico.txt` também foi identificado como
modificado porque a alteração controlada permaneceu presente durante esses
cenários.

O código de saída `0` indica que não foram encontradas divergências. O código
`1` indica que foram detectadas alterações. Erros operacionais ou problemas
com a linha de base retornam código `2`.

## 5. Interpretação

O mecanismo diferenciou corretamente os arquivos que correspondiam à linha
de base daqueles que apresentavam divergências.

Em um ambiente real, uma alteração pode ser legítima, decorrente de
manutenção ou atualização, ou pode exigir investigação. O resultado do FIM,
isoladamente, não comprova comprometimento nem identifica o responsável
pela mudança.

## 6. Limitações

- A linha de base está armazenada no mesmo repositório que a amostra e não
  possui proteção independente contra adulteração.
- Se um agente alterar tanto os arquivos quanto a linha de base, a detecção
  poderá ser comprometida.
- O mecanismo não registra quem alterou um arquivo nem quando a alteração
  ocorreu.
- O monitoramento é executado sob demanda; não há monitoramento contínuo.
- O SHA-256 permite verificar divergências de conteúdo, mas não determina
  se uma mudança é autorizada ou maliciosa.
- O laboratório usa arquivos sintéticos e não representa um ambiente
  corporativo de produção.

## 7. Recomendações defensivas

- Armazenar a linha de base em local com controle de acesso e proteção
  contra alterações não autorizadas.
- Registrar as execuções em um sistema centralizado e protegido.
- Correlacionar alterações com logs de autenticação, processos, mudanças
  administrativas e janelas de manutenção.
- Definir quais arquivos críticos devem ser monitorados e quais mudanças
  são autorizadas.
- Avaliar ferramentas de FIM integradas a uma plataforma de monitoramento,
  como um SIEM, conforme os requisitos do ambiente.

## 8. Reprodução

Na raiz do repositório, com Python 3 instalado:

Criar ou atualizar a linha de base:

    python3 scripts/monitorar_integridade.py baseline

Verificar a integridade:

    python3 scripts/monitorar_integridade.py verificar

Validar a sintaxe do script:

    python3 -m py_compile scripts/monitorar_integridade.py

Atenção: executar `baseline` novamente substitui a referência existente.
Faça isso somente quando desejar estabelecer uma nova linha de base confiável.

## 9. Conclusão

O laboratório demonstrou a utilização de hashes SHA-256 para detectar
divergências de integridade em arquivos, cobrindo os cenários de controle,
modificação, adição e remoção.

A atividade exercitou conceitos de integridade, validação de evidências,
automação com Python e documentação de resultados relevantes para
monitoramento defensivo e operações de SOC.
