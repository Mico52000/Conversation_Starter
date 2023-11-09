from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent

### adding things in curly brackets allows us to inject information in prompt templates


def ice_break(name: str) -> str:
    linkedin_url = linkedin_lookup_agent("Renee Zakhary")
    print(linkedin_url)
    summary_template = """
    Given the information {information} about a person, I want you to create:
    1. A medium length summary
    2. two interesting facts about them
    """


    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )


    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")


    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    # notice how input_variables in the prompt template become an input name in chain.run()
    res = chain.run(information=scrape_linkedin_profile(linkedin_url))
    print(res)
    return res