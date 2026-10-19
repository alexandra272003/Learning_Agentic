# Groq API Chatbot

A beginner-friendly Python project that demonstrates how to integrate the Groq API with a command-line chatbot using a large language model (LLM).

This project is part of my learning journey in Python, API integration, prompt engineering, and Generative AI, progressing toward agentic AI development.

## Overview

The chatbot accepts text prompts, sends them to a language model through the Groq API, and displays the generated responses.

As the project evolves, it explores reusable prompt functions, sentiment analysis, structured JSON responses, data validation, and iterative LLM workflows.

The goal is to understand how to build reliable Python applications powered by LLMs and gradually develop agentic AI capabilities.

## Features

- Integration with the Groq API.
- Command-line prompt input.
- AI-generated text responses.
- Environment variables for API configuration.
- Configurable language model.
- Dependency management using `uv`.
- Environment configuration using `python-dotenv`.
- Reusable functions for repeated LLM calls.
- Product review sentiment analysis.
- Structured JSON output from an LLM.
- JSON parsing and validation.
- Pydantic-based response validation.
- Iterative LLM calls for multi-step problem-solving.
- Conversation history for passing previous responses into subsequent steps.

## Tech Stack

- **Python** — application logic.
- **Groq API** — language model inference.
- **Groq Python SDK / OpenAI-compatible SDK** — API integration.
- **uv** — dependency and virtual environment management.
- **python-dotenv** — environment configuration.
- **JSON** — structured LLM responses.
- **Pydantic** — data validation and type checking.

## Prerequisites

- A compatible Python version.
- `uv` installed.
- A valid Groq API key.
- Basic knowledge of Python functions, lists, dictionaries, and API calls.

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
```

Replace the placeholders with your GitHub repository URL and directory name.

### 2. Configure environment variables

Copy `.env.example` to `.env`.

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
```

**Linux/macOS**

```bash
cp .env.example .env
```

Add your configuration to `.env`:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

Replace the API key placeholder with your own key. Confirm that the configured model is available to your Groq account.

### 3. Install dependencies

```bash
uv sync
```

Make sure the dependencies used by your scripts are declared in `pyproject.toml`.

## Usage

### Basic chatbot

Run the chatbot with a custom prompt:

```bash
uv run main.py "Explain cosine similarity in simple words"
```

### Sentiment analysis

Use a reusable function to classify product reviews:

```python
analyze_review("This product is excellent!")
```

The LLM is prompted to return:

- `sentiment` — positive, negative, or neutral.
- `confidence` — a score between `0.0` and `1.0`.
- `reason` — a short explanation.

### Structured output

Parse the LLM's JSON response:

```python
import json

parsed = json.loads(raw_reply)
print(type(parsed))
```

The result is normally a Python dictionary when the JSON contains an object.

### Pydantic validation

Validate the response against a defined schema:

```python
from pydantic import BaseModel, Field
from typing import Literal

class SentimentResult(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str
```

Validate parsed data:

```python
result = SentimentResult.model_validate(parsed)
print(result)
```

This checks the expected fields, types, allowed sentiment values, and confidence range.

### Iterative LLM workflow

The multi-step mathematics exercise asks the LLM to solve a problem one step at a time.

The workflow:

1. Send the original question.
2. Display the model's response.
3. Append that response to the conversation history.
4. Send another request asking for the next step.
5. Continue until a final-answer condition is detected.

This demonstrates iterative LLM calls and conversation-state management.

## How It Works

1. Load environment variables.
2. Read the user's prompt or review.
3. Construct a system prompt that defines the task.
4. Send messages to the selected model through the Groq API.
5. Receive the generated response.
6. Parse and validate structured responses when required.
7. Display the result or pass it into the next processing step.

## Learning Progression

### 1. API Integration

- Connecting Python to the Groq API.
- Sending prompts to an LLM.
- Receiving and displaying generated responses.
- Selecting a model using environment variables.

### 2. Prompt Engineering

- Writing system and user prompts.
- Defining clear output instructions.
- Using few-shot examples.
- Controlling response generation with supported API parameters.

### 3. Reusable LLM Functions

- Creating functions such as `analyze_review()`.
- Passing different strings or reviews as arguments.
- Reusing the same prompt and API configuration.
- Reducing repeated code.

### 4. Sentiment Analysis

- Classifying product reviews as positive, negative, or neutral.
- Asking the LLM to provide a confidence score.
- Requesting a short explanation for the classification.
- Using prompts to define a consistent output format.

**Important:** An LLM-generated confidence score is an estimate unless it is independently calibrated.

### 5. Structured JSON Output

- Instructing the LLM to return JSON only.
- Using `json.loads()` to parse JSON strings.
- Understanding the difference between a JSON string and a Python dictionary.
- Handling malformed JSON with `json.JSONDecodeError`.

### 6. Pydantic Validation

- Defining a data model with `BaseModel`.
- Using `Literal` to restrict allowed sentiment values.
- Using `Field` to set minimum and maximum confidence values.
- Validating parsed dictionaries with `model_validate()`.
- Detecting invalid response data with validation errors.

JSON parsing checks syntax; Pydantic checks whether the parsed data matches the defined model.

### 7. Iterative LLM Calls

- Making repeated calls to an LLM.
- Appending assistant responses to conversation history.
- Using earlier responses as context for later calls.
- Asking the model to produce one calculation or step per response.
- Stopping when a final-answer condition is detected.

### 8. Chain-of-Thought-Style Step Processing

- Providing examples to guide the model's response format.
- Breaking grade-school mathematics problems into explicit steps.
- Passing previous results into subsequent calls.
- Printing each response as it is generated.
- Understanding that the model may still combine steps or fail to follow instructions consistently.

This exercise requests concise, visible reasoning steps rather than private internal reasoning.

## Stateless vs. Stateful Workflows

### Stateless requests

Each request is independent. Previous prompts and responses are not automatically remembered.

### Stateful conversations

A conversation history is maintained and included in subsequent API calls. This allows the model to use earlier messages as context.

The iterative mathematics exercise is a simple example of a stateful LLM workflow.

## Configuration

| Variable | Purpose |
|---|---|
| `GROQ_API_KEY` | Authenticates API requests |
| `GROQ_MODEL` | Selects the language model |

Model availability depends on the models supported by Groq and the access available to your account.

Model documentation: https://console.groq.com/docs/models

## Security

- Never upload `.env` to GitHub.
- Add `.env` to `.gitignore`.
- Keep API keys out of source code.
- Revoke and replace any exposed API key.
- Share `.env.example` with placeholder values.
- Avoid logging API keys or other secrets.

## Possible Improvements

- Interactive multi-turn chatbot.
- Streaming responses.
- Better error handling and retry logic.
- Unit tests using mocked API calls.
- Strict structured outputs using JSON Schema.
- Improved handling of invalid JSON.
- Pydantic validation and error recovery.
- Reusable prompt templates.
- Configurable stopping conditions and iteration limits.
- Tool calling.
- External tools such as calculators and search.
- Agent workflows that select and execute tools.
- Logging and tracing of LLM calls.
- Evaluation of response quality and reliability.

## Learning Project

This repository documents my practical learning journey with Python, API integration, prompt engineering, structured LLM outputs, and iterative workflows.

The current exercises establish a foundation for agentic AI. Future improvements will focus on tool use, controlled execution, evaluation, and more autonomous task completion.
