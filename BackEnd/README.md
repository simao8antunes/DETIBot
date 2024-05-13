para colocar o backend a funcionar é necessário:

1- docker-compose up qdrant mysql ollama

2- verificar se os 3 containers em cima estão prontos para o funcionamento:

    -> qdrant: verificar apenas se está a rodar no docker ou então fazer localhost:6333/dashboard

    -> mysql: 

    -> ollama: dps de verificar q o container está a rodar fazer na linha de comandos:
        -> docker exec -it ollama ollama run llama2/(outro llm suportado pelo ollama)

3- apôs os passos acima estarem compridos e verificados rodar o backend: 
    
    -> local: uvicorn controller:app --reload 
    -> docker: 
        full app: docker-compose up update api


