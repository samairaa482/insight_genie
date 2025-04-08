from uagents import Agent, Context, Protocol, Model
from insight_utils import generate_summary  # You can also import plotting functions if needed

# Define a message format using a Pydantic model
class DataRequest(Model):
    content: str  # Assume CSV content is passed as a string

class DataResponse(Model):
    summary: str

# Define the protocol
analysis_protocol = Protocol("DataAnalysis")

@analysis_protocol.on_message(model=DataRequest)
async def handle_analysis(ctx: Context, sender: str, msg: DataRequest):
    ctx.logger.info(f"Received data from {sender}")
    
    # Save the content into a temporary CSV file
    with open("temp_data.csv", "w") as f:
        f.write(msg.content)

    # Use the utility to analyze it
    summary = generate_summary("temp_data.csv")

    # Respond back with summary
    await ctx.send(sender, DataResponse(summary=summary))

# Create the agent
data_agent = Agent(
    name="insight_genie_agent",
    seed="insight_secret_phrase",  # You can customize this
    endpoint=["http://127.0.0.1:8001/submit"],
    port=8001,
)

# Add the protocol
data_agent.include(analysis_protocol)

if __name__ == "__main__":
    data_agent.run()
