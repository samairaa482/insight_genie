from uagents import Agent, Context, Protocol, Model

class DataRequest(Model):
    content: str

class DataResponse(Model):
    summary: str

import asyncio

# Define the same model as the main agent
class DataRequest(Model):
    content: str

# Replace with your actual main agent's address
GENIE_ADDRESS = "agent1qfgf6g08je8gjef7nkzn8u3mxv5k96jzw2hvr0qpxjcjgec20wlq77kf9mu"

# Sample CSV content
csv_data = """name,age
Alice,23
Bob,30
"""

# Create the client agent
client_agent = Agent(
    name="test_client",
    seed="test_client_secret",
    port=8002,
)

# When the agent starts up, send the data
@client_agent.on_event("startup")
async def send_data(ctx: Context):
    await asyncio.sleep(2)  # Let it connect fully
    await ctx.send(GENIE_ADDRESS, DataRequest(content=csv_data))
    ctx.logger.info("✅ Sent CSV data to Insight Genie")

# Run the agent
if __name__ == "__main__":
    client_agent.run()
