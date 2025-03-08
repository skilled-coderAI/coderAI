"""
CoderAI Framework Logger
This module provides logging functionality for the CoderAI framework.
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

class LoggerManager:
    """
    Singleton class to manage loggers across the application.
    """
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def get_logger(cls):
        """
        Get the global logger instance.
        
        Returns:
            Logger instance
        """
        return cls._logger
    
    @classmethod
    def set_logger(cls, logger):
        """
        Set the global logger instance.
        
        Args:
            logger: Logger instance to set
        """
        cls._logger = logger

class CoderAILogger:
    """
    Logger for the CoderAI framework.
    """
    def __init__(self, log_path: Optional[str] = None, log_level: int = logging.INFO):
        """
        Initialize the logger.
        
        Args:
            log_path: Path to log file, if None, logs will only be printed to console
            log_level: Logging level
        """
        self.console = Console()
        self.log_path = log_path
        
        # Create logger
        self.logger = logging.getLogger("coderAI")
        self.logger.setLevel(log_level)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # Add console handler to logger
        self.logger.addHandler(console_handler)
        
        # Create file handler if log_path is provided
        if log_path:
            # Create log directory if it doesn't exist
            log_dir = os.path.dirname(log_path)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
                
            # Create file handler
            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            
            # Add file handler to logger
            self.logger.addHandler(file_handler)
            
        # Register with LoggerManager
        LoggerManager.set_logger(self)
    
    def info(self, *args, title: Optional[str] = None, color: str = "blue"):
        """
        Log info message.
        
        Args:
            *args: Arguments to log
            title: Optional title for the panel
            color: Color of the panel border
        """
        message = " ".join(str(arg) for arg in args)
        self.logger.info(message)
        
        if title:
            self.console.print(Panel(
                message,
                title=title,
                border_style=color,
            ))
        else:
            self.console.print(message, style=color)
    
    def warning(self, *args, title: Optional[str] = None, color: str = "yellow"):
        """
        Log warning message.
        
        Args:
            *args: Arguments to log
            title: Optional title for the panel
            color: Color of the panel border
        """
        message = " ".join(str(arg) for arg in args)
        self.logger.warning(message)
        
        if title:
            self.console.print(Panel(
                message,
                title=title,
                border_style=color,
            ))
        else:
            self.console.print(message, style=color)
    
    def error(self, *args, title: Optional[str] = None, color: str = "red"):
        """
        Log error message.
        
        Args:
            *args: Arguments to log
            title: Optional title for the panel
            color: Color of the panel border
        """
        message = " ".join(str(arg) for arg in args)
        self.logger.error(message)
        
        if title:
            self.console.print(Panel(
                message,
                title=title,
                border_style=color,
            ))
        else:
            self.console.print(message, style=color)
    
    def debug(self, *args, title: Optional[str] = None, color: str = "cyan"):
        """
        Log debug message.
        
        Args:
            *args: Arguments to log
            title: Optional title for the panel
            color: Color of the panel border
        """
        message = " ".join(str(arg) for arg in args)
        self.logger.debug(message)
        
        if title:
            self.console.print(Panel(
                message,
                title=title,
                border_style=color,
            ))
        else:
            self.console.print(message, style=color)
    
    def critical(self, *args, title: Optional[str] = None, color: str = "bright_red"):
        """
        Log critical message.
        
        Args:
            *args: Arguments to log
            title: Optional title for the panel
            color: Color of the panel border
        """
        message = " ".join(str(arg) for arg in args)
        self.logger.critical(message)
        
        if title:
            self.console.print(Panel(
                message,
                title=title,
                border_style=color,
            ))
        else:
            self.console.print(message, style=color)
    
    def log_message(self, message: Dict[str, Any], title: Optional[str] = None):
        """
        Log a message.
        
        Args:
            message: Message to log
            title: Optional title for the panel
        """
        role = message.get("role", "unknown")
        content = message.get("content", "")
        
        if role == "system":
            self.console.print(Panel(
                Markdown(content),
                title=title or "System Message",
                border_style="blue",
            ))
        elif role == "user":
            self.console.print(Panel(
                Markdown(content),
                title=title or "User Message",
                border_style="green",
            ))
        elif role == "assistant":
            self.console.print(Panel(
                Markdown(content),
                title=title or "Assistant Message",
                border_style="yellow",
            ))
        else:
            self.console.print(Panel(
                Markdown(content),
                title=title or f"{role.capitalize()} Message",
                border_style="white",
            ))
    
    def log_messages(self, messages: List[Dict[str, Any]], title: Optional[str] = None):
        """
        Log multiple messages.
        
        Args:
            messages: Messages to log
            title: Optional title for the panel
        """
        if title:
            self.console.print(f"[bold]{title}[/bold]")
            
        for message in messages:
            self.log_message(message)
    
    def log_result(self, result: Dict[str, Any], title: Optional[str] = None):
        """
        Log a result.
        
        Args:
            result: Result to log
            title: Optional title for the panel
        """
        self.console.print(Panel(
            str(result),
            title=title or "Result",
            border_style="cyan",
        ))
    
    def log_error(self, error: Union[str, Exception], title: Optional[str] = None):
        """
        Log an error.
        
        Args:
            error: Error to log
            title: Optional title for the panel
        """
        self.console.print(Panel(
            str(error),
            title=title or "Error",
            border_style="red",
        ))
    
    def log_tool_call(self, tool_call: Dict[str, Any], title: Optional[str] = None):
        """
        Log a tool call.
        
        Args:
            tool_call: Tool call to log
            title: Optional title for the panel
        """
        function = tool_call.get("function", {})
        name = function.get("name", "unknown")
        args = function.get("arguments", "{}")
        
        self.console.print(Panel(
            f"Function: {name}\nArguments: {args}",
            title=title or "Tool Call",
            border_style="magenta",
        ))
    
    def log_tool_result(self, tool_result: Dict[str, Any], title: Optional[str] = None):
        """
        Log a tool result.
        
        Args:
            tool_result: Tool result to log
            title: Optional title for the panel
        """
        name = tool_result.get("name", "unknown")
        result = tool_result.get("result", {})
        
        self.console.print(Panel(
            f"Function: {name}\nResult: {result}",
            title=title or "Tool Result",
            border_style="cyan",
        ))
