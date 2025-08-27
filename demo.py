import json
from pathlib import Path

from agent import LangGraphAgent


def main():
    # Path to config
    config_file = Path(__file__).parent / "config.yml"

    # Initialize agent
    agent = LangGraphAgent(config_file)

    # Sample customer query input
    sample_input = {
        "customer_name": "Alice",
        "email": "alice@example.com",
        "query": "My order #123 hasn’t arrived.",
        "priority": "high",
        "ticket_id": "TCKT-9999"
    }

    # Run workflow
    final_output = agent.run(sample_input)

    # Print final structured payload
    print("\n📦 Final Output Payload:")
    print(json.dumps(final_output, indent=2))

    # Save execution log + final payload
    logs_file = Path(__file__).parent / "logs.json"
    with open(logs_file, "w") as f:
        json.dump(final_output, f, indent=2)

    print(f"\n📝 Logs + payload written to {logs_file}")


if __name__ == "__main__":
    main()
