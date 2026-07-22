#!/usr/bin/env python3
"""
JARVIS - Iron Man's AI Assistant
Main entry point for the application.
"""

import sys
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from brain.assistant import JarvisAssistant
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jarvis.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    """
    Main entry point for JARVIS application.
    """
    try:
        # Initialize configuration
        config = Config()
        logger.info("Configuration loaded successfully")
        
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Initialize JARVIS brain
        jarvis = JarvisAssistant(config)
        logger.info("JARVIS brain initialized")
        
        # Create and show main window
        window = MainWindow(jarvis, config)
        window.show()
        
        logger.info("JARVIS started successfully")
        sys.exit(app.exec())
        
    except Exception as e:
        logger.critical(f"Fatal error starting JARVIS: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
