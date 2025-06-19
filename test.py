import os
from dotenv import load_dotenv

load_dotenv()  # loads .env variables

print("Token loaded:", os.getenv('GITHUB_TOKEN'))
print("Username loaded:", os.getenv('GITHUB_USERNAME'))