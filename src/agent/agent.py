import logging

from langchain_core.tools import tool
from langchain_gigachat.chat_models import GigaChat
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent
import time

from src import args


def inicialization() -> CompiledGraph:
    memory = MemorySaver()
    args.model = GigaChat(
        # сюда нужно вставить ключик гигачада
        credentials="",
        scope="GIGACHAT_API_PERS",
        model="GigaChat-Max",
        verify_ssl_certs=False,
        top_p=0.49
    )
    tools = [check_file_info]
    logging.info('Агент стартанул')
    return create_react_agent(args.model,
                              checkpointer=memory,
                              tools=tools,
                            )


def check_file(text, agent, user_id) -> str:
    config = {"configurable": {"thread_id": user_id, "recursion_limit": "100"}}
    resp = agent.invoke({"messages": [("user", text)]}, config=config)
    logging.info(resp)
    time.sleep(1)
    return resp["messages"][-1].content

@tool
def check_file_info():
    """
   сюда идет промт
    """
    # Подсвечивает вызов функции зеленым цветом
    print("\033[92m" + f"Bot requested check_file_info()" + "\033[0m")

