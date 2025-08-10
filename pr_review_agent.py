import os
from pathlib import Path
import requests
from github import Github  # pip install PyGithub

# LangGraph imports would go here
# from langgraph import Graph, Node ...

# ---------- Configuration ----------
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("GITHUB_REPOSITORY")  # e.g., "rakeshrf22/test_code_Review_agent"
PR_NUMBER = os.getenv("PR_NUMBER", "1")  # will be passed from the workflow

# ---------- HTML Report Generator ----------
def generate_html_report(summary, details):
    template_path = Path("reports/report_template.html").read_text()
    filled_html = template_path.replace("{{REVIEW_SUMMARY}}", summary)\
                               .replace("{{REVIEW_DETAILS}}", details)
    Path("reports/review_report.html").write_text(filled_html)

# ---------- Markdown for GitHub Comment ----------
def format_markdown_report(summary, details):
    return f"""## 🤖 Automated Code Review

**Summary**  
{summary}

**Details**  
{details}
"""

# ---------- Dummy Review Logic (Replace with LangGraph output) ----------
def run_code_review():
    # Here, integrate your LangGraph pipeline to review Java code.
    # For now, we'll return dummy data.
    summary = "No major issues found, but some improvements suggested."
    details = "- Method `processData()` could use better exception handling.\n- Consider adding Javadoc for `UserService`."
    return summary, details

# ---------- Post to GitHub PR ----------
def post_pr_comment(markdown_text):
    gh = Github(GITHUB_TOKEN)
    repo = gh.get_repo(REPO_NAME)
    pr = repo.get_pull(int(PR_NUMBER))
    pr.create_issue_comment(markdown_text)

# ---------- Main Orchestration ----------
if __name__ == "__main__":
    summary, details = run_code_review()

    # Save HTML styled report
    generate_html_report(summary, f"<ul><li>{'</li><li>'.join(details.splitlines())}</li></ul>")

    # Post Markdown to PR
    markdown_text = format_markdown_report(summary, details)
    post_pr_comment(markdown_text)

    print("✅ Review complete. HTML report generated and PR comment posted.")
