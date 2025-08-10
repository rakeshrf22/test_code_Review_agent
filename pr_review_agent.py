import argparse
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

# ---- State Definition ----
class PRState(TypedDict):
    pr_number: int
    repo: str
    changed_files: str
    code_diff: str
    raw_review_notes: str
    final_comments: str

# ---- Nodes ----
def pull_request_trigger(state: PRState):
    # In practice, fetch PR data via GitHub API
    print(f"Fetching PR #{state['pr_number']} from {state['repo']}...")
    # Placeholder
    state["changed_files"] = "file1.py, file2.py"
    state["code_diff"] = "diff --git a/file1.py b/file1.py ..."
    return state

def automated_code_review(state: PRState):
    # TODO: Call LLM with prompt
    print("Running LLM review...")
    state["raw_review_notes"] = "Found a potential bug in file1.py at line 42..."
    return state

def comments_generation(state: PRState):
    print("Generating structured comments...")
    state["final_comments"] = "- file1.py:42 — Consider using `len()` instead of manual count."
    return state

def post_results(state: PRState):
    # TODO: Post comments to PR via GitHub API
    print(f"Posting comments:\n{state['final_comments']}")
    return state

# ---- Graph ----
def build_graph():
    workflow = StateGraph(PRState)
    workflow.add_node("pull_request_trigger", pull_request_trigger)
    workflow.add_node("automated_code_review", automated_code_review)
    workflow.add_node("comments_generation", comments_generation)
    workflow.add_node("post_results", post_results)

    workflow.set_entry_point("pull_request_trigger")
    workflow.add_edge("pull_request_trigger", "automated_code_review")
    workflow.add_edge("automated_code_review", "comments_generation")
    workflow.add_edge("comments_generation", "post_results")

    return workflow

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr-number", type=int, required=True)
    parser.add_argument("--repo", type=str, required=True)
    args = parser.parse_args()

    graph = build_graph()
    final_graph = graph.compile()
    final_graph.invoke({"pr_number": args.pr_number, "repo": args.repo})
