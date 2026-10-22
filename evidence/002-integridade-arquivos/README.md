# Evidências — Investigação 002

Este diretório contém os resultados registrados durante os testes do
monitor de integridade `scripts/monitorar_integridade.py`.

## Arquivos

- `resultado-sem-alteracao.txt`: teste de controle com os três arquivos
  correspondendo à linha de base.
- `resultado-modificado.txt`: detecção da alteração em `servico.txt`.
- `resultado-novo.txt`: detecção de `novo_arquivo.txt` como novo.
- `resultado-removido.txt`: detecção da remoção de `politica_acesso.txt`.

## Interpretação dos códigos de saída

- `0`: nenhuma divergência detectada.
- `1`: uma ou mais divergências detectadas.
- `2`: erro operacional ou linha de base inválida.

Nos cenários de adição e remoção, `servico.txt` também estava modificado.
Os resultados refletem o estado dos arquivos no momento de cada execução.

Os arquivos desta evidência são saídas de um laboratório sintético, não
registros de um incidente real.
