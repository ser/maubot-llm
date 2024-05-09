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
    async def create_chat_completion(self, http: ClientSession,  context: List[dict], system: Optional[str], model: Optional[str]) -> ChatCompletion:
        raise NotImplementedError()


class BasicOpenAIBackend(Backend):
    def __init__(self, *, base_url: str, authorization: Optional[str]) -> None:
        self.base_url = base_url
        self.authorization = authorization
    
    async def create_chat_completion(self, http: ClientSession,  context: List[dict], system: Optional[str], model: Optional[str]) -> ChatCompletion:
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
