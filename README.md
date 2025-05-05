# Site de Receitas

Um Site que permite o usuário postar as suas receitas preferidas. Após análise dos administradores, a receita é publicada.

## Como utilizar o projeto

### instalação
* Acesse o terminal do seu computador;
* Utilize o comando `cd` para acessar algum diretório da sua máquina (ex: `cd C:\Documents`);
* Clone o projeto. `git clone https://github.com/BrunoPereiradeSouza/Site-de-Receitas.git`;
* Acesse o diretório do projeto. `cd site de receitas`;
* Crie o ambiente virtual. `Python -m venv venv`;
* Ative o ambiente virtual. `.\venv\Scripts\activate`. OBS: Esse comando é para usuários de windows;
* Instale as dependências. `pip install -r requirements.txt`;
* Execute o sistema na sua máquina local. `python .\manage.py runserver`.

## Aprendizado

Através desse projeto, foi possível aprimorar conhecimentos do framework Django, bem como do Desenvolvimento Web.
Dentre eles:
* Herança de templates, partials e outras particularidades do template engine;
* Testes Unitários e de Integração com Pytest e Unittest;
* Testes Funcionais com Selenium;
* Validações de formulários;
* Autenticação de usuários e criação de sistemas de login e logout;
* Filtragem em consultas ao banco de dados;
* Criação de funções(módulos) para reaproveitamento de código.

Este projeto também possibilitou o aprendizado de Django Rest Framework para a criação de APIs REST.
Conceitos aprendidos:
* Function-Based-View com @api_view e Response do Django Rest Framework;
* Mixins, Generic Views e Pagination no Django Rest Framework;
* ViewSets e Routers;
* Autenticação de usuários com JWT Token;
* Permissões no Django Rest Framework;
* Segurança da API no Django Rest Framework; 
