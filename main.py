#!/usr/bin/env python3
import requests
import json
import os

# 输出文件
CACHE_FILE = "versions.json"

# GitHub Token (避免限流)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)

headers = {}
if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"

# 需要查询的项目
repos = {
    "nginx": "nginx/nginx",
    "php": "php/php-src",
    "mariadb": "MariaDB/server",
    "kubernetes": "kubernetes/kubernetes"
}

def fetch_latest_version(repo, latest=True):
    """获取最新版本号"""
    url = f"https://api.github.com/repos/{repo}/releases"
    if latest:
        url = f"https://api.github.com/repos/{repo}/releases/latest"

    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()

    if latest:
        name = data.get("name", "")
    else:
        name = data[0].get("name", "")

    import re
    match = re.search(r"\d+\.\d+\.\d+", name)
    return match.group(0) if match else "unknown"

def save_versions(versions):

    # with open(CACHE_FILE, "w", encoding="utf-8") as f:
    #     json.dump(output, f, indent=4)
    for i in versions:
        output = {"versions": versions[i]}  # 包裹一层 "versions"
        with open(i+".json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)

def main():
    versions = {}
    for repo in repos:
        versions[repo] = fetch_latest_version(repos[repo], latest=True)
    save_versions(versions)

if __name__ == "__main__":
    main()