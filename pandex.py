import argparse
import json
import os, sys
sys.path.append("api")
from index import app

def load_config(config_path):
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file '{config_path}' not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}")
        return None

def test(config = None):
    import test 
    print("Running tests...")
    if config:
        print(f"Using config: {config}")
    for func in [
        test.test_pollinations, 
        test.test_agent_class, 
        test.test_hub_class,
    ] :
        try : 
            func()
        except Exception as e:
            print(f"Error during test {func.__name__}: {e}")

def server(config = None):
    app.run(debug=True, host='0.0.0.0', port=3333)

def main():
    parser = argparse.ArgumentParser(description="Pandex - A versatile tool")
    parser.add_argument(
        "command", 
        choices=["test", "server",],
        help="Command to run: test, or server"
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Path to configuration JSON file"
    )
    
    args = parser.parse_args()
    
    # Load config if provided
    config = None
    if args.config:
        config = load_config(args.config)
        if config is None:
            return  # Exit if config loading failed
    
    # Execute the appropriate command
    if args.command == "test":
        test(config)
    elif args.command == "server":
        server(config)

if __name__ == "__main__":
    main()