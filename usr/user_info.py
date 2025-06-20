from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def calculate_age(birthday_str: str) -> str:
    birth_date = datetime.strptime(birthday_str, "%Y-%m-%d").date()
    today = date.today()
    delta = relativedelta(today, birth_date)
    total_days = (today - birth_date).days
    weeks = (total_days % 30) // 7
    days = (total_days % 30) % 7
    
    parts = []
    if delta.years:
        parts.append(f"{delta.years} year{'s' if delta.years != 1 else ''}")
    if delta.months:
        parts.append(f"{delta.months} month{'s' if delta.months != 1 else ''}")
    if weeks:
        parts.append(f"{weeks} week{'s' if weeks != 1 else ''}")
    if days:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    
    return ", ".join(parts) if parts else "0 days"

def generate_other_info(username, github_stats: dict, birthday: str = "2000-10-04") -> str:
    age = calculate_age(birthday)
    lines = [
        f"{username}@Github",
        "-------------------",
        "OS: A coffee fueled brain",
        "Host: A very tired body",
        "Kernel: Trauma",
        f"Uptime: {age}",
        "Shell: DAIKAN - Direct Assertive Individual Known for Abrasive Nature",
        "Theme: Dark because light attracts bugs",
        "Memory: Very weak",
        "GitHub Stats:",
        f"Repositories Count: {github_stats['repositoryCount']}",
        f"Total Contributions: {github_stats['totalContributions']}",
        "Languages Percentage:"
    ]
    
    for lang, perc in github_stats["languagePercentages"].items():
        lines.append(f"  {lang}: {perc}%")
    
    return "\n".join(lines)
