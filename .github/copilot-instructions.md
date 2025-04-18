Your markdown content is well-structured and detailed, but there are areas where clarity, conciseness, and formatting can be improved. Here's the rewritten version:

# GitHub Copilot Instructions Template

This template provides a structure for guiding GitHub Copilot within your project. Customize the placeholders (`[...]`) to match your specific project details. For more on custom instructions, see [VS Code Custom Instructions](https://code.visualstudio.com/blogs/2025/03/26/custom-instructions).

---
## 🤖 Instructions: `[Project Name]` Project
---

**Summary:** Provide a brief overview of the project's purpose and technologies (e.g., "This project uses CrewAI to automate [specific process] by analyzing [input data type] and generating [output data type].").

### 📁 Project Structure

Explain the purpose of key files and directories. Replace placeholders with actual names.

* **`[Main Entry Point File]`**: (e.g., `src/main.py`) Entry point for the project. Loads configurations, starts the process, and handles inputs/outputs.
* **`[Crew Definition File]`**: (e.g., `src/crew.py`) Defines the Crew, agents, and task sequence.
* **`[Agent Config File]`**: (e.g., `src/config/agents.yaml`) Contains agent definitions (roles, goals, tools).
* **`[Task Config File]`**: (e.g., `src/config/tasks.yaml`) Defines tasks, expected outputs, and assigned agents.
* **`[Tools Directory]`**: (e.g., `src/tools/`) Contains custom tools for agents.
    * `[Custom Tool 1].py`: Brief description of the tool.
    * `[Custom Tool 2].py`: Brief description of the tool.
* **`[Input Directory/File]`**: (e.g., `input/`) Directory for input data.
* **`[Output Directory/File]`**: (e.g., `output/`) Directory for generated results.
* **`.env`**: Stores environment variables (e.g., API keys).
* **`pyproject.toml` / `requirements.txt`**: Project dependencies.

### 📁 Standard CrewAI Project Structure

```bash
src/<project_name>/
├── config/
│   ├── agents.yaml      
│   └── tasks.yaml       
├── crew.py              
├── main.py              
└── tools/
    └── <tool_name>.py   
```

### 🧠 Agents (`[Agent Config File]`)

List the agents and their roles, goals, and tools.

1. **`[Agent_1_Name]`**
     * **Role**: [Role Description] (e.g., Data Extractor)
     * **Goal**: [Specific Goal] (e.g., Extract key information from input files)
     * **Tool**: `[Tool_Name_Used_By_Agent_1]`

2. **`[Agent_2_Name]`**
     * **Role**: [Role Description] (e.g., Content Analyzer)
     * **Goal**: [Specific Goal] (e.g., Analyze extracted data against requirements)
     * **Tool**: `[Tool_Name_Used_By_Agent_2]`

3. **`[Agent_3_Name]`**
     * **Role**: [Role Description] (e.g., Report Generator)
     * **Goal**: [Specific Goal] (e.g., Generate a structured report based on analysis)
     * **Tool**: `[Tool_Name_Used_By_Agent_3]`

### 📝 Tasks (`[Task Config File]`)

Define the tasks and their expected outputs.

1. **`[Task_1_Name]`**
     * **Description**: [Detailed Task Description] (e.g., Extract data from input files).
     * **Expected Output**: [Output Format] (e.g., A dictionary with keys: 'data_point_1', 'data_point_2').
     * **Agent**: `[Agent_1_Name]`

2. **`[Task_2_Name]`**
     * **Description**: [Detailed Task Description] (e.g., Analyze extracted data for insights).
     * **Expected Output**: [Output Format] (e.g., A bullet-point summary of findings).
     * **Agent**: `[Agent_2_Name]`

3. **`[Task_3_Name]`**
     * **Description**: [Detailed Task Description] (e.g., Compile analysis results into a final report).
     * **Expected Output**: [Output Format] (e.g., A formatted Markdown file).
     * **Agent**: `[Agent_3_Name]`

### 🧰 Tools (`[Tools Directory]`)

Describe the tools used by agents.

* **`[Tool_Name_1]` (`[tool_1_file].py`)**:
    * **Description**: [What the tool does] (e.g., Reads data from a specific API).
    * **How it works**: Briefly explain the mechanism (e.g., Uses `requests` to fetch data).

* **`[Tool_Name_2]` (`[tool_2_file].py`)**:
    * **Description**: [What the tool does] (e.g., Parses text from a specific file format).
    * **How it works**: Briefly explain the mechanism (e.g., Uses `[library_name]` to process files).

### ⚙️ Crew Flow (`[Crew Definition File]`, `[Main Entry Point File]`)

1. **Configuration (`[Crew Definition File]`)**: Set up the Crew with agents and tasks from YAML files. Use `Process.sequential` or other processes as needed.
2. **Execution (`[Main Entry Point File]`)**:
     * Load environment variables.
     * Configure the LLM API.
     * Start the Crew with `crew.kickoff(inputs={...})`.
     * Print and save the result.

### 🧩 Dependencies (`pyproject.toml` / `requirements.txt`)

List main dependencies (e.g., `crewai`, `crewai-tools`, `python-dotenv`, `[specific libraries for tools]`). Use `uv` or `pip` for management.

### ⚙️ Configuration (`.env`)

List required environment variables (e.g., `LLM_API_KEY`, `MODEL_NAME`).

---
## 🤖 General and Copilot Instructions: CrewAI Framework
---

**Summary:** CrewAI ([Official Documentation](https://docs.crewai.com/)) orchestrates autonomous AI agents collaborating on tasks. See [VS Code Custom Instructions](https://code.visualstudio.com/blogs/2025/03/26/custom-instructions) for more.

### 📚 Core CrewAI Concepts

* **Agents:** Entities with `role`, `goal`, `tools`, and `memory`.
* **Tasks:** Actions agents perform, defined by `description` and `expected_output`.
* **Tools:** Python functions with the `@tool` decorator for external interactions.
* **Crew:** Orchestrates agent collaboration and task execution.

### 💡 How Copilot Should Help

* Suggest agent roles, goals, and backstories.
* Propose task descriptions and outputs.
* Assist in tool implementation and usage.
* Validate YAML structure.
* Troubleshoot CrewAI errors and suggest best practices.

---
## ⚡ Instructions: `uv` Package Manager
---

**Summary:** `uv` ([Official Documentation](https://astral.sh/uv)) is a fast Python package and project manager.

### Key Commands

*   `uv init`          # Create `pyproject.toml`
*   `uv add <package>` # Add dependency
*   `uv sync`          # Install dependencies
*   `uv venv`          # Create/reuse virtual environment
*   `uv run <command>` # Run in venv


---
## 🔄 Instructions for Updating Copilot's Internal Documentation
---

**Objective:** Keep this file updated with the latest best practices for CrewAI, `uv`, and your project.

### Update Process

1. Read this file.
2. Identify technologies used.
3. Search for recent documentation and compare.
4. Update sections as needed.
5. Optionally, add a note about the date and versions checked.

---
## 🔄 Instructions: Automatic Commits (Suggestion)
---

**Objective:** Maintain a clear history of changes.

### Suggested Commit Message Format

1. **Prefix:** `[CrewAI]`, `[Tool]`, `[Config]`, `[Docs]`, `[Refactor]`, `[Fix]`, `[Feat]`.
2. **Description:** Clear and concise.
3. **Body (Optional):** Additional details.

---

This version improves readability, removes redundancy, and ensures clarity while maintaining all essential details.
