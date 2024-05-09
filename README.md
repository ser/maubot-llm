This is a very basic [maubot](https://github.com/maubot/maubot) plugin for invoking LLMs.

It's very new and very rough.
Use at your own risk, and expect problems.

The LLM must be supplied by an OpenAI-compatible server.
For example, if you run [LM Studio](https://lmstudio.ai/), this plugin can connect to its server.

You can and probably should configure it to only respond to messages from specific users.

# Installation

- [Setup maubot](https://docs.mau.fi/maubot/usage/setup/index.html)
- Clone this repo and [use `mbc build -u`](https://docs.mau.fi/maubot/usage/cli/build.html) to build the plugin
- [Create a client and an instance](https://docs.mau.fi/maubot/usage/basic.html)
- Update the configuration; see [base-config.yaml](base-config.yaml) for documentation of the available options

# Usage

Once it's added to a room, every message from any user on the allowlist will cause the bot to invoke the LLM and respond with its output.

You can configure multiple backends.
One of them should be designated as the default, but the bot can also use a different backend in each room.
You can also use different models and system prompts in different rooms.

The following commands are available for managing the bot in a room:

- To see the current backend, model, and system prompt, use `!llm info`.
- To change to a different backend, use `!llm backend KEY`, where KEY is the key from the `backends` map in the configuration.
- To use a specific model, use `!llm model NAME`. Currently the name is just passed directly as the `model` field in the request json when invoking the server.
- To change the system prompt, use `!llm system WRITE YOUR PROMPT HERE`.
- To clear the context (forget all past messages in the room), use `!llm clear`.

