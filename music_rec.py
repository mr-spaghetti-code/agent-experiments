import autogen

config_list_gpt4 = [{
    "model": "gpt-4",
    "api_key": "<API_KEY>"
}
]

gpt4_config = {
    "seed": 42, 
    "temperature": 0,
    "config_list": config_list_gpt4,
    "request_timeout": 120,
}

## Agents:
# Planner
# Hispter
# Basic
# Musicologist


user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    code_execution_config=False,
    )


hispter = autogen.AssistantAgent(
    name="hispter",
    llm_config=gpt4_config,
    system_message='''Hispter. Work with Recommender to suggest music to Admin that is less well known and more obscure.
''',
)

musicologist = autogen.AssistantAgent(
    name="musicologist",
    llm_config=gpt4_config,
    system_message='''Musicologist. Work with Recommender to suggest music to Admin that is musically and historically relevant.
    Incorporate music theory and history into learning content for Admin. Write short essays about key concepts that will help Admin understand the genre, music, or artist.
''',
)

planner = autogen.AssistantAgent(
    name="Planner",
    llm_config=gpt4_config,
    system_message='''Planner. Suggest a plan. Revise the plan based on feedback from Admin and Critic, until Recommender approval.
    Explain the plan first.  Be clear which step is performed by which agent.
''',
)

recommender = autogen.AssistantAgent(
    name="Recommender",
    llm_config=gpt4_config,
    system_message='''Recommender. You follow an approved plan. You are a music expert who can teach Admin about new genres, artists, or tracks.
    You are ultimately responsible for providing the best content to Admin based on their request, preferences, taste.
    Make suggestions based on feedback from Admin, Critic, Hipster, and Musicologist.
'''
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message="Critic. Double check plan and claims from other agents and provide feedback. You ensure that the Admin's request is satisfied.",
    llm_config=gpt4_config,
)

groupchat = autogen.GroupChat(agents=[
    user_proxy,
    hispter,
    musicologist,
    planner,
    recommender,
    critic,
], messages=[], max_round=50)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)

user_proxy.initiate_chat(
    manager,
    message="""
I want to learn more about Japanese ambient music like St. Giga. Give me a learning syllabus to learn about this genre with specific music I should listen to and content for me to read.
""",
)

