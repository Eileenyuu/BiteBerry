"""
Configuration constants for BiteBerry application
"""

class DefaultPreferences:
    """Default values for user preferences"""
    MAX_BUDGET = 50.0
    MAX_COOKING_TIME = 30
    DIETARY_RESTRICTIONS = "none"

class ValidationLimits:
    """Validation limits for user preferences"""
    MIN_BUDGET = 0.0
    MAX_BUDGET = 100.0
    MIN_COOKING_TIME = 0
    MAX_COOKING_TIME = 180