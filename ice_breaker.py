from langchain.prompts.prompt import PromptTemplate

# from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
# from langchain_community.llms import LlamaCpp
# from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain


from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent


def ice_break_with(name: str) -> str:
    """
    Generate an ice breaker summary for a person based on their LinkedIn profile.

    This function performs the following steps:
    1. Looks up the LinkedIn username for the given name.
    2. Scrapes the LinkedIn profile data (currently using mock data).
    3. Generates a summary and interesting facts using a language model.

    Args:
        name (str): The name of the person to generate an ice breaker for.

    Returns:
        str: A string containing a summary and interesting facts about the person.
    """
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=True)

    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOllama(model="mistral")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    res = chain.invoke(input={"information": linkedin_data})

    print(res)

if __name__ == "__main__":
    """
    Main entry point of the script.

    This block demonstrates the usage of the ice_break_with function
    by generating an ice breaker for a sample name.
    """
    print("hello Langchain!")

    print("Ice Breaker Enter")
    ice_break_with(name="Eden Marco")
