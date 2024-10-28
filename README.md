This is a very basic [maubot](https://github.com/maubot/maubot) plugin for invoking LLMs.

It's very new and very rough.
Use at your own risk, and expect problems.

The LLM must be supplied by an OpenWebUI server API: https://openwebui.com/

You can and probably should configure it to only respond to messages from specific users.

# Installation

- [Setup maubot](https://docs.mau.fi/maubot/usage/setup/index.html)
- Clone this repo and [use `mbc build -u`](https://docs.mau.fi/maubot/usage/cli/build.html) to build the plugin
- [Create a client and an instance](https://docs.mau.fi/maubot/usage/basic.html)
- Update the configuration; see [base-config.yaml](base-config.yaml) for documentation of the available options

# Usage

Once it's added to a room, message from any user on the allowlist starting with !(check your config)
will cause the bot to invoke the LLM and respond with its output.

You can configure multiple back-ends.
One of them should be designated as the default, but the bot can also use a different
back-end in each room. You can also use different models and system prompts in different rooms.

The following commands are available for managing the bot in a room:

- To see the current back-end, model, and system prompt, along with a list of available models (note: not supported for Anthropic), use `!llm info`.
- To change to a different back-end, use `!llm backend KEY`, where KEY is the key from the `backends` map in the configuration.
- To use a specific model, use `!llm model NAME`. Currently the name is just passed directly as the `model` field in the request json when invoking the server.
- To change the system prompt, use `!llm system WRITE YOUR PROMPT HERE`.
- To clear the context (forget all past messages in the room), use `!llm clear`.

# Copyrights

The work is substantially based on code written by Jacob Williams and taken from https://github.com/brokensandals/maubot-llm/
