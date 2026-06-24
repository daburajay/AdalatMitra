import os

folders = [
    "agents",
    "services",
    "database",
    "models",
    "prompts",
    "utils",
    "config",
    "data",
    "data/judgments",
    "data/orders",
]

files = [
    "streamlit_app.py",
    ".env",
    "requirements.txt",

    "agents/orchestrator.py",
    "agents/case_agent.py",
    "agents/explanation_agent.py",
    "agents/timeline_agent.py",
    "agents/next_action_agent.py",
    "agents/reminder_agent.py",
    "agents/rag_agent.py",

    "services/court_api_service.py",
    "services/llm_service.py",
    "services/embedding_service.py",
    "services/notification_service.py",

    "database/postgres.py",
    "database/qdrant_client.py",

    "models/case_model.py",
    "models/hearing_model.py",
    "models/response_model.py",

    "prompts/explanation_prompt.py",
    "prompts/timeline_prompt.py",
    "prompts/next_action_prompt.py",

    "utils/logger.py",
    "utils/helpers.py",
    "utils/constants.py",

    "config/settings.py"
]

# Create folders first
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for file in files:
    with open(file, "w") as f:
        pass

print("✅ AdalatMitra project structure created successfully!")