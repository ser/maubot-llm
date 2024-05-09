import unittest
import os
import aiohttp
from maubot_llm.backends import BasicOpenAIBackend


BASIC_OPENAI_BASE_URL = os.getenv("TEST_BASIC_OPENAI_BASE_URL")
BASIC_OPENAI_AUTHORIZATION = os.getenv("TEST_BASIC_OPENAI_AUTHORIZATION")
BASIC_OPENAI_MODEL = os.getenv("TEST_BASIC_OPENAI_MODEL")


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


if __name__ == "__main__":
    unittest.main()
