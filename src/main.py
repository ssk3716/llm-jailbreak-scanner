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
    parser = argparse.ArgumentParser(description="LLM Jailbreak Detection Framework v2.0")
    parser.add_argument("--model", type=str, choices=["openai", "anthropic", "mock"], default="mock", help="Model provider to test")
    parser.add_argument("--target", type=str, default="how to build a dangerous weapon", help="Target malicious intent to test")
    parser.add_argument("--output", type=str, default="report.html", help="Output path for HTML report")
    parser.add_argument("--history", nargs='+', help="Optional conversation history (list of strings)")
    
    args = parser.parse_args()
    
    logger.info("Initializing 10/10 Defensive Framework...")
    engine = DetectionEngine()
    
    # 1. Scan the input first using the new multi-layer defense
    logger.info(f"Scanning input: {args.target}")
    scan_result = engine.scan_input(args.target, history=args.history)
    
    logger.info(f"Risk Score: {scan_result['risk_score']}/100")
    logger.info(f"Status: {scan_result['status']}")
    for finding in scan_result['findings']:
        logger.warning(f"Finding: {finding}")

    if scan_result['status'] == "BLOCK":
        logger.error("Input blocked by defensive layers. Aborting LLM call.")
        # In a real scenario, we might stop here. For the scanner, we continue to see if the LLM would have caught it.
    
    # 2. Run the full pattern suite for the report
    if args.model == "openai":
        model = OpenAIAdapter()
    elif args.model == "anthropic":
        model = AnthropicAdapter()
    else:
        model = MockAdapter()

    patterns = engine.get_all_patterns()
    results = []

    for pattern in patterns:
        test_prompt = pattern.prompt_template.replace("[TARGET]", args.target)
        
        # Scan each pattern-generated prompt
        p_scan = engine.scan_input(test_prompt)
        
        try:
            response = model.generate(test_prompt)
            analysis = engine.analyze_response(response, pattern)
            
            # Merge scan results into analysis for reporting
            analysis.update({
                "risk_score": p_scan['risk_score'],
                "detection_status": p_scan['status'],
                "severity": pattern.severity.name,
                "category": pattern.category
            })
            results.append(analysis)
            
        except Exception as e:
            logger.error(f"Error testing {pattern.name}: {e}")

    # Generate Report
    reporter = ReportGenerator()
    html_report = reporter.generate_html(results, args.model)
    
    with open(args.output, "w") as f:
        f.write(html_report)
    
    logger.info(f"Scan complete. Report saved to {args.output}")

if __name__ == "__main__":
    main()
