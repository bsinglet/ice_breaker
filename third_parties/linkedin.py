import yaml
import requests

def load_keys(filename: str = "keys.yaml") -> dict:
    keys = None
    with open(filename, 'r') as my_file:
        try:
            keys = yaml.safe_load(my_file)
            print(keys.keys())
        except yaml.YAMLError as exc:
            print(exc)
    return keys


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """Scrape information from a LinkedIn profile.
    """
    my_keys = load_keys()
    # use our gist if mock is true, so we avoid burning any ProxyCurl credits
    if mock:
        linkedin_profile_url='https://gist.githubusercontent.com/bsinglet/8e5fd3d4ec1b996a698d4de102f908d5/raw/bb7515ecb3eef002244ee874775ab8243322fd02/eden-marco.json'
        response = requests.get(url=linkedin_profile_url, timeout=10)
    else:
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        header = {
            "Authorization": f'Bearer {my_keys["PROXY_URL_KEY"]}'
        }
        response = requests.get(url=api_endpoint, params={"url": linkedin_profile_url},
                               headers=header,
                               timeout=10)
    data = response.json()
    # clean up the data to remove unwanted fields that would waste tokens
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
    scrape_linkedin_profile(linkedin_profile_url='https://www.linkedin.com/in/eden-marco/', mock=True)
