para colocar o backend a funcionar é necessário:

1- docker-compose up qdrant mysql ollama

2- verificar se os 3 containers em cima estão prontos para o funcionamento:

    -> qdrant: verificar apenas se está a rodar no docker ou então fazer localhost:6333/dashboard

    -> mysql: 

    -> ollama: para além de blah blah blah ou depois de blah blah blah fazer o seguinte:

        -> docker desktop: ir ao container ollama entrar no tab Exec e escrever o seguinte comando: ollama run llama2/(llm escolhido suportado pelo ollama)
        -> command line: ns se dá tenho de ver 

3- apôs os passos acima estarem compridos e verificados rodar o backend: 
    
    -> local: uvicorn controller:app --reload 
    -> docker: 
        full app: docker-compose up update api


