# 🎮 Lista de Personagens do sériado Rick and Morty

Projeto Django para recebimento de dados dos **Personagens e Episodios**, templates Django e integração com a **A API Rick and Morty**.

---

## 📌 Funcionalidades

* CRUD completo de **Personagens** e **Episodios**.
* Consumo da **API externa de Rick and Morty**.
* Banco de dados **PostgreSQL**.
* Página em **Django Template** para listagem de **Personagens e Episodios**.

---

## ⚙️ Tecnologias

* [Api Usada](https://rickandmortyapi.com/)
* [Django](https://www.djangoproject.com/)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [Requests](https://docs.python-requests.org/)

---

## 🚀 Instalação

### 🔹 1. Clone o repositório

```bash
git clone https://github.com/ClaytonAugust/wsBackend-Fabrica25.2.git
cd wsBackend-Fabrica25.2
```

### 🔹 2. Criar nosso ambiente virutal Isolado: venv
Abra o terminal da pasta e execute esse comando:
```bash
py -m venv venv
```
Depois digita esse comando:
```bash
.\venv\Scripts\activate
```
Após ser ativado, checar se aparece um venv verde no terminal
## 🛠️Agora Baixar todos os requisitos
Digite o comando:
```bash
pip install -r requirements.txt
```
---
## ✅Após baixar tudo, Por essas configurações do POSTGRESQL
```bash
    Nome do banco: rickmortydb       
    nome do usuario: rickmortyuser
    PASSWORD: senhasecreta
```
## 🖼️ Páginas dos Template

Para personagens Acesse:

```bash
http://127.0.0.1:8000/personagens/
http://127.0.0.1:8000/personagens/novo/
http://127.0.0.1:8000/personagens/editar/{api_id}/
http://127.0.0.1:8000/personagens/deletar/{api_id}/
```
Para Episodios Acesse:
```bash
http://127.0.0.1:8000/episodios/

```
---