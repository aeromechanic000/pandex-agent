
import curl_cffi
from agent import PandexAgent, PandexHub

test_agent_config_1 = {
    "template": "[[PROMPT]]",
    "executor": {
        "type": "api",
        "url": "https://text.pollinations.ai/openai",
        "headers": {"Content-Type" : "application/json"},
        "data": {"model": "deepseek", "prompt": "Hello world."},
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
        "type": "api",
        "url": "https://text.pollinations.ai/openai",
        "headers": {"Content-Type" : "application/json"},
        "data": {"model": "deepseek", "prompt": "Hello world."},
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
    response = curl_cffi.requests.get(f"https://text.pollinations.ai/hello")
    print(f"[test_pollinations] Response from Pollinations API: {response.text}")

def test_agent_class() : 
    print("[test_agent_class] Testing...")
    agent = PandexAgent("test_1", None, config = test_agent_config_1)
    result = agent.execute(plan = {"vars" : {"prompt": "what is pollinations ai."}})
    print(f"[test_agent_class] Agent 1 execution result: {result}")
    agent = PandexAgent("test_2", None, config = test_agent_config_2)
    result = agent.execute(plan = {"vars" : {"prompt": "what is pollinations ai."}})
    print(f"[test_agent_class] Agent 2 execution result: {result}")

test_agent_config_3 = {
    "template": "[[PROMPT]] : [[reference]]",
    "executor": {
        "type": "api",
        "url": "https://text.pollinations.ai/openai",
        "headers": {"Content-Type" : "application/json"},
        "data": {"model": "deepseek", "prompt": "Hello world."},
    },
    "vars": {
        "prompt": {
            "type": "text",
            "default": "Hello world.",
        },
        "refenrece": {
            "type": "agent",
            "agent" : "test_2",
            "plan" : {"input" : "", "vals" : {"prompt" : "what is pollinations ai"}}, 
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
    print("[test_hub_class] Testing...")
    hub = PandexHub(config = test_hub_config)
    result = hub.agents["test_3"].execute(plan = {"vars" : {"prompt": "repeate the following"}})
    print(f"[test_hub_class] Agent 3 execution result: {result}")