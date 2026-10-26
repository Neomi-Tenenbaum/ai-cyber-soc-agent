import os
import sqlite3
import logging
from typing import List, Tuple

# Setup professional logging environment
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# System-wide static configurations
DATABASE_PATH = "data/cyber_security.db"

def reset_test_data() -> None:
    """Resets server statuses to their baseline values for testing."""
    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.executemany(
            "UPDATE Servers SET status = ? WHERE ip = ?",
            [
                ("active", "192.168.1.50"),
                ("compromised", "192.168.1.90"),
                ("active", "10.0.0.1"),
            ],
        )
    logger.info("Server test data reset to baseline statuses.")

def create_production_schema(cursor: sqlite3.Cursor) -> None:
    """Defines and builds the core database schemas for the SOC environment."""
    logger.info("Initializing relational database schemas...")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Servers (
            ip TEXT PRIMARY KEY,
            os TEXT NOT NULL,
            status TEXT NOT NULL,
            importance TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Vulnerabilities (
            cve_id TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            severity TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Security_Logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            ip TEXT NOT NULL,
            event TEXT NOT NULL
        )
    """)

def seed_baseline_data(cursor: sqlite3.Cursor) -> None:
    """Populates the database tables with baseline security operational records."""
    logger.info("Seeding baseline infrastructural vectors...")
    
    servers_payload: List[Tuple[str, str, str, str]] = [
        ("192.168.1.50", "Linux Ubuntu 22.04", "active", "Regular"),
        ("192.168.1.90", "CentOS 7", "compromised", "Regular"),
        ("10.0.0.1", "Windows Server 2022", "active", "Management")
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO Servers (ip, os, status, importance) VALUES (?, ?, ?, ?)", 
        servers_payload
    )
    
    vulnerabilities_payload: List[Tuple[str, str, str]] = [
        ("CVE-2026-0001", "Critical Remote Code Execution in core network daemon", "Critical"),
        ("CVE-2025-9999", "Privilege escalation via local system token manipulation", "High")
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO Vulnerabilities (cve_id, description, severity) VALUES (?, ?, ?)", 
        vulnerabilities_payload
    )

def initialize_soc_database() -> None:
    """Main execution lifecycle to establish and populate the secure cyber datastore."""
    
    try:
        # Enforce directory creation if it doesn't exist on the host filesystem
        db_dir = os.path.dirname(DATABASE_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        # Utilizing Context Managers to guarantee transaction safety and connection teardown
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            
            create_production_schema(cursor)
            seed_baseline_data(cursor)
            
            conn.commit()
            logger.info(f"Database successfully established at target location: '{DATABASE_PATH}'")
            
    except sqlite3.Error as e:
        logger.error(f"Critical error during database subsystem orchestration: {e}")
        raise

if __name__ == "__main__":
    initialize_soc_database()