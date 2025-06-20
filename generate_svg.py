import os
from usr.fetch_data import fetch_github_data
from usr.user_info import generate_other_info

ASCII_FILE = os.path.join("usr", "ascii.txt")
OUTPUT_SVG = "github_stats.svg"


def escape_svg(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


def pad_lines(lines, length):
    while len(lines) < length:
        lines.append("")
    return lines


def combine_columns(left_lines, right_lines, gap=5):
    max_lines = max(len(left_lines), len(right_lines))
    left_lines = pad_lines(left_lines, max_lines)
    right_lines = pad_lines(right_lines, max_lines)
    left_width = max(len(line) for line in left_lines)

    combined = [
        f"{left_lines[i].ljust(left_width + gap)}{right_lines[i]}"
        for i in range(max_lines)
    ]
    return combined


def generate_svg_lines(lines: list) -> str:
    svg_lines = []
    y = 30
    for line in lines:
        svg_lines.append(f'<tspan x="20" y="{y}">{escape_svg(line)}</tspan>')
        y += 20  # line height
    return "\n    ".join(svg_lines)


def generate_svg(ascii_lines, stats_lines):
    combined_lines = combine_columns(ascii_lines, stats_lines)
    svg_text = generate_svg_lines(combined_lines)
    height = 20 * len(combined_lines) + 40

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}">
  <style>
    text {{
      font-family: monospace;
      font-size: 14px;
      fill: #2c3e50;
      white-space: pre;
    }}
    rect {{
      fill: #fdf6e3;
    }}
  </style>
  <rect width="100%" height="100%" rx="15" ry="15"/>
  <text>{svg_text}</text>
</svg>'''


def main():
    if not os.path.exists(ASCII_FILE):
        print(f"⚠️ ASCII file '{ASCII_FILE}' not found.")
        return

    with open(ASCII_FILE, "r", encoding="utf-8") as f:
        ascii_art = f.read().strip().splitlines()

    github_stats, username = fetch_github_data()
    stats_text = generate_other_info(username, github_stats)
    stats_lines = stats_text.splitlines()

    svg_content = generate_svg(ascii_art, stats_lines)

    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"✅ SVG generated successfully → {OUTPUT_SVG}")


if __name__ == "__main__":
    main()
