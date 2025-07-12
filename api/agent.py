
import re, os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from executor import * 

def split_content_and_json(text) :
    content, data = text, {}
    mark_pos = [m.start() for m in re.finditer("```", text)]
    for i in range(0, len(mark_pos) - 1) :
        data_start = mark_pos[i]
        data_end = mark_pos[i + 1]
        try :
            json_text = text[(data_start + 3) : data_end].replace("\n", "").replace("\r", "").strip()
            start = json_text.find("{")
            list_start = json_text.find("[")
            if list_start >= 0 and list_start < start :
                start = list_start
            if start >= 0 :
                json_text = json_text[start:]
            for tag in ["html", "css", "python", "javascript", "json", "xml"] :
                if json_text.find(tag) == 0 :
                    json_text = json_text[len(tag):].strip()
                    break
            data = json5.loads(json_text)
            content = text[:data_start].strip() + "\n" + text[min(len(text), data_end + 3):].strip()
        except Exception as e :
            content, data = text, {}
        if type(data) == dict and len(data) > 0 :
            break
    return content, data

class PandexAgent(object) :
    """
    A class representing a Pandex agent.
    """
    def __init__(self, name, hub, config = None):
        """
        Initialize the agent with a name and optional configuration.
        """
        self.name, self.hub = name, hub
        self.config = config or {
            "template" : "[[PROMPT]]",
            "executor" : {
                "type" : "api",
                "url" : None,
                "headers" : None,
                "data" : {},
            },
            "output" : {
                "type" : "json",
                "keys" : {
                    "content" : {
                        "type" : "string",
                        "description" : "content",
                    },
                    "status" : {
                        "type" : "int",
                        "description" : "status",
                    }, 
                    "decision" : {
                        "type" : "bool",
                        "description" : "decision",
                    }, 
                },
            },
            "vars" : {
                "prompt" : {
                    "type" : "text",
                    "default" : "Hello world.",
                }
            }
        }

        if "executor" in self.config.keys() :
            _type = self.config.get("executor", {}).get("type", None)
            if _type == "api" :
                self.executor = PandexAPIExecutor(self.config["executor"]) 
            else :
                print(f"Invalid executor config: {self.config['executor']}")
        else :
            print(f"Executor config is missing in agent {self.name}.")

        self.plan = {
            "input" : {
                "description" : "The text input to the agent's execution.",
                "value" : self.config.get("template", "[[PROMPT]]"),  
            },
            "vals" : {},
        }
        self.result = {
            "status" : -1,
            "output" : None,
            "error" : None,
        }
        print(f"Agent {self.name} initialized with config: {self.config}")

    def get_value(self, var) : 
        value = None
        if var in self.config.get("vars", {}).keys() :
            config = self.config.get("vars", {}).get(var, {})
            value = config.get("default", None)
            _type = config.get("type", "text")
            try : 
                if _type == "text" : 
                    value = str(value)
                elif _type == "int" : 
                    value = int(value)
                elif _type == "float" : 
                    value = float(value)
                elif _type == "bool" : 
                    value = bool(value)
                elif _type == "agent" : 
                    agent = self.hub.agents.get(config.get("agent", None), None) 
                    result = agent.execute(config.get("plan", {}))
                    key = config.get("key", None)
                    if key is not None and key in result.keys() :
                        value = result.get(key, "")
                    else : 
                        value = result.get("output", "")
            except Exception as e :
                print(f"Error getting value for variable '{var}': {e}")
                value = None
        return value

    def update(self, plan = None, refresh = True) :
        """
        Update values for the variables.
        """
        if plan is not None : 
            for var, value in plan.get("vars", {}).items() :
                self.plan["vals"][var] = value
        for var in self.config.get("vars", {}).keys() :
            if (plan is None or var not in self.plan.get("vals", {}).keys()) and (var not in self.plan["vals"].keys() or refresh == True) :
                self.plan["vals"][var] = self.get_value(var)
    
    def replace(self) :
        for var, value in self.plan["vals"].items() :
            if f"[[{var.upper()}]]" in self.plan["input"]["value"] :
                if isinstance(value, str) :
                    self.plan["input"]["value"] = self.plan["input"]["value"].replace(f"[[{var.upper()}]]", value)
                else : 
                    self.plan["input"]["value"] = self.plan["input"]["value"].replace(f"[[{var.upper()}]]", "")
        keys = self.config.get("output", {}).get("keys", {})
        if self.config.get("output", {}).get("type", "raw") == "json" and len("keys") > 0 :
            self.plan["input"]["value"] += '''
The result should be formatted in **JSON** dictionary and enclosed in **triple backticks (` ``` ` )**  without labels like 'json', 'css', or 'data'.
- **Do not** generate redundant content other than the result in JSON format.
- **Do not** use triple backticks anywhere else in your answer.
- The JSON must include the following keys and values accordingly :
'''
            for key in keys.keys() : 
                self.plan["input"]["value"] += f'''
    - '{key}' : value type is {keys[key]["type"]} {", " + keys[key]["description"] if len(keys[key]["description"].strip()) > 0 else "."} 
''' 

    def execute(self, plan) :
        """
        Execute the agent's main logic.
        """
        if self.executor is not None :
            print(f"Agent {self.name} is executed.")
            self.update(plan)
            self.replace()
            self.result = self.executor.process(self.plan)
            output_type = self.config.get("output", {}).get("type", "raw") 
            output_keys = self.config.get("output", {}).get("keys", {}) 
            if output_type == "json" and len(output_keys) > 0: 
                content, data = split_content_and_json(str(self.result.get("output", "")))
                self.result["output"], self.result["keys"] = content, {} 
                for key in output_keys.keys() :
                    if key in data.keys() :
                        if output_keys[key]["type"] == "int" :
                            self.result["keys"][key] = int(data[key])
                        elif self.config["output"]["keys"][key]["type"] == "float" :
                            self.result["keys"][key] = float(data[key])
                        elif self.config["output"]["keys"][key]["type"] == "bool" :
                            self.result["keys"][key] = bool(data[key])
                        elif self.config["output"]["keys"][key]["type"] == "string" :
                            self.result["keys"][key] = str(data[key])
                        else :
                            self.result["keys"][key] = data[key]
                    else :
                        self.result[key] = None
        else :
            print(f"Agent {self.name} cannot be executed without executor")
        return self.result

class PandexHub(object) :
    """
    A class representing a Pandex agnet hub.
    """
    def __init__(self, config):
        """
        Initialize the agent hub with the configuration.
        """
        self.config = config or {}
        self.status = []
        self.agents = {}
        for name, config in self.config.get("agents", {}).items():
            self.agents[name] = PandexAgent(name, self, config)
        print(f"Hub initialized with config: {self.config}")
    
    def add_status(self, status) : 
        self.status.append(f"{status}")
    
    def get_status(self) :
        return self.status