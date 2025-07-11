
import json5, curl_cffi, urllib.parse

class PandexExecutor(object) :
    """
    A class representing a Pandex agent executor.
    """
    def __init__(self, config = None):
        """
        Initialize the executor with a configuration.
        """
        self.config = config or {}
    
    def process(self, data = None) : 
        print("Processing data in PandexExecutor...")
        return {"status" : 0, "output" : ""} 

class PandexAPIExecutor(PandexExecutor) :
    """
    A class representing a Pandex agent executor to call a API.
    """
    def __init__(self, config = None):
        """
        Initialize the API executor with a configuration.
        """
        super().__init__(config)
        self.url = self.config.get("url", None)
        self.headers = self.config.get("headers", None)
        self.data = self.config.get("data", {})

    def process(self, data = None) : 
        result = {"status" : -1, "output" : None, "error" : None} 
        print("Processing data in PandexAPIExecutor...")

        if data is None : 
            data = self.data

        prompt = data.get("input", {}).get("value", self.data.get("prompt", "Response to 'Hello world', and add a reminder to the user to notice that this is the default prompt."))
        try :
            response = curl_cffi.requests.get(f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}")
            if response.status_code == 200 :
                result["output"] = response.text 
                if result["output"] is None : 
                    result["status"] = 1
                    result["error"] = f"Invalid response: {response}"
            else :
                result["status"] = 1
                result["error"] = f"Reponse error: {response.status_code}"
        except Exception as e :
            result["status"] = 2
            result["error"] = f"Exception: {e}"
        return result

class PandexPollinationsExecutor(PandexExecutor) :
    """
    A class representing a Pandex agent executor to call a API.
    """
    def __init__(self, config = None):
        """
        Initialize the Pollinations executor with a configuration.
        """
        super().__init__(config)
        self.url = self.config.get("url", None)
        self.headers = self.config.get("headers", None)
        self.data = self.config.get("data", {})

    def process(self, data = None) : 
        result = {"status" : -1, "output" : None, "error" : None} 
        print("Processing data in PandexAPIExecutor...")

        if data is None : 
            data = self.data

        payload = {
            "model" : data.get("model", self.data.get("model", None)), 
            "messages" : [{
                "role" : "user", 
                "content" : data.get("input", {}).get("value" , self.data.get("prompt", "Response to 'Hello world', and add a reminder to the user to notice that this is the default prompt.")),
            }],  
            "max_tokens" : data.get("max_tokens", self.data.get("max_tokens", 500)), 
            "temperature" : data.get("temperature", self.data.get("temperature", 0.7)),
            "stream" : False,
        }

        if "pollinations" in self.url.lower() :
            payload["private"] = True

        try :
            response = curl_cffi.requests.post(
                self.url,
                headers = self.headers or {"Content-Type" : "application/json"},
                json = payload,
            )
            if response.status_code == 200 :
                response_data = response.json() 
                if "choices" in response_data.keys() : 
                    if response_data["choices"][0]["message"].get("content", None) is not None : 
                        result["output"] = response_data["choices"][0]["message"]["content"]
                    elif response_data["choices"][0]["message"].get("reasoning_content", None) is not None : 
                        result["output"] = response_data["choices"][0]["message"]["reasoning_content"]
                if result["output"] is None : 
                    result["status"] = 1
                    result["error"] = f"Invalid response data: {response_data}"
            else :
                result["status"] = 1
                result["error"] = f"Reponse error: {response.status_code}"
        except Exception as e :
            result["status"] = 2
            result["error"] = f"Exception: {e}"
        return result


