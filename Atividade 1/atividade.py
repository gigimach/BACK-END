from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from Backend.modules.utils import formatar_valores, not_found_error_message

app = FastAPI()

'''

origins = ['http://127.0.0.1:5500']
    """_summary_

    Raises:
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''


class Tarefa(BaseModel):
    id: int | None
    descricao: str
    responsavel: str
    nivel: int
    prioridade: int
    situacao: str = 'Nova'


tarefas: list[Tarefa] = []

# adcionar tarefa


@app.post("/tarefa", status_code=status.HTTP_201_CREATED)
def adicionar_tarefa(tarefa: Tarefa):
    niveis = [1, 3, 5, 8]
    prioridades = [1, 2, 3]

    if tarefa.nivel not in niveis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Nível indisponível. Por favor, escolha 1, 3, 5 ou 8')

    if tarefa.prioridade not in prioridades:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" A prioridade está indisponível. Por favor, escolha 1, 2, ou 3")

    tarefa.id = len(tarefas)+1
    tarefas.append(tarefa)

    return 'A tarefa foi adicionada com sucesso'

# remover tarefa


@app.delete("/tarefa/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_tarefa(tarefa_id: int):
    for tarefa_atual in tarefas:
        if tarefa_atual.id == tarefa_id:
            tarefas.remove(tarefa_atual)
            return

    raise HTTPException(404, detail="Desculpe. Tarefa não encontrada")

# listar tarefas


@app.get("/tarefa")
def listar_tarefas():
    return tarefas

# detalhar tarefa - obter somente uma tarefa


@app.get("/tarefa/{tarefa_id}")
def detalhar_tarefa(tarefa_id: int):
    for trf in tarefas:
        if trf.id == tarefa_id:
            return trf

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Desculpe. Tarefa com ID {tarefa_id} não encontrada.')

# Em andamento - in_progress


@app.put("/tarefa/in_progess/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def marcar_em_andamento(tarefa_id: int):
    for trf in tarefas:
        if trf.id == tarefa_id:
            if trf.situacao == "Em andamento":
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f'Tarefa com ID {tarefa_id} já está em andamento.')
            elif trf.situacao == "Nova" or trf.situacao == "Pendente":
                trf.situacao = "Em andamento"
                return
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail='A tarefa não está em situação de nova ou pendente.')

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Tarefa com ID {tarefa_id} não encontrada.')

# Pendente


@app.put('/tarefa/pending/{tarefa_id}', status_code=status.HTTP_204_NO_CONTENT)
def marcar_como_pendente(tarefa_id: int):
    for trf in tarefas:
        if trf.id == tarefa_id:
            if trf.situacao == "Pendente":
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f'A tarefa com ID {tarefa_id} já está pendente.')
            elif trf.situacao == "Nova" or trf.situacao == "Em andamento":
                trf.situacao = 'Pendente'
                return
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="A tarefa não está em situação de nova ou em andamento.")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Tarefa com ID {tarefa_id} não encontrada.')

# Resolvida


@app.put('/tarefa/resolved/{tarefa_id}', status_code=status.HTTP_204_NO_CONTENT)
def marcar_como_pendente(tarefa_id: int):
    for trf in tarefas:
        if trf.id == tarefa_id:
            if trf.situacao == "Resolvida":
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f'A tarefa com ID {tarefa_id} já está resolvida.')
            elif trf.situacao == "Nova" or trf.situacao == "Em andamento":
                trf.situacao = 'Resolvida'
                return
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="A tarefa não está em situação de nova ou em andamento.")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Tarefa com ID {tarefa_id} não encontrada.')

# cancelar tarefa


@app.put('/tarefa/cancelar/{tarefa_id}', status_code=status.HTTP_204_NO_CONTENT)
def cancelar_tarefa(tarefa_id: int):
    for trf in tarefas:
        if trf.id == tarefa_id:
            if trf.situacao == 'Cancelada':
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f'A tarefa com id {tarefa_id} já está cancelada')
            else:
                trf.situacao = "Cancelada"
                return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Tarefa com ID {tarefa_id} não encontrada.')

# filtrar por situação


@app.get('/tarefa/ft-situacao/')
def filtrar_por_situacao(situacao: str, start: int = 0, end: str = len(tarefas)+1):
    tarefas_selecionadas: list[Tarefa] = []
    situacao = situacao.capitalize()
    situacao = situacao.replace("-", " ")

    for trf in tarefas:
        if trf.situacao == situacao:
            tarefas_selecionadas.append(trf)

    if len(tarefas_selecionadas) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Não há tarefas em situação de {situacao}.")
    else:
        return tarefas_selecionadas

# filtrar por prioridade


@app.get('/tarefa/ft-nivel-prioridade/')
def filtrar_por_nivel_prioridade(nivel: int, prioridade: int, start: int = 0, end: int = len(tarefas)+1):
    tarefas_selecionadas: list[Tarefa] = []
    for trf in tarefas:
        if trf.nivel == nivel and trf.prioridade == prioridade:
            tarefas_selecionadas.append(trf)

    if len(tarefas_selecionadas) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Não existe tarefa com nível {nivel} e prioridade {prioridade}.")
    else:
        return tarefas_selecionadas
