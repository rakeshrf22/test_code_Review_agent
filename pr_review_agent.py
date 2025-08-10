import os
from github import Github
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

# --- GitHub Setup ---
gh = Github(os.environ["GITHUB_TOKEN"])
repo_name = os.environ["GITHUB_REPOSITORY"]
pr_number = int(os.environ["PR_NUMBER"])
repo = gh.get_repo(repo_name)
pr = repo.get_pull(pr_number)

# --- Collect Java files from the PR ---
java_files = [
    f for f in pr.get_files()
    if f.filename.endswith(".java")
]

if not java_files:
    print("No Java files found in PR.")
    exit(0)

# --- AI Review ---
llm = ChatOpenAI(model="gpt-4", temperature=0)

review_prompt = PromptTemplate(
    input_variables=["filename", "code"],
    template="""
You are a senior Java code reviewer.
Review the following file for code quality, best practices, potential bugs, and improvements.

File: {filename}

Code:
