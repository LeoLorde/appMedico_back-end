# AppMed #

A parte **backend** do aplicativo **AppMed**, focado em facilitar o agendamento de consultas com diversos tipos de profissionais da saúde.

## Rotas ##

### `POST /client/create` ###

Cria um novo cliente no sistema.

**URL:**  
`/client/create`

**Método:**  
`POST`

---

Body (JSON) — formato válido:

```json
{
 "username": "nome",
 "senha": "senha",
 "dataDeNascimento": "2002-02-02",
 "genero": "MAN",
 "cpf": "98296907841",
 "email": "erda"
}
```

Body (JSON) - Resposta:

```json
{
  "message": "Client criado com sucesso",
  "data": {
            "id": 0,
            "username": "nome",
            "email": "erda",
            "cpf": "98296907841", 
            "dataDeNascimento": "2002-02-02",
            "genero": "MAN"
        }
}
```
