# AI-Driven Cyber SOC Analyst & Incident Response Agent

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-Stateful__Agents-orange)
![License](https://img.shields.io/badge/License-MIT-green)

An AI-powered Security Operations Center (SOC) agent built with **Python, LangChain, and LangGraph**. The system investigates security assets, retrieves CVE-related threat intelligence, enforces role-based access restrictions, and coordinates incident-response actions through human approval workflows. The project demonstrates agent orchestration, stateful execution, policy enforcement, and controlled database operations in cybersecurity incident-response scenarios.

## Key Features

- **Agentic Workflow Orchestration:** Uses LangGraph to coordinate LLM reasoning, tool execution, conditional routing, and workflow transitions.
- **Role-Based Access Control (RBAC):** Applies role-specific restrictions for Junior and Senior analysts.
- **Tool-Based Investigation:** Provides tools to inspect database schemas, retrieve server information, and update server status.
- **Human-in-the-Loop (HITL):** Uses LangGraph interrupts and resume commands to require supervisor approval before executing sensitive isolation actions.
- **State Management:** Uses LangGraph state management and in-memory checkpointing to support controlled workflow interruption and resumption.
- **Threat Intelligence:** Incorporates a CVE-related intelligence tool into the incident-response workflow.
- **Relational Data Management:** Uses SQLite to manage server inventory, vulnerability records, and security logs.

## Architecture

```text
User Request
     |
     v
Dynamic System Prompt (Role-Based Rules)
     |
     v
LangGraph Agent
     |
     v
Tool Selection and Routing
     |
     +--------+--------+

     |                 |
     v                 v
Read-Only Operations  Sensitive Action

     |                 |
     v                 v
Execute Tool      Human Approval Gate
                       |
                 +-----+-----+

                 |           |
                 v           v
              Approve     Reject

                 |           |
                 v           v
           Execute Update  Block Update

                 |           |
                 +-----+-----+
                       |
                       v
                Agent Response
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic and tool implementation |
| LangChain | LLM integration and tool calling |
| LangGraph | Workflow orchestration, conditional routing, and interrupt/resume handling |
| OpenAI API | Language model inference |
| SQLite | Local relational database |
| Pydantic | Structured data validation where defined by the application |
| uv | Dependency and environment management |

## Database Schema

The application uses a local SQLite database with three primary tables.

| Table | Description |
|---|---|
| `Servers` | Stores server IP addresses, operating systems, operational statuses, and importance levels. |
| `Vulnerabilities` | Stores CVE identifiers, vulnerability descriptions, and severity levels. |
| `Security_Logs` | Stores timestamped security events associated with server IP addresses. |

The `Servers` table includes:
- `ip` — Server IP address
- `os` — Operating system
- `status` — Operational or security status
- `importance` — Asset importance classification

Supported server statuses include `active`, `compromised`, and `isolated`.

## Demonstrated Scenarios

### Case 1 — Role-Based Access Restriction
- **Role:** Junior Analyst  
- **Key concepts:** Role-aware behavior and restricted access to sensitive assets.

The agent receives a request to retrieve all records for servers classified as `Management`. Access is denied under the configured role-based restrictions.  

### Case 2 — Isolation Rejected
- **Role:** Senior Analyst  
- **Key concepts:** Human-in-the-loop approval, interrupt/resume control flow, and enforcement of rejected actions.

The agent retrieves server `192.168.1.90` and identifies its status as `compromised`. It requests an isolation operation, but the supervisor rejects the action. The database update is blocked.  

### Case 3 — Isolation Approved
- **Role:** Senior Analyst  
- **Key concepts:** Multi-step tool orchestration, threat-intelligence workflow integration, human approval, and controlled database mutation.

The agent requests threat intelligence for `CVE-2026-0001` and then requests isolation of server `192.168.1.50`. Following supervisor approval, the server status is successfully updated to `isolated`.

## Getting Started

### Prerequisites
- Python version compatible with the project dependencies
- [`uv`](https://docs.astral.sh/uv/)
- An OpenAI API key

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/Neomi-Tenenbaum/ai-cyber-soc-agent.git
cd ai-cyber-soc-agent
```

**2. Install dependencies**
```bash
uv sync
```

**3. Configure your API access key in the root environment file**
   ```bash
   echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
   ```
*Keep credentials out of source control. Do not commit the `.env` file.*

**4. Initialize the database**
```bash
uv run python init_db.py
```

**5. Run the application**
```bash
uv run python src/ai_cyber_soc_agent/main.py
```
The application executes the three demonstration scenarios and prints model responses, tool calls, and approval outcomes to the terminal.

### Example Output

When you run the application, the agent executes the three configured scenarios sequentially. You can view a complete sample execution log, including the agent's multi-step tool calls, role-based restriction blocks, and human-in-the-loop decisions, in the [demo_run.log](demo_run.log) file.

## Project Structure

```text
ai-cyber-soc-agent/
├── demo_run.log
├── init_db.py
├── data/
│   └── cyber_security.db
├── src/
│   └── ai_cyber_soc_agent/
│       ├── __init__.py
│       ├── main.py
│       ├── prompts.py
│       ├── schemas.py
│       └── tools.py
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```
*The database is initialized locally. Environment files and sensitive credentials should be excluded from version control.*

## Design Considerations

- **Access control:** Role-based restrictions govern access to sensitive asset information.
- **Approval before mutation:** Sensitive isolation actions require explicit approval before execution.
- **Separation of concerns:** Agent orchestration, prompt generation, schemas, and tool implementations are maintained in separate modules.
- **Stateful execution:** LangGraph manages workflow state and supports interruption and resumption during approval handling.
- **Local persistence:** SQLite stores application data, while `InMemorySaver` maintains workflow checkpoints in memory.

## Scope

This project is a local cybersecurity agent prototype demonstrating controlled AI-assisted investigation and incident-response workflows. Supervisor decisions are simulated, and the current threat-intelligence tool provides a predefined response rather than querying a live external intelligence provider. The project does not claim deployment to production infrastructure.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
