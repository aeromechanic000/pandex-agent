
import os, curl_cffi
from agent import PandexAgent, PandexHub

test_agent_config_1 = {
    "template": "[[PROMPT]]",
    "executor": {
        "type": "pollinations",
    },
    "vars": {
        "prompt": {
            "type": "text",
            "default": "Hello world.",
        },
    },
}

test_agent_config_2 = {
    "template": "[[PROMPT]]",
    "executor": {
        "type": "pollinations",
    },
    "output" : {
        "type" : "json",
        "keys" : {
            "response" : {
                "type" : "string",
                "description" : "response content", 
            }
        }
    },
    "vars": {
        "prompt": {
            "type": "text",
            "default": "Hello world.",
        },
    },
}

def test_pollinations() : 
    print(f"\033[38;5;220m[test_pollinations]\033[0m Testing...")
    response = curl_cffi.requests.get(f"https://text.pollinations.ai/hello")
    print(f"\033[38;5;220m[test_pollinations]\033[0m Response from Pollinations API: {response.text}")

def test_agent_class() : 
    print(f"\033[38;5;220m[test_agent_class]\033[0m Testing...")
    agent = PandexAgent("test_1", None, config = test_agent_config_1)
    result = agent.execute(plan = {"vars" : {"prompt": "what is pollinations ai."}})
    print(f"\033[38;5;220m[test_agent_class]\033[0m Agent 1 execution result: {result}")
    agent = PandexAgent("test_2", None, config = test_agent_config_2)
    result = agent.execute(plan = {"vars" : {"prompt": "what is pollinations ai."}})
    print(f"\033[38;5;220m[test_agent_class]\033[0m Agent 2 execution result: {result}")

test_agent_config_3 = {
    "template": "[[PROMPT]] : [[REFERENCE]]",
    "executor": {
        "type": "api",
        "url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
        "api_key" : os.environ.get("DOUBAO_API_KEY", None),
        "data": {
            "model": "doubao-1-5-pro-32k-250115", 
            "prompt": "Hello world.", 
        },
    },
    "vars": {
        "prompt": {
            "type": "text",
            "default": "Hello world.",
        },
        "reference": {
            "type": "agent",
            "agent" : "test_2",
            "plan" : {"vals" : {"prompt" : "what is pollinations ai"}}, 
            "key" : "response",
            "default": "Everything is okay.",
        },
    },
}

test_hub_config = {
    "agents" : {
        "test_2" : test_agent_config_2,
        "test_3" : test_agent_config_3,
    },
}

def test_hub_class() : 
    print(f"\033[38;5;220m[test_hub_class]\033[0m Testing...")
    hub = PandexHub(config = test_hub_config)
    result = hub.agents["test_3"].execute(plan = {"vals" : {"prompt": "repeate the following"}})
    print(f"\033[38;5;220m[test_hub_class]\033[0m Agent 3 execution result: {result}")