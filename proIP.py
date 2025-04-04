import requests
from github import Github
import os

# GitHub 配置
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # 从环境变量获取 Token
REPO_NAME = "kpsmail/new"
OUTPUT_FILE_PATH = "IPV4.txt"
BRANCH = "main"
SOURCE_URL = "https://raw.githubusercontent.com/ymyuuu/IPDB/refs/heads/main/BestProxy/proxy.txt"

# 获取源文件内容
response = requests.get(SOURCE_URL)
ip_list = response.text.strip().splitlines()

# 格式转换
formatted_lines = []
for ip in ip_list:
    if ip:  # 跳过空行
        formatted_lines.append(f"{ip}:443#443反代IP")
        formatted_lines.append(f"{ip}:8443#8443反代IP")
        formatted_lines.append(f"{ip}:2053#2053反代IP")

# 使用 GitHub API 更新文件
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# 检查文件是否存在，存在则更新，不存在则创建
try:
    file = repo.get_contents(OUTPUT_FILE_PATH, ref=BRANCH)
    repo.update_file(
        OUTPUT_FILE_PATH,
        "Auto-update IPV4.txt with formatted IPs",
        "\n".join(formatted_lines),
        file.sha,
        branch=BRANCH
    )
    print(f"文件 {OUTPUT_FILE_PATH} 已更新")
except:
    repo.create_file(
        OUTPUT_FILE_PATH,
        "Create IPV4.txt with formatted IPs",
        "\n".join(formatted_lines),
        branch=BRANCH
    )
    print(f"文件 {OUTPUT_FILE_PATH} 已创建")
