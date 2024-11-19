from dotenv import load_dotenv
from langchain import hub
from langchain_experimental.agents import create_csv_agent
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool

load_dotenv()

def main():
    print("Inicio...")

    instructions = """
                    You are an agent designed to write and execute Python code to answer questions.
                    You have access to a python REPL, which you can use to execute python code.
                    Only use de output of your code to answer the questions.
                    You might know the answer without any code, but you should still run the code to get the answer.
                    If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
                    """

    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instructions)

    tools = [PythonREPLTool()]
    agent = create_react_agent(
        prompt=prompt,
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
        tools=tools,
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    agent_executor.invoke(
        input={
            "input":"""generate and save in current working directory 2 QR codes that point to www.google.com, you have qrcode package installe already"""
        }
    )

if __name__ == "__main__":
    main()