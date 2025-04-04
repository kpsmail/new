import requests
from github import Github
import os
import sys

# GitHub 配置
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN").strip()  # 去除首尾空格和换行符
REPO_NAME = "kpsmail/new"
OUTPUT_FILE_PATH = "IPV4.txt"
BRANCH = "main"
SOURCE_URL = "https://raw.githubusercontent.com/ymyuuu/IPDB/refs/heads/main/BestProxy/proxy.txt"

try:
    # 验证 Token 是否有效
    if not GITHUB_TOKEN:
        raise ValueError("GITHUB_TOKEN 环境变量未设置或为空")

    # 获取源文件内容
    print("正在获取源文件...")
    response = requests.get(SOURCE_URL, timeout=10)
    response.raise_for_status()
    ip_list = response.text.strip().splitlines()
    print(f"成功获取 {len(ip_list)} 个 IP 地址")

    # 格式转换
    formatted_lines = []
    for ip in ip_list:
        if ip:  # 跳过空行
            formatted_lines.append(f"{ip}:443")
            formatted_lines.append(f"{ip}:8443")
            formatted_lines.append(f"{ip}:2053")
    print(f"格式转换完成，生成了 {len(formatted_lines)} 行")

    # 使用 GitHub API 更新文件
    print(f"正在连接到 GitHub 仓库 {REPO_NAME}...")
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    print("连接成功")

    # 检查文件是否存在，存在则更新，不存在则创建
    print(f"正在更新文件 {OUTPUT_FILE_PATH}...")
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

except Exception as e:
    print(f"发生错误: {str(e)}", file=sys.stderr)
    sys.exit(1)
