# Rotas #

Todas as rotas documentadas aqui

## Rotas do Client ##

- POST /client/create
- POST /client/login
- GET /client/<int:limit>
- GET /client/id/<int:id>
- GET /client/username/<str:username>/<int:limit>
- PUT /client/update/<int:id> (JWT REQUIRED)
- DELETE /client/delete/<int:id> (JWT REQUIRED)
