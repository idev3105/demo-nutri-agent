from google.adk.agents import Agent, SequentialAgent

analysis_food_agent = Agent(
    model='gemini-2.0-flash-001',
    name='analysis_food_agent',
    description='A helpful assistant for user questions about food analysis.',
    instruction='You are a food analysis assistant. User will give you a image of food and you will analyze the ingredients and weight of each ingredient.',
)

calories_food_agent = Agent(
    model='gemini-2.0-flash-001',
    name='calories_food_agent',
    description='A helpful assistant for user questions about food calories.',
    instruction='You are a food calories assistant. User will give you a list of ingredient and weight of each ingredient and you will calculate the calories of each ingredient and total calories. You must return the result as a json object.',
)

root_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[analysis_food_agent, calories_food_agent],
    description="A helpful assistant for user questions about food analysis and calories.",
)
