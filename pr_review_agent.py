import os
import json
from github import Github
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

# ====== LangGraph Setup ======
from typing_extensions import TypedDict

class ReviewState(TypedDict):
    code: str
    review_summary: str
    findings: list

def analyze_code(state: ReviewState):
    """Analyze the code using LLM."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = f"""
    You are a senior code reviewer.
    Review the following Java code for best practices, bugs, and improvements.
    Provide:
    1. A summary
    2. A bullet-point list of findings

    Code:
    {state['code']}
    """
    response = llm.invoke(prompt).content
    summary, *findings = response.split("\n")
    return {"review_summary": summary, "findings": findings}

# ====== LangGraph Orchestration ======
graph = StateGraph(ReviewState)
graph.add_node("analyze", analyze_code)
graph.add_edge(START, "analyze")
graph.add_edge("analyze", END)
review_agent = graph.compile()

# ====== GitHub Helper ======
def post_github_comment(repo_name, pr_number, comment_body):
    g = Github(os.environ["GITHUB_TOKEN"])
    repo = g.get_repo(repo_name)
    pr = repo.get_pull(int(pr_number))
    pr.create_issue_comment(comment_body)

def format_html_review(summary, findings):
    css_styles = ""
    with open(".github/workflows/style.css", "r") as f:
        css_styles = f.read()

    html_report = f"""
    <style>{css_styles}</style>
    <div class="review-container">
        <h2>🤖 Automated Code Review Report</h2>
        <p>{summary}</p>
        <ul>
            {''.join([f"<li>{f}</li>" for f in findings])}
        </ul>
    </div>
    """
    return html_report

if __name__ == "__main__":
    repo_name = os.environ["GITHUB_REPOSITORY"]
    pr_number = os.environ["PR_NUMBER"]

    # Example: scan a Java file
    with open("src/main/java/com/example/MyClass.java", "r") as f:
        code_content = f.read()

    result = review_agent.invoke({"code": code_content})
    summary = result["review_summary"]
    findings = result["findings"]

    # Save HTML report
    html_review = format_html_review(summary, findings)
    with open("review_report.html", "w") as f:
        f.write(html_review)

    # Post PR comment (without full CSS, since GitHub strips most styles)
    markdown_comment = f"""
### 🤖 Automated Code Review
**Summary:**
{summary}

**Findings:**
{"".join([f"- {f}\n" for f in findings])}

📎 [Download Full Styled Report](./review_report.html)
"""
    post_github_comment(repo_name, pr_number, markdown_comment)
