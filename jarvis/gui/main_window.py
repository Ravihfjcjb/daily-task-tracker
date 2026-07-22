"""
Main GUI Window
Futuristic Iron Man-inspired interface.
"""

import sys
import logging
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QStatusBar, QProgressBar
)
from PySide6.QtCore import Qt, QTimer, QSize, QThread, Signal
from PySide6.QtGui import QFont, QColor, QPalette
from gui.widgets import JarvisOrb, StatusIndicator
from gui.animations import OrbAnimation

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main JARVIS GUI window.
    """
    
    def __init__(self, jarvis, config):
        """
        Initialize main window.
        
        Args:
            jarvis: JARVIS assistant instance
            config: Configuration object
        """
        super().__init__()
        
        self.jarvis = jarvis
        self.config = config
        
        self._setup_ui()
        self._setup_styles()
        self._setup_connections()
        self._setup_timers()
    
    def _setup_ui(self) -> None:
        """Setup UI components."""
        self.setWindowTitle("JARVIS - AI Assistant")
        self.setGeometry(
            100, 100,
            self.config.ui.window_width,
            self.config.ui.window_height
        )
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header with orb
        header_layout = QHBoxLayout()
        
        # JARVIS Orb
        self.orb = JarvisOrb()
        header_layout.addWidget(self.orb)
        
        # Status indicators
        status_layout = QVBoxLayout()
        
        self.mode_label = QLabel("ONLINE MODE")
        self.mode_label.setFont(QFont("Arial", 12, QFont.Bold))
        status_layout.addWidget(self.mode_label)
        
        self.internet_indicator = StatusIndicator("Internet: ON", QColor(0, 255, 0))
        status_layout.addWidget(self.internet_indicator)
        
        self.listening_indicator = StatusIndicator("Microphone: OFF", QColor(100, 100, 100))
        status_layout.addWidget(self.listening_indicator)
        
        header_layout.addLayout(status_layout)
        main_layout.addLayout(header_layout)
        
        # Conversation display
        self.conversation_display = QTextEdit()
        self.conversation_display.setReadOnly(True)
        self.conversation_display.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #00ff00;
                border: 2px solid #0066cc;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Courier New';
            }
        """)
        main_layout.addWidget(self.conversation_display)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(60)
        self.input_field.setPlaceholderText("Type or say something...")
        self.input_field.setStyleSheet("""
            QTextEdit {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 2px solid #0066cc;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        input_layout.addWidget(self.input_field)
        
        self.send_button = QPushButton("Send")
        self.send_button.setMaximumWidth(100)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0066cc;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
        """)
        input_layout.addWidget(self.send_button)
        
        main_layout.addLayout(input_layout)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        self.cpu_label = QLabel("CPU: 0%")
        self.ram_label = QLabel("RAM: 0%")
        self.time_label = QLabel()
        
        self.statusBar.addWidget(self.cpu_label)
        self.statusBar.addWidget(self.ram_label)
        self.statusBar.addPermanentWidget(self.time_label)
    
    def _setup_styles(self) -> None:
        """Setup application styles."""
        dark_stylesheet = """
            QMainWindow {
                background-color: #0a0a0a;
            }
            QLabel {
                color: #ffffff;
            }
        """
        self.setStyleSheet(dark_stylesheet)
    
    def _setup_connections(self) -> None:
        """Setup signal connections."""
        self.send_button.clicked.connect(self._on_send_clicked)
    
    def _setup_timers(self) -> None:
        """Setup update timers."""
        # Update system stats
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self._update_system_stats)
        self.stats_timer.start(1000)
        
        # Update time
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self._update_time)
        self.time_timer.start(1000)
    
    def _on_send_clicked(self) -> None:
        """Handle send button click."""
        text = self.input_field.toPlainText().strip()
        if text:
            self.input_field.clear()
            self._display_message("You", text)
            
            # Process in separate thread
            # Implementation would go here
    
    def _display_message(self, sender: str, message: str) -> None:
        """
        Display message in conversation.
        
        Args:
            sender: Message sender
            message: Message content
        """
        cursor = self.conversation_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        
        color = "#00ff00" if sender == "JARVIS" else "#0066cc"
        formatted_message = f'<span style="color: {color}"><b>{sender}:</b> {message}</span><br/>'
        
        cursor.insertHtml(formatted_message)
        self.conversation_display.ensureCursorVisible()
    
    def _update_system_stats(self) -> None:
        """Update system statistics."""
        try:
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=0.1)
            ram_percent = psutil.virtual_memory().percent
            
            self.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")
            self.ram_label.setText(f"RAM: {ram_percent:.1f}%")
        except Exception as e:
            logger.error(f"Error updating stats: {e}")
    
    def _update_time(self) -> None:
        """Update time display."""
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(current_time)
    
    def closeEvent(self, event):
        """Handle window close event."""
        logger.info("JARVIS window closing")
        event.accept()
