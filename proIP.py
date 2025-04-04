import requests
from github import Github

# GitHub 配置
GITHUB_TOKEN = "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"  # 替换为你的 Personal Access Token
REPO_NAME = "kpsmail/new"  # 目标仓库
OUTPUT_FILE_PATH = "IPV4.txt"  # 目标文件路径（在 GitHub 仓库中）
BRANCH = "main"  # 目标分支

# 源文件 URL
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

# 将结果写入本地文件（可选，用于检查）
with open("temp_output.txt", "w") as f:
    f.write("\n".join(formatted_lines))

# 使用 GitHub API 上传文件
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

# 检查文件是否已存在，若存在则更新，否则创建
try:
    file = repo.get_contents(OUTPUT_FILE_PATH, ref=BRANCH)
    repo.update_file(
        OUTPUT_FILE_PATH,
        "Update IPV4.txt with formatted IPs",
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

print("任务完成！")