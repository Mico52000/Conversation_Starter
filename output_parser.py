from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List


class PersonIntel(BaseModel):
    summary: str = Field(description="Summary of the person")
    facts: List[str] = Field(description="Interesting facts about the person")
    topics_of_interest: List[str] = Field(description="Topics that interset the person")
    conversation_starters: List[str] = Field(
        description="Create ince breakers to start a conversation with someone"
    )

    def to_dict(self):
        return {
            "summary": self.summary,
            "facts": self.facts,
            "topics_of_interest": self.topics_of_interest,
            "conversation_starters": self.conversation_starters,
        }


person_intel_parser = PydanticOutputParser(pydantic_object=PersonIntel)
