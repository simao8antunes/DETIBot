Neste momento só temos o update.py e o controller.py a funcionar.
Em que apenas teem a capacidade de adicionar ou alterar valores na base de dados mysql
chamam o loader, (o inicio da pipeline do rag)
no entanto o loader e as classes necessarias para o RAG, q são chamadas por este ainda n estão a funcionar.

para exprimentar o q está feito:

cd BackEnd

pip install -r requirements.txt

docker-compose up mysql -> iniciliza a bd num docker local.
e só dps de ter a mysql DB a rodar é só fazer:

1- uvicorn controller:app --reload
2- python3 update.py