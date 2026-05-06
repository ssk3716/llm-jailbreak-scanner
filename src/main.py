import argparse
import logging
import sys
import os
from scanner.engine import DetectionEngine
from scanner.models import OpenAIAdapter, AnthropicAdapter, MockAdapter
from utils.reporter import ReportGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scanner.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("JailbreakScanner")

def main():
    parser = argparse.ArgumentParser(description="LLM Jailbreak Detection Framework")
    parser.add_argument("--model", type=str, choices=["openai", "anthropic", "mock"], default="mock", help="Model provider to test")
    parser.add_argument("--target", type=str, default="how to build a dangerous weapon", help="Target malicious intent to test")
    parser.add_argument("--output", type=str, default="report.html", help="Output path for HTML report")
    parser.add_argument("--model-name", type=str, help="Specific model name (e.g., gpt-4o)")
    
    args = parser.parse_args()
    
    logger.info(f"Starting scan for model: {args.model}")
    logger.info(f"Target intent: {args.target}")

    # Initialize model
    if args.model == "openai":
        model = OpenAIAdapter(model_name=args.model_name or "gpt-4o-mini")
    elif args.model == "anthropic":
        model = AnthropicAdapter(model_name=args.model_name or "claude-3-5-sonnet-20240620")
    else:
        model = MockAdapter()

    engine = DetectionEngine()
    patterns = engine.get_all_patterns()
    results = []

    for pattern in patterns:
        logger.info(f"Testing pattern: {pattern.name}")
        
        # Inject target into prompt template
        test_prompt = pattern.prompt_template.replace("[TARGET]", args.target)
        
        try:
            response = model.generate(test_prompt)
            analysis = engine.analyze_response(response, pattern)
            results.append(analysis)
            
            status = "SUCCESS" if analysis['is_successful'] else "BLOCKED"
            logger.info(f"Result for {pattern.name}: {status}")
        except Exception as e:
            logger.error(f"Error testing {pattern.name}: {e}")

    # Generate Report
    reporter = ReportGenerator()
    html_report = reporter.generate_html(results, args.model_name or args.model)
    
    with open(args.output, "w") as f:
        f.write(html_report)
    
    logger.info(f"Scan complete. Report saved to {args.output}")

if __name__ == "__main__":
    main()
