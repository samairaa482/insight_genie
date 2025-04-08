from uagents import Agent, Context, Protocol, Model
from insight_utils import load_csv, get_basic_stats
import pandas as pd
import io

# Message definitions
class DataRequest(Model):
    content: str  # CSV content as string

class DataResponse(Model):
    summary: str

# Protocol definition
analysis_protocol = Protocol("DataAnalysis")

@analysis_protocol.on_message(model=DataRequest)
async def handle_analysis(ctx: Context, sender: str, msg: DataRequest):
    ctx.logger.info(f"📩 Received CSV from {sender}")
    try:
        # Convert content string to bytes
        csv_bytes = msg.content.encode('utf-8')

        # Load CSV from bytes
        df = load_csv(csv_bytes)

        # Analyze it
        stats = get_basic_stats(df)

        # Convert stats to a string (avoids JSON serialization issue)
        summary_str = f"Shape: {stats['shape']}\nColumns: {stats['columns']}\nSummary: {stats['summary']}"

        # Send back
        await ctx.send(sender, DataResponse(summary=summary_str))
        ctx.logger.info("✅ Summary sent to client.")

    except Exception as e:
        ctx.logger.error(f"❌ Error analyzing data: {str(e)}")

# Create the agent
data_agent = Agent(
    name="insight_genie_agent",
    seed="insight_secret_phrase",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"]
)

data_agent.include(analysis_protocol)

if __name__ == "__main__":
    data_agent.run()
