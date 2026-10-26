import sqlite3
from contextlib import closing, contextmanager
from typing import Annotated, Iterator, Literal
from langgraph.prebuilt import InjectedState

from ai_cyber_soc_agent.schemas import AgentState
from langchain_core.tools import tool

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from init_db import DATABASE_PATH


@contextmanager
def _database_connection() -> Iterator[sqlite3.Connection]:
    with closing(sqlite3.connect(DATABASE_PATH)) as conn:
        with conn:
            yield conn


@tool
def list_database_tables() -> str:
    """List application tables in the SOC database. Does not return table data."""
    try:
        with _database_connection() as conn:
            rows = conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
            ).fetchall()

        tables = [name for (name,) in rows if not name.startswith("sqlite_")]
        return "\n".join(tables) if tables else "No application tables found."
    except sqlite3.Error:
        return "Database operation failed."


@tool
def describe_database_table(table_name: str) -> str:
    """Show column names and types for an existing application table."""
    try:
        with _database_connection() as conn:
            row = conn.execute(
                """
                SELECT name FROM sqlite_master
                WHERE type = 'table' AND name = ?
                """,
                (table_name,),
            ).fetchone()

            if row is None or table_name.startswith("sqlite_"):
                return "Unknown table."

            quoted_name = '"' + table_name.replace('"', '""') + '"'
            columns = conn.execute(
                f"PRAGMA table_info({quoted_name})"
            ).fetchall()

        return "\n".join(
            f"{column[1]}: {column[2]}" for column in columns
        )
    except sqlite3.Error:
        return "Database operation failed."


@tool
def get_server(
    ip: str,
    state: Annotated[AgentState, InjectedState],
) -> str:
    """Get one server by IP, applying the analyst's access level."""
    role = state.get("analyst_role", "Junior")
    if role not in {"Junior", "Senior"}:
        return "Access denied: unknown analyst role."

    try:
        with _database_connection() as conn:
            row = conn.execute(
                """
                SELECT ip, os, status, importance
                FROM Servers
                WHERE ip = ?
                  AND (importance != 'Management' OR ? = 'Senior')
                """,
                (ip, role),
            ).fetchone()

        return str(row) if row else "Server not found or access denied."
    except sqlite3.Error as exc:
        return f"Database operation failed: {exc}"


@tool
def update_server_status(
    ip: str,
    status: Literal["active", "compromised", "isolated"],
    state: Annotated[AgentState, InjectedState],
) -> str:
    """Update the status of one server. Restricted to Senior analysts."""
    role = state.get("analyst_role", "Junior")
    if role != "Senior":
        return "Access denied."

    if status not in {"active", "compromised", "isolated"}:
        return "Unsupported status."

    try:
        with _database_connection() as conn:
            cursor = conn.execute(
                "UPDATE Servers SET status = ? WHERE ip = ?",
                (status, ip),
            )
            if cursor.rowcount != 1:
                return "No matching server was updated."

        return "Status updated."
    except sqlite3.Error:
        return "Database operation failed."


@tool
def fetch_mcp_threat_intelligence(cve_id: str) -> str:
    """Query external global threat intelligence databases via the Model Context Protocol (MCP) server."""
    # Simulate an external network API fetch mapping known threat exploits to incoming CVE hashes
    if "2026-0001" in cve_id:
        return "MCP Intelligence Feed: CVE-2026-0001 is actively exploited by threat actors. Immediate remediation required."
    return f"MCP Intelligence Feed: Metadata logged for {cve_id}. Baseline severity confirmed."
