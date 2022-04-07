# Back-end do desafio1

Back-end desenvolvido em python utilizando a biblioteca Flask para fazer API.

Foi utilizado Venv para virtualizar o projeto juntamente com Docker.

Foi utilizado tambem autenticação com Token JWT, onde o token era criado no back-end e armazenado em cookie no front-end. Em cada requisição do usuário, o token é validado e o usuário só consegue navegar para a pagina desejada se estiver logado.

O servidor de back end está hospedado no heroku no seguinte host: https://desafio-backend-and-bd.herokuapp.com/

## Aqui está um vídeo que fiz utilizando o sistema: https://www.youtube.com/watch?v=tvNomTL-hlI

### O servidor back end em alguns momentos está apresentando um erro com o conector do MySQL que infelizmente eu não consegui ajeitar antes do prazo. Este problema é resolvido ao reiniciar o servidor.

O banco de dados utilizado foi o MySQL e o arquivo do banco está na raiz deste repositório com o nome "db.sql".
Para conectar ao banco, é necessário rodar o script em alguma ferramenta de manipulação de SQL e em seguida inserir os dados de conexão no arquivo "./server/server" (ou no arquivo ".ENV" na raiz do projeto), inserindo o host, user, password e database.

É necessário tambem ter um servidor MySQL rodando na porta 3306.

Para criar a imagem do projeto, é necessário rodar o comando "docker build -t desafio1_backend ."
E para criar o container, é necessário rodar o comando "docker run -d -p 5000:5000 desafio1_backend"

As informações sobre o front end estão no repositóri do mesmo.
