import os
from langchain import PromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackManager
from langchain.chat_models import ChatOpenAI

from langchain.agents import initialize_agent, Tool, AgentType
from langchain.llms.gpt4all import GPT4All

from tools.tools import get_profile_url


def lookup(name: str) -> str:
    #llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    current_path = os.getcwd()
    gpt4all_path = os.path.join(current_path, "llm_models", "nous-hermes-llama2-13b.Q4_0.gguf")
    callback_manager = BaseCallbackManager([StreamingStdOutCallbackHandler()])
    llm = GPT4All(model=gpt4all_path, callback_manager=callback_manager, verbose=True, repeat_last_n=0)
    template = """given the full name {name_of_person} I want you to get it me a link to their Linkedin profile page.
                          Your answer should contain only a URL"""

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url,
            description="useful for when you need get the Linkedin Page URL",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    linked_profile_url = agent.run(prompt_template.format_prompt(name_of_person=name))
    return linked_profile_url
