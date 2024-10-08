﻿Projeto CarLead

Este projeto tem como objetivo criar uma aplicação Django que conecta a API da Tabela FIPE para consultas de veículos, bem como outras funcionalidades relacionadas a dados veiculares, com a finalidade de capturar leads de pessoas interessadas em vender seu veículo.

## Requisitos

0. Antes de tudo, você precisará ter os seguintes itens instalados no seu sistema:

 - Python 3.8+
 - Docker
 - Git

## Configuração usando Docker

1. Clone o repositório e navegue até a pasta do projeto:

    ```bash
    git clone https://github.com/estevaonrs/carleadv2.git
    cd carleadv2

2. Construa a imagem do Docker:

    ```bash
    docker-compose build

3. Execute a aplicação:

    ```bash
    docker-compose up

4. Acesse a aplicação:

    ```bash
        http://localhost:8000

5. Criar superusuário (opcional):

    ```bash
        docker-compose run web python manage.py createsuperuser



## Configuração sem Docker (usando venv)

1. Clone o repositório e navegue até a pasta do projeto:

    ```bash
    git clone https://github.com/estevaonrs/carleadv2.git
    cd carleadv2

2. Crie o ambiente virtual:

    ```bash
    python3 -m venv venv

3. Ative o ambiente virtual:
    - No Linux/MacOS:
        source venv/bin/activate
    
    - No Windows:
        venv\Scripts\activate

4. Instale as dependências:

    ```bash
        pip install -r requirements.txt

5. Execute as migrações:

    ```bash
        python manage.py migrate

6. Inicie o servidor:

    ```bash
        python manage.py runserver

7. Acesse a aplicação:

    ```bash
        Abra o navegador e vá para http://localhost:8000

8. Criar superusuário (opcional)::

    ```bash
        python manage.py createsuperuser

