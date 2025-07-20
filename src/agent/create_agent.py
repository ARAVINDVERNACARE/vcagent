import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import FunctionTool, ToolSet, MessageRole, ListSortOrder
from user_functions import user_functions

def main():
    load_dotenv()
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    agent_client = AgentsClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )

    with agent_client:
        functions = FunctionTool(user_functions)
        toolset = ToolSet()
        toolset.add(functions)

        agent_client.enable_auto_function_calls(toolset)

        # Create the agent
        agent = agent_client.create_agent(
            model=model_deployment,
            name="sql-query-agent",
            instructions="""
                You are a smart data assistant. 
                When a user asks a question, use your tool to convert it into SQL and return the answer from the database.
            """,
            toolset=toolset
        )

        thread = agent_client.threads.create()
        print(f"🧠 Agent {agent.name} created! (ID: {agent.id})")

        while True:
            user_input = input("💬 You: ")
            if user_input.lower() == "quit":
                break

            agent_client.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_input
            )

            run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

            if run.status == "failed":
                print("❌ Run failed:", run.last_error)
                continue

            last_msg = agent_client.messages.get_last_message_text_by_role(
                thread_id=thread.id,
                role=MessageRole.AGENT
            )
            if last_msg:
                print("🤖 Agent:", last_msg.text.value)

        agent_client.delete_agent(agent.id)
        print("🧹 Agent deleted.")

if __name__ == "__main__":
    main()
