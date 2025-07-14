#  <img src="https://s2.loli.net/2025/07/14/8jSEN5PCqUoQv3x.png" alt="Minecraft AI" width="36" height="36"> PandexAgent: A Modular Agent Framework for Context Engineering with LLMs

PandexAgent is a flexible, JSON-configurable agent framework designed to help large language models (LLMs) manage context, chain tasks, and interact with tools more systematically. It enables the definition of nested prompt templates, structured outputs, and multi-agent collaboration through a lightweight configuration-first design.

## 🧠 What Is a PandexAgent?

A PandexAgent is a modular unit consisting of:

- a **template** prompt,
- an **executor** backend,
- an **output schema**,
- and a set of **input variables**.

Each variable can be a primitive (text, int, bool) or another agent’s output, allowing recursive compositions.


## ✨ Key Features

- **Prompt Composition & Nesting**: Modular prompt templates using `[[VARIABLE_NAME]]` placeholders.
- **Structured Output**: Supports `raw` or `json`-based outputs, making integration with tools like MCP seamless.
- **LLM-Editable**: Both individual agents and agent hubs are entirely configurable via JSON, enabling LLMs to create, modify, and chain agents.
- **Multi-Agent Hub**: Use `PandexHub` to coordinate multiple agents that can reference each other’s outputs.

## 🎮 Online Playground

We provide a web-based playground at:

👉 [Pandex Agent Playground](https://pandex-agent.vercel.app/)

![Pandex Agent Playground](https://s2.loli.net/2025/07/14/anY8QdHo9b1Rjrh.png)

This is a lightweight, interactive demo designed to preview how PandexAgent works. It allows you to experiment with prompt composition, nested variables, and structured outputs without setting up a local environment.

⚠️ Note: This playground is not optimized for production use. Responses may be delayed due to limited backend resources.

## 🧱 Origin & Community

PandexAgent is inspired by our work in the Minecraft AI project, where we build robust and extensible LLM agents to act as the cognitive core for in-game AI characters. These agents need to reason, reflect, and coordinate with others—driving the need for modular, prompt-driven architectures like PandexAgent.

We welcome collaboration, discussion, and ideas. Join us in the Minecraft AI Discord server to connect with our community and explore how PandexAgent and other tools are shaping AI in virtual environments.

💬 Join the Minecraft AI Discord

<a href="https://discord.gg/RKjspnTBmb" target="_blank"><img src="https://s2.loli.net/2025/04/18/CEjdFuZYA4pKsQD.png" alt="Official Discord Server" width="180" height="36"></a>

---

## 🧩 Agent Configuration Format

```json
{
  "template": "Say hello to [[NAME]] and explain [[TOPIC]].",
  "executor": {
    "type": "api",
    "url": "https://api.example.com/generate",
    "headers": { "Content-Type": "application/json" },
    "data": {}
  },
  "output": {
    "type": "json",
    "keys": {
      "response": {
        "type": "string",
        "description": "The generated text response"
      },
      "confidence": {
        "type": "float",
        "description": "Model confidence score"
      }
    }
  },
  "vars": {
    "name": {
      "type": "text",
      "default": "Alice"
    },
    "topic": {
      "type": "text",
      "default": "how the moon affects tides"
    }
  }
}
````

### Supported Variable Types

* `"text"`: Plain string
* `"int"` / `"float"` / `"bool"`: Primitive types
* `"agent"`: Reference to another agent’s result

---

## 🧠 What Is a PandexHub?

A `PandexHub` is a container for multiple named `PandexAgent`s. Agents in the hub can reference each other and be executed in any sequence.

### 🏗️ Hub Configuration Format

```json
{
  "agents": {
    "question": {
      "template": "What is [[TOPIC]]?",
      "executor": { "type": "pollinations" },
      "output": { "type": "json", "keys": {
        "response": { "type": "string", "description": "Answer to the topic" }
      }},
      "vars": {
        "topic": {
          "type": "text",
          "default": "quantum computing"
        }
      }
    },
    "summary": {
      "template": "Summarize: [[ANSWER]]",
      "executor": { "type": "pollinations" },
      "output": { "type": "raw" },
      "vars": {
        "answer": {
          "type": "agent",
          "agent": "question",
          "plan": { "vals": { "topic": "LLMs" } },
          "key": "response",
          "default": "Large Language Models are AI systems..."
        }
      }
    }
  }
}
```

---

## Examples

More examples will be added to `api/static/examples`.

---

## 🚀 Getting Started

```bash
git clone https://github.com/your-username/pandex-agent.git
cd pandex-agent
python agent.py  # Run with custom config
```

You can load your own JSON config or define agents programmatically.

---

## 📚 Use Cases

* Context-aware LLM prompt construction
* Tool-augmented agent decision pipelines
* Autonomous multi-agent simulations
* Planning, summarization, reasoning chains

---

## 🛠 Roadmap

* [ ] Native YAML/DSL to JSON transpiler
* [ ] Visual agent config editor (in-browser)
* [ ] WebSocket support for real-time tool calls
* [ ] HuggingFace Transformers backend integration
* [ ] Enhanced LLM prompts for self-building agents

---

## 🤝 Contributing

Pull requests and ideas are welcome! You can also contribute by:

* Creating new `executor` types (e.g., OpenAI, local models)
* Sharing real-world config examples
* Improving JSON schemas or documentation

---

*Build agents that build agents.*

