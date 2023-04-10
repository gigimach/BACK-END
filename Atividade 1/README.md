# atividade_01_BackEnd
01 - Tasks - Minha Primeira API - Python/FastAPI
Atributos: Descrição, Responsável, Nivel [1, 3, 5, 8], Prioridade[1, 2, 3], Situação ["NOVA", "EM ANDAMENTO", "PENDENTE", "RESOLVIDA", "CANCELADO"]

Features:
a) Adicionar, Remover, Listar, Detalhes (Obter um)
b) Marcar como EM ANDAMENTO
c) Marcar como PENDENTE
d) Marcar como RESOLVIDA
e) Cancelar Tarefa (Marcar com CANCELADA)
f) Listar Filtrado por Situação (usar Query Param)
g) Listar Filtrado por Nível e Prioridade (usar Query Param)

Diagrama de Estados:
1) NOVA --> Ao criar Tarefa
2) EM ANDAMENTO vem de NOVA ou de PENDENTE
3) PENDENTE vem de NOVA ou de EM ANDAMENTO
4) CANCELADA por vir de qualquer Situação
5) RESOLVIDA vem de EM ANDAMENTO
