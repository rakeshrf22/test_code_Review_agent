import os
from github import Github
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pathlib import Path

# -----------------------------
# 1. Environment Variables
# -----------------------------
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
LANGCHAIN_API_KEY = os.environ.get("LANGCHAIN_API_KEY")
PR_NUMBER = os.environ.get("PR_NUMBER")
REPO_NAME = os.environ.get("GITHUB_REPOSITORY")

if not all([GITHUB_TOKEN, LANGCHAIN_API_KEY, PR_NUMBER, REPO_NAME]):
    raise ValueError("Missing required environment variables.")

# -----------------------------
# 2. GitHub Client
# -----------------------------
gh = Github(GITHUB_TOKEN)
repo = gh.get_repo(REPO_NAME)
pr = repo.get_pull(int(PR_NUMBER))

print(f"🔍 Reviewing PR #{PR_NUMBER} in repo {REPO_NAME}")

# -----------------------------
# 3. Collect Java Files in PR
# -----------------------------
java_files = [f for f in pr.get_files() if f.filename.endswith(".java")]

if not java_files:
    print("⚠️ No Java files found in this PR. Exiting...")
    exit(0)

# -----------------------------
# 4. AI Model Setup
# -----------------------------
llm = ChatOpenAI(
    model="gpt-4o",  # You can use gpt-4o-mini for cost efficiency
    temperature=0,
    api_key=LANGCHAIN_API_KEY
)

review_prompt = PromptTemplate(
    input_variables=["filename", "code"],
    template="""
You are a **Senior Java Architect** performing a **strict, professional code review**.

Review the following file for:
- **Correctness** (bugs, logic errors, null handling, edge cases)
- **Code Quality** (readability, maintainability, naming conventions)
- **Performance**
- **Security** (input validation, injection risks)
- **Best Practices** (Java, OOP, design patterns)

Output:
- List findings as **clear bullet points**
- Suggest **specific improvements**
- Keep feedback **professional and concise**

File: {filename}

Code:

"""
def generate_html_report(summary, details):
    template_path = Path("reports/report_template.html").read_text()
    filled_html = template_path.replace("{{REVIEW_SUMMARY}}", summary)\
                               .replace("{{REVIEW_DETAILS}}", details)
    Path("reports/review_report.html").write_text(filled_html)

# Example usage
generate_html_report("No major issues found", "<ul><li>Consider refactoring method X</li></ul>")

