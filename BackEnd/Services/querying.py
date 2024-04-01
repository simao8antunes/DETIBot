#This class contains all the functions and calls to the other classes
#To execute the neccessary methods to return an answer to the caller
#Of 'answer_question' method.

class Query: 

    def answer_question(arg,prompt:str):
        return {"Answer": prompt}
        