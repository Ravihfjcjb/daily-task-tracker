"""
Calculator Skill
Handle natural language math calculations.
"""

import logging
import math
from typing import Optional

logger = logging.getLogger(__name__)


class CalculatorSkill:
    """
    Provides calculation capabilities.
    """
    
    def __init__(self, config):
        """
        Initialize calculator skill.
        
        Args:
            config: Configuration object
        """
        self.config = config
    
    async def evaluate(self, expression: str) -> Optional[float]:
        """
        Evaluate mathematical expression.
        
        Args:
            expression: Math expression
            
        Returns:
            Result or None
        """
        try:
            logger.info(f"Evaluating: {expression}")
            result = eval(expression, {"__builtins__": {}}, {"math": math})
            return result
        except Exception as e:
            logger.error(f"Calculation error: {e}")
            return None
