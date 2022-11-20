# gerenciamento-cpd-api
API de um Gerenciador de CPD proposto pela faculdade UCL no semestre 02/2022

#### URI e JSON Body de cada rota

* GET
    * URI - /api/temperatura-umidade
    * *Não possui JSON para envio.*
    * retorno
        ```json
        {
            "temperatura": 27,
            "umidade": 95
        }
        ```

<hr>

* GET
    * URI - /api/leitor-rfid/{usuarioId}
    * *Não possui JSON para envio.*
    * retorno
        ```json
        {
            "permitido": true
        }
        ```

<hr>

* POST
    * URI - /api/cadastro/leitor-rfid
        ```json
        {
            "usuarioId": 1
        }
        ```
    * retorno
        ```json
        {
            "cadastro": true,
            "erro": null
        }
        ```

<hr>

* GET
    * URI - /api/sensor-infravermelho
    * *Não possui JSON para envio.*
    * retorno
        ```json
        {
            "encontrado_item": true
        }
        ```
<hr>

* GET
    * URI - /api/sensor-gas
    * *Não possui JSON para envio.*
    * retorno
        ```json
        {
            "valor": 37
        }
        ```
<hr>

* GET
    * URI - /api/sensor-voltagem
    * *Não possui JSON para envio.*
    * retorno
        ```json
        {
            "valor": 0
        }
        ```
<hr>

* GET
    * URI - /api/sensor-amperagem
    * *Não possui JSON para envio.*
    * retorno
        ```json
        {
            "valor": 0.0
        }
        ```
<hr>

* POST
    * URI - /api/login
        ```json
        {
            "login": "gustavosfrts",
            "senha": "111222"
        }
        ```
    * retorno
        ```json
        {
            "email": "gustavosf@ucl.br",
            "erro": null,
            "id": 1,
            "nome": "Gustavo Freitas",
            "sucesso": true
        }
        ```
<hr>

* POST
    * URI - /api/criar-usuario
        ```json
        {
            "nome": "Gustavo Freitas",
            "email": "gustavosf@ucl.br",
            "login": "gustavosfrts",
            "senha": "111222"
        }
        ```
    * retorno
        ```json
        {
            "erro": null,
            "sucesso": true
        }
        ```
<hr>