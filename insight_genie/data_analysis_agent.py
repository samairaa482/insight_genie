from uagents import Agent, Context, Protocol, Model
from insight_utils import load_csv, get_basic_stats  # Utility functions
import base64
import os

# Message format using Pydantic model
class DataRequest(Model):
    content: str  # Base64-encoded CSV content

class DataResponse(Model):
    summary: str  # JSON-like string summary

# Define protocol
analysis_protocol = Protocol("DataAnalysis")

@analysis_protocol.on_message(model=DataRequest)
async def handle_analysis(ctx: Context, sender: str, msg: DataRequest):
    ctx.logger.info(f"📩 Received data from {sender}")

    try:
        # Decode the base64 string back to bytes
        file_bytes = base64.b64decode(msg.content)

        # Use utility to load and summarize data
        df = load_csv(file_bytes)
        summary = get_basic_stats(df)

        # Log and respond
        ctx.logger.info("✅ Data analysis completed")
        await ctx.send(sender, DataResponse(summary=str(summary)))

    except Exception as e:
        ctx.logger.error(f"❌ Error analyzing data: {e}")
        await ctx.send(sender, DataResponse(summary=f"Error: {e}"))

# Instantiate the agent
data_agent = Agent(
    name="insight_genie_agent",
    seed="insight_secret_phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
    port=8001,
)

# Attach the protocol
data_agent.include(analysis_protocol)

# Run the agent
if __name__ == "__main__":
    data_agent.run()
