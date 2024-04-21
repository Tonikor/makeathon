import os
import pandas as pd

os.environ["OPENAI_API_KEY"] = "sk-proj-lwTL4y7sL9TBd9yAShrKT3BlbkFJMqsPT0v7tSrESwHTmLrJ"

df = pd.read_csv("flight_taxi.csv")
print(df.shape)

from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine

engine = create_engine("sqlite:///flight_taxi.db")

df.to_sql("flight_taxi", engine, index=False)

db = SQLDatabase(engine=engine)

from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

agent_executor.invoke({"input": "know that all the data represents a single day."
                                "what is the average number of taxis that arrived on flights that had arrival delay?"})

agent_executor.invoke({"input": "at what hour of the day did most planes arrive?"})

agent_executor.invoke({"input": """using the data of the join table, provide me with a
strategy in order to maximise usage of taxis"""})
