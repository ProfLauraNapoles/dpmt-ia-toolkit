# Registro de testes — Land

Data: **13/11/2026**. Aplicação local no macOS, Python 3.12, Streamlit 1.67.0. Dados fictícios. Nenhuma chamada real de IA ou uso de credenciais reais nesta validação.

## Testes automatizados

Comando executado:

```sh
python -m unittest -v test_land test_app
```

**Resultado: 15 testes aprovados** (11 de regras/integração simulada e quatro da interface simulada). A compilação dos módulos também passou.

Cobertura relevante:

- Campos vazios, limites, IDs duplicados e fontes inválidas são rejeitados.
- Edições aparecem no modo sem IA, que não chama modelo.
- Fontes desconhecidas/repetidas, cobertura incompleta, citações inventadas, hipóteses com referências inválidas e ausência de limites são rejeitadas.
- O teste registra expressamente que uma interpretação errada com citação literal pode passar: revisão humana continua necessária.
- Transporte simulado verifica endereço fixo, autenticação fora do prompt, JSON Schema, `store: false`, timeout e uma chamada por clique.
- Respostas incompletas, recusas, formato inválido, conteúdo excessivo, falhas de rede e erros HTTP 400/401/403/429/500 geram mensagens compreensíveis sem expor a credencial fictícia.
- A interface exige campos e opção de envio para habilitar IA. O modelo só é chamado ao clicar. Nova entrada, troca de modo e falha retiram o resultado anterior.
- Inclusão/remoção de fonte e restauração do exemplo foram verificadas.

O AppTest pode emitir o aviso “missing ScriptRunContext” no processo de teste; os testes passaram sem exceção da aplicação. Isso não é evidência de uma chamada externa.

## Verificação no navegador

Chrome no macOS: abertura local, execução sem IA, três fontes na tabela, leitura integral das citações, preenchimento da revisão e download JSON conferidos. O arquivo baixado preservou as três fontes e a anotação de revisão. A marcação da revisão foi conferida na interface e no arquivo. Também confirmadas a retirada do resultado após editar a pergunta, a restauração do exemplo e a desabilitação da chamada de IA sem configuração.

## Pendências antes da gravação com IA

- Executar com chave e modelo disponíveis na conta escolhida, verificar custo/acesso e observar a resposta real.
- Conferir a pertinência das afirmações e a utilidade das hipóteses geradas pelo modelo escolhido.
- Ensaiar os nove minutos da demonstração e a alternativa sem IA.

Não validados: instalação em Windows/Linux, celulares, ambiente multiusuário, hospedagem pública, carga ou acessibilidade integral. O projeto é um exemplo didático local, não um serviço publicado.
