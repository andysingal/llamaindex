```py
import os
import json
import requests
from crewai import Agent, Task, Crew
from crewai_tools import BaseTool

# 1. Create Custom Tool to Get Game Score from API
from crewai_tools import tool
@tool("Game Score Tool")
def game_score_tool(team_name: str) -> str:
    """Get the current score for a given NBA game by querying the Flask API. It accepts team_name"""
    url = f'http://127.0.0.1:5000/score?team={team_name}'
    response = requests.get(url)
    if response.status_code == 200:
        return json.dumps(response.json(), indent=2)
    else:
        return json.dumps({"error": "API request failed", "status_code": response.status_code}, indent=2)

# 2. Create Agents
researcher = Agent(
    role='Researcher',
    goal='Gather and analyze information on NBA game scores',
    verbose=True,
    backstory=(
        "As a seasoned researcher, you have a keen eye for detail and a "
        "deep understanding of sports analytics. You're adept at sifting through "
        "scores to find the most relevant and accurate data."
    ),
    tools=[game_score_tool],
    allow_delegation=False
)

writer = Agent(
    role='Sports Journalist',
    goal='Compose an engaging news article based on NBA game scores',
    verbose=True,
    backstory=(
        "With a talent for storytelling, you convert statistical data and game outcomes "
        "into engaging sports narratives. Your articles are insightful, capturing the excitement "
        "of the games and providing a deep analysis for sports enthusiasts."
    ),
    allow_delegation=False
)

# 3. Define Tasks
research_task = Task(
    description="Investigate the scores for the Warriors game.",
    expected_output='A detailed report summarizing the data.',
    tools=[game_score_tool],
    agent=researcher,
)

writing_task = Task(
    description="Write a detailed news article about an NBA game, focusing stats.",
    expected_output='An engaging and informative article suitable for publication in sports media.',
    context=[research_task],
    agent=writer,
)

# 4. Run the Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task]
)

result = crew.kickoff()
print(result)
```
