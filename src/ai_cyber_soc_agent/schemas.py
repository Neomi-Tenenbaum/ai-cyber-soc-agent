from typing import TypedDict, List, Literal, Any, Dict, Annotated
from pydantic import BaseModel, Field, IPvAnyAddress
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing import NotRequired


class AgentState(TypedDict):
    """Represents the global state synchronized across all nodes in the graph network."""
    messages: Annotated[List[BaseMessage], add_messages]
    analyst_role: Literal["Junior", "Senior"]
    structured_report: NotRequired[Dict[str, Any]]

class TechnicalRiskReport(BaseModel):
    """Pydantic model enforcing a strict structured schema format for compliance logging."""
    target_ip: IPvAnyAddress = Field(description="The IP address of the targeted or analyzed network host")
    detected_vulnerabilities: List[str] = Field(description="List of identified CVE identifiers affecting the asset")
    risk_score: int = Field(ge=1, le=100, description="Calculated risk level score scaled from 1 to 100")
    remediation_steps: str = Field(description="Actionable remediation and mitigation steps for network recovery")
