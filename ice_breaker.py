from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parser import PersonIntel, person_intel_parser

##import tuple from typing so we can type annotate the return value for icebreak
from typing import Tuple

### adding things in curly brackets allows us to inject information in prompt templates


def ice_break(name: str) -> Tuple[PersonIntel, str]:
    linkedin_url = linkedin_lookup_agent(name)
    print(linkedin_url)
    summary_template = """
             given the Linkedin information {linkedin_information}  about a person from I want you to create:
             1. a short summary
             2. two interesting facts about them
             3. A topic that may interest them
             4. 2 creative Ice breakers to open a conversation with them 
             \n{format_instructions}
         """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information"],
        template=summary_template,
        ### since our output parser is ready before running the chain, we can give it to the prompt template now
        ### this is done by defining the partial variables
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    # notice how input_variables in the prompt template become an input name in chain.run()
    linkedin_data = scrape_linkedin_profile(linkedin_url)
    res = chain.run(linkedin_information=linkedin_data)
    ### notice how the rsult is still a string but it is formatted exactly like the output parser we defined
    ### in output parser.py

    return person_intel_parser.parse(res), linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    ice_break("Michael Zakhary")
