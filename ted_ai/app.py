"""
Ted-AI Main Application Module

Entry point and configuration management for the Ted-AI system.
"""

import os
import sys
import logging
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class AppConfig:
    """Application configuration"""
    
    # Database settings
    database_path: str = "ted_ai.db"
    echo_sql: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    
    # AI Model settings
    ai_model: str = "qwen3.5:9b"     # FOR EDITORS: You cound use any llm you think would be good for this part
    reasoning_model: str = "qwen3.5:8b"
    api_endpoint: str = "http://localhost:11434"     # Ollama endpoint
    api_key: Optional[str] = None
    
    # Application settings
    debug_mode: bool = False
    log_level: str = "INFO"
    data_dir: str = "ted_ai_data"
    cache_dir: str = "ted_ai_cache"
    
    # Feature flags
    enable_research_layer: bool = True
    enable_auto_analysis: bool = True
    auto_analysis_interval: int = 3600  # seconds
    
    def get_db_path(self) -> str:
        """Get database path (cross-platform)"""
        return str(Path(self.database_path).resolve())
    
    def get_data_dir(self) -> str:
        """Get data directory (cross-platform)"""
        return Path(self.data_dir).resolve()
    
    def get_cache_dir(self) -> str:
        """Get cache directory (cross-platform)"""
        return Path(self.cache_dir).resolve()

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load configuration from environment variables"""
        config = cls(
            database_path=os.getenv("TED_DB_PATH", "ted_ai.db"),
            echo_sql=os.getenv("TED_ECHO_SQL", "false").lower() == "true",
            ai_model=os.getenv("TED_AI_MODEL", "qwen3.5:9b"),
            reasoning_model=os.getenv("TED_REASONING_MODEL", "qwen3.5:8b"),
            api_endpoint=os.getenv("TED_API_ENDPOINT", "http://localhost:11434"),
            debug_mode=os.getenv("TED_DEBUG", "false").lower() == "true",
            log_level=os.getenv("TED_LOG_LEVEL", "INFO"),
        )
        return config
    
    def setup_directories(self):
        """Create necessary directories"""
        self.get_data_dir().mkdir(parents=True, exist_ok=True)
        self.get_cache_dir().mkdir(parents=True, exist_ok=True)
        logger.info(f"Directories setup: {self.get_data_dir()}, {self.get_cache_dir()}")
        
    @classmethod
    def from_file(cls, config_path: str) -> "AppConfig":
        """Load configuration from JSON file"""
        config_path = Path(config_path)
        if not config_path.exists():
            logger.warning(f"Config file not found: {config_path}")
            return cls()
        
        try:
            with open(config_path, 'r') as f:
                config_dict = json.load(f)
            return cls(**config_dict)
        except Exception as e:
            logger.error(f"Error loading config: {str(e)}")
            return cls()
    
    def save(self, config_path: str):
        """Save configuration to JSON file"""
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, 'w') as f:
                json.dump(asdict(self), f, indent=2)
            logger.info(f"Config saved to {config_path}")
        except Exception as e:
            logger.error(f"Error saving config: {str(e)}")
    
    def setup_directories(self):
        """Create necessary directories"""
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Directories setup: {self.data_dir}, {self.cache_dir}")


class TEDApplication:
    """Main application controller"""
    
    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or AppConfig.from_env()
        self._setup_logging()
        self.config.setup_directories()
        self.logger = logging.getLogger(__name__)
        
        logger.info("Ted-AI application initialized")
        logger.info(f"Database: {self.config.database_path}")
        logger.info(f"AI Model: {self.config.ai_model}")
    
    def _setup_logging(self):
        """Configure application logging"""
        log_level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        
        # Update root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
        
        # Add file handler
        log_file = Path(self.config.data_dir) / "ted_ai.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        
        formatter = logging.Formatter(
            '%(asctime)s - [%(name)s] - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        root_logger.addHandler(file_handler)
        
        logger.info(f"Logging configured: level={self.config.log_level}, file={log_file}")
    
    def run_cli(self):
        """Run the interactive CLI interface"""
        from ted_ai.cli import TEDCLIInterface
        
        logger.info("Starting CLI interface")
        cli = TEDCLIInterface(db_path=self.config.database_path)
        cli.run()
    
    def run_server(self, host: str = "127.0.0.1", port: int = 8000):
        """Run the API server (future feature)"""
        logger.info(f"Starting API server on {host}:{port}")
        # Implementation for API server would go here
        raise NotImplementedError("API server not yet implemented")
    
    def health_check(self) -> Dict[str, Any]:
        """Check application health"""
        from database import DatabaseManager, DatabaseConfig
        
        health = {
            "status": "healthy",
            "components": {}
        }
        
        # Check database
        try:
            db_config = DatabaseConfig(db_path=self.config.database_path)
            db = DatabaseManager(db_config)
            engagements = db.get_all_engagements()
            health["components"]["database"] = {
                "status": "ok",
                "path": self.config.database_path,
                "engagements": len(engagements)
            }
            db.close()
        except Exception as e:
            health["components"]["database"] = {
                "status": "error",
                "message": str(e)
            }
            health["status"] = "degraded"
        
        # Check AI model availability
        try:
            # Would check actual model availability here
            health["components"]["ai_model"] = {
                "status": "ok",
                "model": self.config.ai_model
            }
        except Exception as e:
            health["components"]["ai_model"] = {
                "status": "error",
                "message": str(e)
            }
            health["status"] = "degraded"
        
        return health


def create_app(config: Optional[AppConfig] = None) -> TEDApplication:
    """Factory function to create TEDApplication"""
    if config is None:
        config = AppConfig.from_env()
    return TEDApplication(config)


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = "cli"
    
    # Create application
    app = create_app()
    
    # Execute command
    if command == "cli":
        app.run_cli()
    elif command == "health":
        health = app.health_check()
        print(json.dumps(health, indent=2))
    elif command == "server":
        host = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
        port = int(sys.argv[3]) if len(sys.argv) > 3 else 8000
        app.run_server(host, port)
    else:
        print(f"Unknown command: {command}")
        print("Available commands: cli, health, server")
        sys.exit(1)