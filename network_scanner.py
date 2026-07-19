"""Network Scanner - Handles network scanning"""

from typing import List, Dict
import re
from .core import WiFiManager

class NetworkScanner:
    """Scans for available networks"""
    
    def __init__(self):
        self.wifi_manager = WiFiManager()
    
    def scan_networks(self) -> List[Dict]:
        """Scan for available networks"""
        output = self.wifi_manager.run_command("netsh wlan show networks")
        networks = []
        current_ssid = None
        current_auth = None
        current_signal = None
        
        for line in output.splitlines():
            if "SSID" in line and "BSSID" not in line:
                current_ssid = line.split(":")[1].strip() if ":" in line else None
            elif "Authentication" in line:
                current_auth = line.split(":")[1].strip() if ":" in line else None
            elif "Signal" in line:
                current_signal = line.split(":")[1].strip() if ":" in line else None
            
            if current_ssid and current_auth:
                if current_ssid not in [n['ssid'] for n in networks]:
                    networks.append({
                        'ssid': current_ssid,
                        'security': current_auth,
                        'signal': current_signal,
                        'signal_bars': self._calculate_signal_bars(current_signal)
                    })
                current_ssid = None
                current_auth = None
                current_signal = None
        
        return networks
    
    def _calculate_signal_bars(self, signal: str) -> int:
        """Calculate signal bars from signal strength"""
        if not signal:
            return 3
        
        try:
            # Extract numeric value if present
            numbers = re.findall(r'\d+', signal)
            if numbers:
                strength = int(numbers[0])
                # Convert to 1-5 bars
                if strength >= 80:
                    return 5
                elif strength >= 60:
                    return 4
                elif strength >= 40:
                    return 3
                elif strength >= 20:
                    return 2
                else:
                    return 1
        except:
            pass
        
        return 3  # Default