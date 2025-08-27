import logging
from typing import Dict, Any
import requests  # Can be used if you connect to real MCP servers

logger = logging.getLogger("MCPClient")


class MCPClient:
    """
    Base MCP client class for ability execution.
    """

    def __init__(self, server_type: str, base_url: str = None):
        self.server_type = server_type
        self.base_url = base_url or f"http://localhost:8000/{server_type.lower()}"

    def execute(self, ability: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a given ability.
        Currently mocked; replace with real API calls if servers are available.
        """
        logger.info(f"[{self.server_type}] Executing ability: {ability}")

        # Example of real HTTP call if needed
        # try:
        #     response = requests.post(
        #         f"{self.base_url}/{ability}",
        #         json=payload,
        #         timeout=5
        #     )
        #     response.raise_for_status()
        #     return response.json()
        # except requests.RequestException as e:
        #     logger.error(f"Error executing {ability} on {self.server_type}: {e}")
        #     return {f"{ability}_error": str(e)}

        # Mocked response for now
        return {f"{ability}_result": f"Simulated result from {self.server_type}"}


class CommonClient(MCPClient):
    def __init__(self, base_url: str = None):
        super().__init__("COMMON", base_url)


class AtlasClient(MCPClient):
    def __init__(self, base_url: str = None):
        super().__init__("ATLAS", base_url)
