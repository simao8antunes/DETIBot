# detiBot

[Website](https://detibot.pages.dev)

## Tecnologias Utilizadas

- **Storing**: MySQL, Qdrant
- **Web Scraping**: Selenium, BeautifulSoup
- **RAG**: LangChain
- **LLM**: Ollama llama3
- **FrontEnd**: React
- **Deployment**: Docker

## Comandos para Executar a Aplicação

### Executar a Aplicação Completa

```sh
docker-compose up --build
```

### Executar Backend

```sh
docker-compose up --build
docker-compose up update api
```
ou se preferires correr localmente
```sh
docker-compose up --build
uvicorn controller:app --reload
```