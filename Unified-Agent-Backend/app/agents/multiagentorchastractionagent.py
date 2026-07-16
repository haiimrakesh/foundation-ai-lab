# file: agents/orchestration_loop.py
from crewai import Crew

# --- Specialized agents ---
def availability_agent(query, context):
    """Check if the requested book exists in the library DB."""
    books = ["The Great Gatsby", "War and Peace", "1984"]
    for book in books:
        if book.lower() in query.lower():
            return {"available": True, "book": book, "handover": "loan"}
    return {"available": False, "book": None, "handover": None}

def loan_agent(query, context):
    """Loan the book if available."""
    if context.get("available"):
        return {"loaned": True, "book": context["book"], "handover": "policy"}
    return {"loaned": False, "reason": "Book not available", "handover": None}

def policy_agent(query, context):
    """Check borrowing policies (max 5 books)."""
    borrowed_count = 4  # Example: user already has 4 books
    if borrowed_count >= 5:
        return {"allowed": False, "reason": "Borrowing limit reached", "handover": None}
    return {"allowed": True, "remaining": 5 - borrowed_count, "handover": None}

# --- Crew setup ---
crew = Crew()
crew.add_agent("availability", availability_agent)
crew.add_agent("loan", loan_agent)
crew.add_agent("policy", policy_agent)

# --- Central Orchestrator ---
def orchestrate(query, publish_mode=False):
    """
    Orchestration loop:
    - If publish_mode=True → broadcast query to all agents, collect responses.
    - Otherwise → follow agent handovers until no next agent is suggested.
    """
    context = {}
    trace = []
    current_agent = "availability"

    while True:
        if publish_mode:
            # Broadcast to all agents
            results = {}
            for agent_name in ["availability", "loan", "policy"]:
                results[agent_name] = crew.run(agent_name, query, context)
            trace.append(f"📢 Published to all agents → {results}")
            # Decide best next agent based on responses
            if results["availability"].get("available"):
                context.update(results["availability"])
                current_agent = "loan"
            elif results["loan"].get("loaned"):
                context.update(results["loan"])
                current_agent = "policy"
            else:
                current_agent = None
        else:
            # Sequential handover mode
            trace.append(f"➡️ Sending to {current_agent} agent...")
            result = crew.run(current_agent, query, context)
            trace.append(f"🔎 {current_agent} result → {result}")
            context.update(result)
            current_agent = result.get("handover")

        if not current_agent:
            break

    # Final decision
    if not context.get("available"):
        trace.append("❌ Book not available.")
    elif not context.get("loaned"):
        trace.append(f"❌ Loan failed: {context.get('reason')}")
    elif not context.get("allowed"):
        trace.append(f"⚠️ Loan denied: {context.get('reason')}")
    else:
        trace.append(f"✅ Book '{context['book']}' loaned successfully. You may borrow {context['remaining']} more books.")

    return "\n".join(trace)

# --- Example run ---
if __name__ == "__main__":
    print(orchestrate("Can I borrow War and Peace?", publish_mode=False))
    print("\n---\n")
    print(orchestrate("Can I borrow War and Peace?", publish_mode=True))
