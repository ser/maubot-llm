import unittest
import os
import aiohttp
from maubot_llm.backends import BasicOpenAIBackend, OpenAIBackend


BASIC_OPENAI_BASE_URL = os.getenv("TEST_BASIC_OPENAI_BASE_URL")
BASIC_OPENAI_AUTHORIZATION = os.getenv("TEST_BASIC_OPENAI_AUTHORIZATION")
BASIC_OPENAI_MODEL = os.getenv("TEST_BASIC_OPENAI_MODEL")
OPENAI_API_KEY = os.getenv("TEST_OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("TEST_OPENAI_MODEL", "gpt-4-turbo")


class TestBackends(unittest.IsolatedAsyncioTestCase):
    async def test_basic(self) -> None:
        if BASIC_OPENAI_BASE_URL is None:
            print("SKIPPING because TEST_BASIC_OPENAI_BASE_URL not configured")
            return
        backend = BasicOpenAIBackend(dict(base_url=BASIC_OPENAI_BASE_URL, authorization=BASIC_OPENAI_AUTHORIZATION))
        async with aiohttp.ClientSession() as http:
            context = [{"role": "user", "content": "Please say the word 'hello' in lowercase and nothing else."}]
            system = "You are a helpful digital assistant."
            completion = await backend.create_chat_completion(http, context=context, system=system, model=BASIC_OPENAI_MODEL)
            self.assertEqual(completion.message["role"], "assistant")
            self.assertRegex(completion.message["content"], r".*hello.*")
            self.assertEqual(completion.finish_reason, "stop")
    
    async def test_openai(self) -> None:
        if OPENAI_API_KEY is None:
            print("SKIPPING because TEST_OPENAI_API_KEY not configured")
        backend = OpenAIBackend(dict(api_key=OPENAI_API_KEY))
        async with aiohttp.ClientSession() as http:
            context = [{"role": "user", "content": "Please say the word 'hello' in lowercase and nothing else."}]
            completion = await backend.create_chat_completion(http, context=context, model=OPENAI_MODEL)
            self.assertEqual(completion.message["role"], "assistant")
            self.assertRegex(completion.message["content"], r".*hello.*")
            self.assertEqual(completion.finish_reason, "stop")

if __name__ == "__main__":
    unittest.main()
