import requests
import os
from dotenv import load_dotenv


def scrape_linkedin_profile(linked_in_profile):
    """
    scrape information from linkedin profile
    manually scrape the information from a linkedin profile
    :param linked_in_profile:
    :return: a pythong dictionary that contains information pulled from that person's linkedin profile
    """
    load_dotenv()

    # Get the API key from the environment
    api_key = os.getenv("PROXYCURL_API_KEY")

    # Check if the API key is set
    if api_key is None:
        raise ValueError("API_KEY is not set in the .env file")

    headers = {"Authorization": "Bearer " + api_key}
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    params = {"url": linked_in_profile}
    ##### we will avoid repeating this request to proxycurl since we are so limited in our free requests
    # response = requests.get(api_endpoint,
    #                         params=params,
    #                         headers=headers)
    # return a hard coded profile from gist for me
    response = requests.get(
        "https://gist.githubusercontent.com/Mico52000/7de88c16aec904b08750866075b89960/raw/f26936a0234116a1e705b4042794c879a1e24ddf/la.json"
    )
    data = response.json()
    ## dictionary comprehension to filter for the keys and values we want
    data = {
        k: v
        for k, v in data.items()
        if v not in ["", [], "", None]
        and k not in ["certifications", "people_also_viewed"]
    }
    ## if data includes infomration about groups, remove the group picture url
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_picture_url")

    return data
