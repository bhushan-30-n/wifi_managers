"""Utility functions"""

from datetime import datetime
import subprocess
import platform

class Utils:
    """Utility functions"""
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp"""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def get_os():
        """Get operating system"""
        return platform.system()
    
    @staticmethod
    def is_admin() -> bool:
        """Check if running as administrator"""
        if platform.system() == "Windows":
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
        return False
    
    @staticmethod
    def format_bytes(size: int) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"