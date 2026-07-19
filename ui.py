"""UI Manager - Handles all display functions"""

import os
from datetime import datetime
from typing import List, Dict, Optional

class UIManager:
    """Handles all user interface elements"""
    
    COLORS = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m',
        'bold': '\033[1m',
    }
    
    def clear_screen(self):
        """Clear terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def colorize(self, text: str, color: str = 'white') -> str:
        """Add color to text"""
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['reset']}"
    
    def display_banner(self):
        """Display application banner"""
        banner = f"""
{self.COLORS['cyan']}╔══════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   ██╗    ██╗██╗███████╗██╗     ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ║
║   ██║    ██║██║██╔════╝██║     ████╗ ████║██╔══██╗████╗  ██║██╔══██╗ ║
║   ██║ █╗ ██║██║█████╗  ██║     ██╔████╔██║███████║██╔██╗ ██║███████║ ║
║   ██║███╗██║██║██╔══╝  ██║     ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║ ║
║   ╚███╔███╔╝██║██║     ███████╗██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║ ║
║    ╚══╝╚══╝ ╚═╝╚═╝     ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ║
║                                                                          ║
║              {self.COLORS['yellow']}🌟 Professional Wi-Fi Manager v2.0 🌟{self.COLORS['cyan']}           ║
╚══════════════════════════════════════════════════════════════════╝{self.COLORS['reset']}
"""
        print(banner)
        print(f"{self.COLORS['green']}📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{self.COLORS['reset']}")
        print("═"*60)
    
    def display_menu(self):
        """Display main menu"""
        menu = f"""
{self.COLORS['cyan']}╔══════════════════════════════════════════════════════════════════╗
║                     {self.COLORS['yellow']}📋 MAIN MENU{self.COLORS['cyan']}                         ║
╠══════════════════════════════════════════════════════════════════╣
║  {self.COLORS['green']}1.{self.COLORS['reset']} 📋 List Saved Wi-Fi Profiles                         ║
║  {self.COLORS['green']}2.{self.COLORS['reset']} 🔍 Show Profile Details (With Password)             ║
║  {self.COLORS['green']}3.{self.COLORS['reset']} 📡 Show Current Wi-Fi Connection                    ║
║  {self.COLORS['green']}4.{self.COLORS['reset']} 🔎 Scan Available Wi-Fi Networks                    ║
║  {self.COLORS['green']}5.{self.COLORS['reset']} 💾 Export Profiles to File                          ║
║  {self.COLORS['green']}6.{self.COLORS['reset']} 🛡️  Security Score & Analysis                      ║
║  {self.COLORS['green']}7.{self.COLORS['reset']} 🗑️  Delete a Saved Profile                         ║
║  {self.COLORS['green']}8.{self.COLORS['reset']} 🔧 Advanced Tools                                 ║
║  {self.COLORS['green']}9.{self.COLORS['reset']} 🚪 Exit                                            ║
╚══════════════════════════════════════════════════════════════════╝{self.COLORS['reset']}
        """
        print(menu)
    
    def display_profiles(self, profiles: List[str]) -> bool:
        """Display profiles in formatted table"""
        if not profiles:
            print(f"\n{self.COLORS['red']}❌ No saved Wi-Fi profiles found.{self.COLORS['reset']}")
            return False
        
        print(f"\n{self.COLORS['yellow']}📋 SAVED WI-FI PROFILES{self.COLORS['reset']}")
        print("═"*50)
        for i, p in enumerate(profiles, 1):
            print(f"  {self.COLORS['cyan']}{i:2}.{self.COLORS['reset']} {p}")
        print("═"*50)
        return True
    
    def show_profile_details(self, name: str):
        """Display detailed profile information"""
        print(f"\n{self.COLORS['yellow']}🔍 Details for: {name}{self.COLORS['reset']}")
        print("═"*50)
        
        # This would be enhanced with actual profile data
        print(f"{self.COLORS['green']}✅ Profile: {name}{self.COLORS['reset']}")
        print("═"*50)
    
    def display_current_wifi(self, info: Dict):
        """Display current Wi-Fi information"""
        if 'error' in info:
            print(f"\n{self.COLORS['red']}❌ {info['error']}{self.COLORS['reset']}")
            return
        
        print(f"\n{self.COLORS['green']}📶 Current Wi-Fi Status:{self.COLORS['reset']}")
        print("═"*40)
        print(f"🌐 SSID: {self.COLORS['cyan']}{info.get('ssid', 'Not connected')}{self.COLORS['reset']}")
        print(f"📊 Signal: {self.COLORS['yellow']}{info.get('signal', 'N/A')}{self.COLORS['reset']}")
        print(f"📡 State: {self.COLORS['green']}{info.get('state', 'N/A')}{self.COLORS['reset']}")
        if info.get('radio_type'):
            print(f"📻 Radio Type: {info.get('radio_type')}")
        if info.get('bssid'):
            print(f"🆔 BSSID: {info.get('bssid')}")
        print("═"*40)
    
    def display_networks(self, networks: List[Dict]):
        """Display available networks"""
        if not networks:
            print(f"\n{self.COLORS['red']}❌ No networks found.{self.COLORS['reset']}")
            return
        
        print(f"\n{self.COLORS['yellow']}🔎 AVAILABLE NETWORKS ({len(networks)}){self.COLORS['reset']}")
        print("═"*50)
        
        for i, network in enumerate(networks, 1):
            signal_bars = "📶" + "█" * min(network.get('signal_bars', 3), 5) + "░" * (5 - min(network.get('signal_bars', 3), 5))
            security_icon = "🔒" if network.get('security') != 'Open' else "🔓"
            
            print(f"  {self.COLORS['cyan']}{i:2}.{self.COLORS['reset']} {network.get('ssid', 'Unknown')}")
            print(f"      {security_icon} {network.get('security', 'Unknown')}")
            print(f"      {signal_bars}")
            print()
    
    def display_stats(self, stats: Dict):
        """Display statistics"""
        print(f"\n{self.COLORS['yellow']}📊 WI-FI STATISTICS{self.COLORS['reset']}")
        print("═"*40)
        print(f"📋 Total Profiles: {self.COLORS['cyan']}{stats.get('total_profiles', 0)}{self.COLORS['reset']}")
        print(f"🔒 Secure Profiles: {self.COLORS['green']}{stats.get('secure_profiles', 0)}{self.COLORS['reset']}")
        print(f"🔓 Open Networks: {self.COLORS['yellow']}{stats.get('open_profiles', 0)}{self.COLORS['reset']}")
        print("═"*40)
    
    def display_history(self, history: List[str]):
        """Display activity history"""
        print(f"\n{self.COLORS['yellow']}📝 ACTIVITY LOG{self.COLORS['reset']}")
        print("═"*50)
        if not history:
            print("No actions logged yet.")
        else:
            for entry in history[-20:]:  # Show last 20 entries
                print(f"  {entry}")
        print("═"*50)
    
    def monitor_signal_strength(self):
        """Monitor signal strength in real-time"""
        print(f"\n{self.COLORS['yellow']}📶 Signal Strength Monitor{self.COLORS['reset']}")
        print("Press Ctrl+C to stop")
        print("═"*40)
        
        # This would be implemented with real monitoring
    
    def show_warning(self, message: str):
        """Display warning message"""
        print(f"{self.COLORS['yellow']}⚠️  {message}{self.COLORS['reset']}")
    
    def show_error(self, message: str):
        """Display error message"""
        print(f"{self.COLORS['red']}❌ {message}{self.COLORS['reset']}")
    
    def show_success(self, message: str):
        """Display success message"""
        print(f"{self.COLORS['green']}✅ {message}{self.COLORS['reset']}")
    
    def show_info(self, message: str):
        """Display info message"""
        print(f"{self.COLORS['blue']}ℹ️  {message}{self.COLORS['reset']}")
    
    def show_goodbye(self):
        """Display goodbye message"""
        print(f"\n{self.COLORS['green']}👋 Thank you for using Wi-Fi Manager!{self.COLORS['reset']}")
        print(f"   {self.COLORS['yellow']}Goodbye! 👋{self.COLORS['reset']}")