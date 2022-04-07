# Back-end do desafio1

Back-end desenvolvido em python utilizando a biblioteca Flask para fazer API.

Foi utilizado Venv para virtualizar o projeto juntamente com Docker.

O servidor de back end está hospedado no heroku no seguinte host: https://desafio-backend-and-bd.herokuapp.com/

O servidor de hospedagem está instável e apresentando um erro atípico de conexão com o banco de dados algumas vezes.

O banco de dados utilizado foi o MySQL e o arquivo do banco está na raiz deste repositório com o nome "db.sql".
Para conectar ao banco, é necessário rodar o script em alguma ferramenta de manipulação de SQL e em seguida inserir os dados de conexão no arquivo "./server/server" (ou no arquivo ".ENV" na raiz do projeto), inserindo o host, user, password e database.

É necessário tambem ter um servidor MySQL rodando na porta 3306.

Para criar a imagem do projeto, é necessário rodar o comando "docker build -t desafio1_backend ."
E para criar o container, é necessário rodar o comando "docker run -d -p 5000:5000 desafio1_backend"

As informações sobre o front end estão no repositóri do mesmo.