"""Prepara o exemplo de Land. Não chama IA nem acessa a rede."""
import json
from pathlib import Path


def montar_prompt(cartoes):
    """Valida os cartões e junta instruções com as fontes fictícias."""
    if not isinstance(cartoes, list) or not cartoes:
        raise ValueError("Forneça uma lista não vazia de cartões.")
    ids = set()
    for cartao in cartoes:
        if not isinstance(cartao, dict):
            raise ValueError("Cada cartão deve ser um objeto.")
        for campo in ("id", "fornecedor", "trecho"):
            if not isinstance(cartao.get(campo), str) or not cartao[campo].strip():
                raise ValueError(f"Campo obrigatório ausente: {campo}")
        if cartao["id"] in ids:
            raise ValueError("Os identificadores das fontes devem ser únicos.")
        ids.add(cartao["id"])
    instrucao = (
        "Compare somente os cartões fictícios abaixo.\n"
        "Entregue: fornecedor | capacidade mencionada | ID da fonte | informação ausente.\n"
        "Separe duas hipóteses para investigação.\n"
        "Não converta ausência de menção em ausência de funcionalidade.\n"
        "Não invente preços, clientes ou indicadores.\n\nDADOS FICTÍCIOS\n"
    )
    return instrucao + json.dumps(cartoes, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    arquivo = Path(__file__).resolve().parent / "dados-land.json"
    cartoes = json.loads(arquivo.read_text(encoding="utf-8"))
    print(montar_prompt(cartoes))
