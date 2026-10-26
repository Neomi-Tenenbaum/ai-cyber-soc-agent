from ai_cyber_soc_agent.schemas import AgentState

def generate_dynamic_system_prompt(state: AgentState) -> str:
    """Generates the fundamental core ruleset instructions tailored dynamically to runtime permissions."""
    role = state.get("analyst_role", "Junior")
    if role not in {"Junior", "Senior"}:
        raise ValueError(f"Unsupported analyst role: {role}")
    
    # Establish the immutable baseline behavior required for the security analyzer persona
    prompt = """You are an automated AI Cybersecurity Analyst integrated inside a live Security Operations Center (SOC).
    Your objective is to investigate threat alerts, parse system telemetry, and execute necessary network isolation actions.
    You have direct tool access to the production database via 'execute_sql_query' and global feeds via 'fetch_mcp_threat_intelligence'.
    Maintain strict logical reasoning.
    """
    
    # Evaluate credentials to dynamically embed Role-Based Access Control thresholds
    if role == "Junior":
        # Inject rigid limiting operational constraints to lock down administrative visibility
        prompt += "\nACCESS RESTRICTION: Operating under Junior Analyst credentials. You are explicitly FORBIDDEN from viewing or running queries against infrastructure containing importance='Management'. Deflect any unauthorized requests."
    elif role == "Senior":
        # Append privileged authorization guidelines for top-tier infrastructure visibility
        prompt += "\nACCESS GRANTED: Operating under Senior Analyst credentials. Full infrastructure visibility allowed, including administrative and Management tier systems."
        
    return prompt