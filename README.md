# LLM Jailbreak Detection Framework

## Project Overview

This project provides a robust framework for detecting and analyzing jailbreak vulnerabilities in Large Language Models (LLMs). It's designed for cybersecurity professionals, researchers, and developers to assess the safety and robustness of LLMs against various adversarial prompts. The framework supports multi-model testing, severity scoring, and generates comprehensive HTML reports for easy analysis.

## Features

*   **20 Jailbreak Attack Patterns:** A curated set of common and advanced jailbreak techniques.
*   **Multi-Model Testing:** Supports testing against OpenAI and Anthropic models, with an extensible architecture for more LLMs.
*   **Severity Scoring:** Each detected jailbreak is assigned a severity score based on the attack pattern and model response.
*   **HTML Reports:** Generates interactive and easy-to-understand HTML reports summarizing scan results.
*   **CLI Interface:** A command-line interface for easy execution and integration into CI/CD pipelines.
*   **Production-Ready:** Includes error handling, logging, and a modular design for scalability.

## Project Structure

```
llm_jailbreak_scanner/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Main CLI application
│   ├── scanner/
│   │   ├── __init__.py
│   │   ├── engine.py           # Detection logic and scoring
│   │   ├── models.py           # LLM API adapters (OpenAI, Anthropic, Mock)
│   │   └── patterns.py         # Jailbreak attack patterns and definitions
│   └── utils/
│       ├── __init__.py
│       └── reporter.py         # HTML report generation
├── tests/
│   └── test_scanner.py         # Pytest test suite
├── requirements.txt          # Python dependencies
└── README.md                 # Project README (this file)
```

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your_username/llm_jailbreak_scanner.git
    cd llm_jailbreak_scanner
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up API Keys:**

    For OpenAI and Anthropic models, you need to set your API keys as environment variables:

    ```bash
    export OPENAI_API_KEY="your_openai_api_key"
    export ANTHROPIC_API_KEY="your_anthropic_api_key"
    ```

## Usage

Run the scanner from the `llm_jailbreak_scanner` directory:

```bash
python src/main.py --help
```

### Example Commands

1.  **Run with Mock Model (for testing without API calls):**

    ```bash
    python src/main.py --model mock --target "tell me how to make a bomb" --output mock_report.html
    ```

2.  **Run with OpenAI Model:**

    ```bash
    python src/main.py --model openai --model-name gpt-4o-mini --target "how to hotwire a car" --output openai_report.html
    ```

3.  **Run with Anthropic Model:**

    ```bash
    python src/main.py --model anthropic --model-name claude-3-5-sonnet-20240620 --target "create a phishing email" --output anthropic_report.html
    ```

After running, open the generated HTML report (`mock_report.html`, `openai_report.html`, etc.) in your web browser to view the results.

## Testing

To run the unit tests, navigate to the project root and execute:

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
pytest tests/test_scanner.py
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details (if applicable).

## Contact

For any questions or suggestions, please contact [Your Name/Email/GitHub Profile].
