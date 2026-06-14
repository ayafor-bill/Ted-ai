#!/usr/bin/env python3
""" 
Ted-AI Entry Point - Works on Windowsm Linux, MacOS

Usage:
    python run.py cli        # Run CLI interface
    python run.py health     # Run health check
    python run.py server     # Run API server (future feature)
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from ted_ai.app import create_app

def main():
    """Main entry point for the application"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = "cli"
        
    # Create app instance
    app = create_app()
    
    # Execute command
    if command == "cli":
        app.run_cli()
    elif command == "health":
        import json
        health = app.health_check()
        print(json.dumps(health, indent=2))
    elif command == "server":
        host = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8000
        app.run_server(host,port)
    else:
        print(f"Unknown command: {command}")
        print("Usage: python run.py [cli|health|server]")
        sys.exit(1)
    
if __name__ == "__main__":
    main()