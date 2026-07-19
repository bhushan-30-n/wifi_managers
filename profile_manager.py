"""Profile Manager - Handles Wi-Fi profiles"""

from typing import List, Dict, Optional
from .core import WiFiManager

class ProfileManager:
    """Manages Wi-Fi profiles"""
    
    def __init__(self):
        self.wifi_manager = WiFiManager()
    
    def list_profiles(self) -> List[str]:
        """List all saved profiles"""
        output = self.wifi_manager.run_command("netsh wlan show profiles")
        profiles = []
        
        for line in output.splitlines():
            if "All User Profile" in line or "所有用户配置文件" in line:
                profile_name = line.split(":")[1].strip() if ":" in line else None
                if profile_name and profile_name not in profiles:
                    profiles.append(profile_name)
        
        return profiles
    
    def get_profile_details(self, name: str, show_password: bool = False) -> Dict:
        """Get profile details"""
        command = f'netsh wlan show profile name="{name}"'
        if show_password:
            command += " key=clear"
        
        output = self.wifi_manager.run_command(command)
        
        details = {
            'name': name,
            'ssid': None,
            'authentication': None,
            'encryption': None,
            'security_key': None,
            'key_content': None,
            'network_type': None,
            'radio_type': None,
            'vendor': None
        }
        
        for line in output.splitlines():
            if "SSID" in line and "BSSID" not in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    details['ssid'] = parts[1].strip()
            elif "Authentication" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    details['authentication'] = parts[1].strip()
            elif "Encryption" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    details['encryption'] = parts[1].strip()
            elif "Security key" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    details['security_key'] = parts[1].strip()
            elif "Key Content" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    details['key_content'] = parts[1].strip()
        
        return details
    
    def delete_profile(self, name: str) -> str:
        """Delete a profile"""
        result = self.wifi_manager.run_command(f'netsh wlan delete profile name="{name}"')
        return "Profile deleted successfully!" if "successfully" in result.lower() else f"Failed to delete profile: {result}"
    
    def get_profile_password(self, name: str) -> Optional[str]:
        """Get password for a profile"""
        details = self.get_profile_details(name, show_password=True)
        return details.get('key_content')