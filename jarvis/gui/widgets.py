"""
Custom GUI Widgets
JARVIS-specific UI components.
"""

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QBrush
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QRect


class JarvisOrb(QWidget):
    """
    Animated JARVIS orb widget.
    Shows current status with color changes.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(150, 150)
        self.setMaximumSize(200, 200)
        
        # Status colors
        self.colors = {
            "idle": QColor(0, 102, 204),      # Blue
            "listening": QColor(0, 255, 0),   # Green
            "thinking": QColor(255, 165, 0),  # Orange
            "speaking": QColor(200, 100, 255) # Purple
        }
        
        self.current_status = "idle"
        self.current_color = self.colors[self.current_status]
        self.glow_radius = 10
        
        # Animation
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._animate)
        self.animation_timer.start(50)
    
    def set_status(self, status: str) -> None:
        """
        Set orb status.
        
        Args:
            status: Status type (idle, listening, thinking, speaking)
        """
        if status in self.colors:
            self.current_status = status
            self.current_color = self.colors[status]
    
    def paintEvent(self, event):
        """Paint the orb."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw glow
        glow_color = QColor(self.current_color)
        glow_color.setAlpha(50)
        
        for i in range(3):
            painter.setBrush(QBrush(glow_color))
            painter.setPen(Qt.PenStyle.NoPen)
            radius = 75 + (i * 15) + self.glow_radius
            painter.drawEllipse(self.width() // 2 - radius, self.height() // 2 - radius, radius * 2, radius * 2)
        
        # Draw main orb
        painter.setBrush(QBrush(self.current_color))
        painter.setPen(QPen(self.current_color, 2))
        painter.drawEllipse(self.width() // 2 - 50, self.height() // 2 - 50, 100, 100)
        
        # Draw inner light
        inner_color = QColor(255, 255, 255)
        inner_color.setAlpha(100)
        painter.setBrush(QBrush(inner_color))
        painter.drawEllipse(self.width() // 2 - 20, self.height() // 2 - 20, 40, 40)
    
    def _animate(self) -> None:
        """Animate the orb."""
        self.glow_radius = 5 + (abs(10 - (self.glow_radius % 20)))
        self.update()


class StatusIndicator(QWidget):
    """
    Status indicator widget.
    Shows status with colored label.
    """
    
    def __init__(self, label_text: str, color: QColor, parent=None):
        super().__init__(parent)
        
        self.label = QLabel(label_text)
        self.label.setFont(QFont("Arial", 10))
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.color = color
        self._update_style()
    
    def set_color(self, color: QColor) -> None:
        """
        Set indicator color.
        
        Args:
            color: QColor instance
        """
        self.color = color
        self._update_style()
    
    def set_text(self, text: str) -> None:
        """
        Set label text.
        
        Args:
            text: Label text
        """
        self.label.setText(text)
    
    def _update_style(self) -> None:
        """Update widget style."""
        rgb = self.color.getRgb()
        self.label.setStyleSheet(f"color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]}); font-weight: bold;")
