## Lang Graph Agent – Customer Support Workflow

This project implements a **Lang Graph Agent** that models customer support workflows as a graph of **11 stages**.  
Each stage executes abilities via **MCP Clients** (COMMON or ATLAS), with state persistence across the workflow.  

---

## 🚀 Features
- **Graph-based workflow** with deterministic + non-deterministic stages.
- **State persistence**: variables passed from one stage to the next.
- **MCP client orchestration**:
  - COMMON server → abilities with no external data.
  - ATLAS server → abilities requiring external system interaction.
- **Stage logs** for demo and debugging.
- **Final structured payload** output at completion.

---

## 🏗️ Project Structure
```
lang-graph-agent/
│── agent.py # Main orchestrator (reads config + runs workflow)
│── mcp_client.py # MCP client classes (Common + Atlas)
│── demo.py # Demo runner with sample input
│── config.yml # Workflow definition (stages + abilities + servers)
│── requirements.txt # Dependencies
│── logs.json # Auto-generated workflow log + final payload
```
## Create virtual environment
```
python -m venv venv
# Activate it
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

## Install dependencies
```
pip install -r requirements.txt
```

## Running the Demo
```
Run:
python demo.py

Example logs:
➡️ Stage: UNDERSTAND (deterministic)
[COMMON] Executing ability: parse_request_text
[ATLAS] Executing ability: extract_entities
...
✅ Workflow Complete
```
## Example final payload (printed + saved to logs.json):
```
{
  "customer_name": "Alice",
  "email": "alice@example.com",
  "query": "My order #123 hasn’t arrived.",
  "priority": "high",
  "ticket_id": "TCKT-9999",
  "decision": "escalated_to_human",
  "solution_score": 85,
  "response_generation_result": "Simulated result from COMMON",
  "output_payload_result": "Simulated result from COMMON"
}
```

## 🧩 Workflow Stages

- INTAKE – accept payload

- UNDERSTAND – parse request, extract entities

- PREPARE – normalize, enrich, add flags

- ASK – clarify missing info

- WAIT – wait & store answer

- RETRIEVE – KB search & store data

- DECIDE – solution evaluation & escalation decision (non-deterministic)

- UPDATE – update/close ticket

- CREATE – generate response

- DO – API calls, notifications

- COMPLETE – output payload