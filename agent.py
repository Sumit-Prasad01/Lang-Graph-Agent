import yaml
import json
import logging
from pathlib import Path
from typing import Dict, Any
from mcp_client import CommonClient, AtlasClient

import requests  # For MCP client simulation


# =========================================================
# Logging Setup
# =========================================================
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)
logger = logging.getLogger("LangGraphAgent")


# =========================================================
# MCP Client (Common + Atlas)
# =========================================================
class MCPClient:
    def __init__(self, server_type: str):
        self.server_type = server_type
        self.clients = {
            "COMMON": CommonClient(),
            "ATLAS": AtlasClient()
        }

    def execute(self, ability: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulated ability execution.
        Replace this with actual API calls to MCP servers if available.
        """
        logger.info(f"[{self.server_type}] Executing ability: {ability}")
        # Mocked response for now
        return {f"{ability}_result": f"Simulated result from {self.server_type}"}


# =========================================================
# LangGraph Agent
# =========================================================
class LangGraphAgent:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.state: Dict[str, Any] = {}
        self.clients = {
            "COMMON": MCPClient("COMMON"),
            "ATLAS": MCPClient("ATLAS")
        }

    @staticmethod
    def _load_config(path: str) -> Dict[str, Any]:
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def run(self, input_payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("🚀 Starting Lang Graph Agent workflow")

        # Initialize state with input schema
        self.state.update(input_payload)

        for stage in self.config["stages"]:
            stage_name = stage["name"]
            mode = stage["mode"]
            logger.info(f"\n➡️ Stage: {stage_name} ({mode})")

            if mode == "deterministic":
                self._run_deterministic(stage)
            elif mode == "non-deterministic":
                self._run_non_deterministic(stage)

        logger.info("✅ Workflow Complete")
        return self.state

    def _run_deterministic(self, stage: Dict[str, Any]):
        for ability in stage["abilities"]:
            client = self.clients[ability["server"]]
            result = client.execute(ability["name"], self.state)
            self.state.update(result)

    def _run_non_deterministic(self, stage: Dict[str, Any]):
        """
        Example: DECIDE stage
        - Run solution_evaluation
        - If <90 -> escalation_decision
        - Else -> auto-resolve
        """
        # Step 1: Evaluate solution
        eval_result = self.clients["COMMON"].execute("solution_evaluation", self.state)
        score = 85  # Mock score; you can randomize or derive from eval_result
        self.state["solution_score"] = score

        logger.info(f"Solution score = {score}")

        if score < 90:
            result = self.clients["ATLAS"].execute("escalation_decision", self.state)
            self.state.update(result)
            self.state["decision"] = "escalated_to_human"
        else:
            self.state["decision"] = "auto_resolved"

        # Update payload in state
        update_result = self.clients["COMMON"].execute("update_payload", self.state)
        self.state.update(update_result)


# =========================================================
# Demo Run
# =========================================================
if __name__ == "__main__":
    config_file = Path(__file__).parent / "config.yml"

    agent = LangGraphAgent(config_file)

    sample_input = {
        "customer_name": "Alice",
        "email": "alice@example.com",
        "query": "My order #123 hasn’t arrived.",
        "priority": "high",
        "ticket_id": "TCKT-9999"
    }

    final_output = agent.run(sample_input)

    print("\n📦 Final Output Payload:")
    print(json.dumps(final_output, indent=2))
