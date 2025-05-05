import asyncio
import sys
from google.adk.sessions import InMemorySessionService, Session
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from nutri_agent import agent
from google.genai.types import Content, Part, Blob
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Fix for Windows event loop issue
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

APP_NAME = "nutri_agent"

# Create a simple session to examine its properties
session_service = InMemorySessionService()
session: Session = session_service.create_session(
    app_name=APP_NAME,
    user_id="example_user",
    session_id="example_session",
)

memory_service = InMemoryMemoryService()

runner = Runner(
    # Start with the info capture agent
    agent=agent.root_agent,
    app_name=APP_NAME,
    session_service=session_service,
    memory_service=memory_service # Provide the memory service to the Runner
)

# Run the agent
async def run_agent(image_bytes: bytes = b""):
    if not image_bytes:
        raise ValueError("Image bytes cannot be empty.")
    user_input = Content(parts=[Part(inline_data=Blob(mime_type="image/png", data=image_bytes)), Part(text="Calculate calories")], role="user")
    final_response_text = "(No final response)"
    events = runner.run_async(user_id=session.user_id, session_id=session.id, new_message=user_input)
    async for event in events:
        # NOTE: Only use the final response, we don't need the whole conversation
        if event.is_final_response() and event.content and event.content.parts:
            final_response_text = event.content.parts[0].text
    final_response_text = final_response_text.replace("```json", "")
    final_response_text = final_response_text.replace("```", "")
    return final_response_text

# Flask app
app = Flask(__name__)
# Flask route to handle API requests
@app.route('/run_agent', methods=['POST'])
async def run_agent_api():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    # Read the image file
    image_file = request.files['image']
    image_bytes = image_file.read()

    # Run the agent asynchronously
    result = await run_agent(image_bytes)

    return jsonify({"response": result})

if __name__ == '__main__':
    app.run(debug=True)