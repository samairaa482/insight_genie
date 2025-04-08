from uagents import Agent, Context, Model
import asyncio

# Define message model
class DataRequest(Model):
    content: str


GENIE_ADDRESS = "agent1qfgf6g08je8gjef7nkzn8u3mxv5k96jzw2hvr0qpxjcjgec20wlq77kf9mu"

# Sample CSV content
csv_data = """name,age
Alice,23
Bob,30
"""

# Save it locally as temp_data.csv (optional for debug/demo)
with open("temp_data.csv", "w") as f:
    f.write(csv_data)

# Create the client agent
client_agent = Agent(
    name="test_client",
    seed="test_client_secret",
    port=8002,
)

# When the client starts, send the message
@client_agent.on_event("startup")
async def send_data(ctx: Context):
    await asyncio.sleep(2)  # Allow time to initialize
    ctx.logger.info("🚀 Sending CSV to Insight Genie...")
    await ctx.send(GENIE_ADDRESS, DataRequest(content=csv_data))
    ctx.logger.info("✅ CSV data sent to Insight Genie")

# Run the agent
if __name__ == "__main__":
    client_agent.run()
