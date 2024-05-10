from typing import List, Optional
from aiohttp import ClientSession


class ChatCompletion:
    def __init__(self, message: dict, finish_reason: str, model: Optional[str]) -> None:
        self.message = message
        self.finish_reason = finish_reason
        self.model = model
    
    def __eq__(self, other) -> bool:
        return self.message == other.message and self.finish_reason == other.finish_reason and self.model == other.model


class Backend:
    def __init__(self, cfg: dict) -> None:
        self.cfg = cfg
        self.default_model = cfg.get("default_model")
        self.default_system_prompt = cfg.get("default_system_prompt")

    async def create_chat_completion(self, http: ClientSession,  context: List[dict], system: Optional[str] = None, model: Optional[str] = None) -> ChatCompletion:
        raise NotImplementedError()
    
    async def fetch_models(self, http: ClientSession) -> List[str]:
        raise NotImplementedError()


class BasicOpenAIBackend(Backend):
    def __init__(self, cfg) -> None:
        super().__init__(cfg)
        self.base_url = cfg["base_url"]
        self.authorization = cfg["authorization"]
    
    async def create_chat_completion(self, http: ClientSession,  context: List[dict], system: Optional[str] = None, model: Optional[str] = None) -> ChatCompletion:
        url = f"{self.base_url}/v1/chat/completions"
        reqbody = {"messages": context}
        if system is not None:
            reqbody["messages"].insert(0, {"role": "system", "content": system})
        if model is not None:
            reqbody["model"] = model
        headers = {}
        if self.authorization is not None:
            headers["Authorization"] = self.authorization
        async with http.post(url, headers=headers, json=reqbody) as resp:
            # TODO error handling
            respbody = await resp.json()
            choice = respbody["choices"][0]
            return ChatCompletion(
                message=choice["message"],
                finish_reason=choice["finish_reason"],
                model=choice.get("model", None)
            )
    
    async def fetch_models(self, http: ClientSession) -> List[str]:
        url = f"{self.base_url}/v1/models"
        headers = {}
        if self.authorization is not None:
            headers["Authorization"] = self.authorization
        async with http.get(url, headers=headers) as resp:
            # TODO error handling
            respbody = await resp.json()
            return [m["id"] for m in respbody["data"]]


class OpenAIBackend(BasicOpenAIBackend):
    def __init__(self, cfg) -> None:
        cfg["authorization"] = f"Bearer {cfg['api_key']}"
        if cfg.get("base_url") is None:
            cfg["base_url"] = "https://api.openai.com"
        super().__init__(cfg)


class AnthropicBackend(Backend):
    def __init__(self, cfg) -> None:
        super().__init__(cfg)
        self.base_url = cfg.get("base_url", "https://api.anthropic.com")
        self.api_key = cfg["api_key"]
        self.max_tokens = cfg["max_tokens"]

    async def create_chat_completion(self, http: ClientSession,  context: List[dict], system: Optional[str] = None, model: Optional[str] = None) -> ChatCompletion:
        url = f"{self.base_url}/v1/messages"
        reqbody = {"messages": context}
        if system is not None:
            reqbody["system"] = system
        if model is not None:
            reqbody["model"] = model
        reqbody["max_tokens"] = self.max_tokens
        headers = {}
        headers["anthropic-version"] = "2023-06-01"
        headers["x-api-key"] = self.api_key
        async with http.post(url, headers=headers, json=reqbody) as resp:
            # TODO error handling
            respbody = await resp.json()
            text = "\n\n".join(c["text"] for c in respbody["content"])
            return ChatCompletion(
                message=dict(role="assistant", content=text),
                finish_reason=respbody["stop_reason"],
                model=respbody["model"]
            )
