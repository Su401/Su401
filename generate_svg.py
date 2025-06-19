import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')

if not GITHUB_TOKEN or not GITHUB_USERNAME:
    raise ValueError("Missing GITHUB_TOKEN or GITHUB_USERNAME in environment variables")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

# GitHub GraphQL query to get user info and stats
QUERY = """
query {
  user(login: "%s") {
    name
    bio
    repositories(privacy: PUBLIC) {
      totalCount
    }
    followers {
      totalCount
    }
    contributionsCollection {
      contributionCalendar {
        totalContributions
      }
    }
  }
}
""" % GITHUB_USERNAME

def fetch_github_data():
    url = "https://api.github.com/graphql"
    response = requests.post(url, json={'query': QUERY}, headers=HEADERS)

    if response.status_code == 401:
        raise Exception("Authentication failed: 401 Bad Credentials. Check your token.")
    elif response.status_code != 200:
        raise Exception(f"Query failed with status code {response.status_code}")

    return response.json()

def generate_svg(data):
    user = data['data']['user']
    name = user['name'] or GITHUB_USERNAME
    bio = user.get('bio', '')
    repos = user['repositories']['totalCount']
    followers = user['followers']['totalCount']
    contributions = user['contributionsCollection']['contributionCalendar']['totalContributions']

    svg_content = f'''
<svg width="400" height="180" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{ font: bold 18px sans-serif; fill: #2c3e50; }}
    .info {{ font: 14px monospace; fill: #34495e; }}
  </style>
  <text x="10" y="30" class="title">GitHub Stats for {name}</text>
  <text x="10" y="60" class="info">Bio: {bio}</text>
  <text x="10" y="90" class="info">Public Repos: {repos}</text>
  <text x="10" y="120" class="info">Followers: {followers}</text>
  <text x="10" y="150" class="info">Contributions this year: {contributions}</text>
</svg>
'''
    with open('github_stats.svg', 'w') as f:
        f.write(svg_content)

def main():
    data = fetch_github_data()
    generate_svg(data)
    print("SVG generated successfully.")

if __name__ == "__main__":
    main()
