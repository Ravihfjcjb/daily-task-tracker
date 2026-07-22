"""
Animation Systems
Smooth animations for JARVIS UI.
"""

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QColor


class OrbAnimation:
    """
    Manages orb animations.
    """
    
    @staticmethod
    def create_glow_animation(widget, duration: int = 1000):
        """
        Create glow animation.
        
        Args:
            widget: Target widget
            duration: Animation duration in ms
            
        Returns:
            Animation object
        """
        animation = QPropertyAnimation(widget, b"color")
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        return animation
    
    @staticmethod
    def create_pulse_animation(widget, duration: int = 500):
        """
        Create pulse animation.
        
        Args:
            widget: Target widget
            duration: Animation duration in ms
            
        Returns:
            Animation object
        """
        animation = QPropertyAnimation(widget, b"scale")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(1.1)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        return animation
