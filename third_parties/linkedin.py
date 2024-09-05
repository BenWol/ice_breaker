import os
import requests


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = True):
    """scrape information from linkedin profiles, manually scrape the information from the linkedin profile"""
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/BenWol/c75584e63906d73291c71f03857a1144/raw/4cbb6b3d573f0038b74ec8c173a9f0698556e948/eden_marco.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/eden-marco/", mock=True
        )
    )
