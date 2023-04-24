import os
import random
from config import settings
os.environ['OPENAI_API_KEY'] = settings['OPENAI_API_KEY']
from langchain.llms import OpenAI
from langchain import PromptTemplate

class EducationExpert:
    def __init__(self, temperature=0.7):
        self.llm = OpenAI(temperature=temperature)
        self.template1 = """ You are an expert in education and are execellent at teaching. You are also a good writer and have written many books.
Additionally,  you teach kids about grammer. 

You are an English teacher that is teaching about English Grammer and writing. Write muliple choice grammar question for a {grade} grade student on the topic of {topic}. It must be a multiple choice question with 5 choices.

Only ask the question. Do not give the answer. 

A random number to help you not generate the same question each time is {random_number}.

Your question is:"""
        self.template2 = """ You are an expert in education and are execellent at teaching. You are also a good writer and have written many books. 
Additionally, you teach kids about grammer.

Another teacher wrote this question {question}. 

Your job is to generate the correct answer to the question. It should be a single word or number. If it is a multiple choice question, then you should ONLY give the letter of the correct answer. The answer must be machine gradeable.

The correct answer is:"""
        self.prompt1 = PromptTemplate(template=self.template1, input_variables=["grade", 'topic', 'random_number'])
        self.prompt2 = PromptTemplate(template=self.template2, input_variables=["question"])
        self.question = None
        self.answer = None
    
    def generate_question(self, grade, topic):
        prompt = self.prompt1.format(grade=grade, topic=topic, random_number=random.randint(1, 1000000))
        self.question = self.llm(prompt)
        # print(self.question)
    
    def generate_answer(self):
        prompt = self.prompt2.format(question=self.question)
        self.answer = self.llm(prompt)
        # strip out single and double quotes, then strip out any leading or trailing spaces
        self.answer = self.answer.replace("'", "").replace('"', "").strip()
        # also remove ) and .
        self.answer = self.answer.replace(")", "").replace(".", "")
        # try splitting on spaces, if there are more than 1, then it is a multiple choice question
        answer_parts = self.answer.split(" ")
        if len(answer_parts) > 1:
            # it is a multiple choice question
            # get the first letter of the answer
            self.answer = answer_parts[0]
        # print("---------")
        # print("Answer:", self.answer)
        
    def make_QA(self, grade, topic):
        self.generate_question(grade, topic)
        self.generate_answer()
        return self.question, self.answer

if __name__ == "__main__":
    ee = EducationExpert()
    print(ee.make_QA(grade="5th", topic="animals"))
    