"""Prepara o exemplo de Land. Não chama IA nem acessa a rede."""
import json
from pathlib import Path
from land_core import DEFAULT_QUESTION, build_prompt


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
    return build_prompt(DEFAULT_QUESTION, cartoes)


if __name__ == "__main__":
    arquivo = Path(__file__).resolve().parent / "dados-land.json"
    cartoes = json.loads(arquivo.read_text(encoding="utf-8"))
    print(montar_prompt(cartoes))
