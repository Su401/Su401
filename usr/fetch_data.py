import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

if not GITHUB_TOKEN or not GITHUB_USERNAME:
    raise ValueError("Missing GITHUB_TOKEN or GITHUB_USERNAME in environment variables")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

QUERY = """
query($login: String!) {
  user(login: $login) {
    login
    name
    bio
    followers {
      totalCount
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
      }
    }
    repositories(first: 100, isFork: false, orderBy: {field: STARGAZERS, direction: DESC}) {
      totalCount
      nodes {
        name
        languages(first: 50) {
          edges {
            size
            node {
              name
            }
          }
        }
      }
    }
  }
}
"""

def fetch_github_data():
    url = "https://api.github.com/graphql"
    variables = {"login": GITHUB_USERNAME}

    response = requests.post(
        url,
        json={"query": QUERY, "variables": variables},
        headers=HEADERS
    )

    if response.status_code == 401:
        raise Exception("Authentication failed: 401 Bad Credentials. Check your token.")
    elif response.status_code != 200:
        raise Exception(f"Query failed with status code {response.status_code}")

    data = response.json()["data"]["user"]

    # Compute language totals
    language_sizes = {}
    for repo in data["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            lang = edge["node"]["name"]
            size = edge["size"]
            language_sizes[lang] = language_sizes.get(lang, 0) + size

    total_size = sum(language_sizes.values())
    language_percentages = {
        lang: f"{(size / total_size) * 100:.2f}"
        for lang, size in language_sizes.items()
    } if total_size > 0 else {}

    stats = {
        "username": data["login"],
        "name": data.get("name"),
        "bio": data.get("bio"),
        "followers": data["followers"]["totalCount"],
        "totalContributions": data["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        "repositoryCount": data["repositories"]["totalCount"],
        "languagePercentages": language_percentages,
    }

    return stats, GITHUB_USERNAME
