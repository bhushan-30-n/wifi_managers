"""Core Wi-Fi Manager functionality"""

import subprocess
import platform
import time
from typing import List, Dict, Optional
from .utils import Utils
from .profile_manager import ProfileManager
from .network_scanner import NetworkScanner
from .security import SecurityManager
from .export_manager import ExportManager
from .ui import UIManager

class WiFiManager:
    """Main Wi-Fi Manager class"""
    
    def __init__(self):
        self.utils = Utils()
        self.profile_manager = ProfileManager()
        self.network_scanner = NetworkScanner()
        self.security_manager = SecurityManager()
        self.export_manager = ExportManager()
        self.ui = UIManager()
        
        self.check_admin()
        self.history = []
    
    def check_admin(self):
        """Check if running as administrator"""
        if platform.system() == "Windows":
            try:
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin()
                if not is_admin:
                    self.ui.show_warning("Some features require Administrator privileges! Run as Administrator for full functionality.")
                    time.sleep(2)
            except:
                pass
    
    def run_command(self, command: str) -> str:
        """Execute system command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return f"Error: {str(e)}"
    
    def log_action(self, action: str):
        """Log user actions"""
        timestamp = self.utils.get_timestamp()
        self.history.append(f"[{timestamp}] {action}")
        if len(self.history) > 100:
            self.history.pop(0)
    
    def get_stats(self) -> Dict:
        """Get statistics about saved profiles"""
        profiles = self.profile_manager.list_profiles()
        stats = {
            'total_profiles': len(profiles),
            'secure_profiles': 0,
            'open_profiles': 0,
            'profile_names': profiles
        }
        
        for profile in profiles:
            details = self.profile_manager.get_profile_details(profile, show_password=False)
            if 'WPA2' in details or 'WPA' in details:
                stats['secure_profiles'] += 1
            else:
                stats['open_profiles'] += 1
        
        return stats
    
    def run(self):
        """Main application loop"""
        while True:
            self.ui.clear_screen()
            self.ui.display_banner()
            self.ui.display_menu()
            
            choice = input("\n👉 Enter your choice (1-9): ").strip()
            
            if choice == "1":
                profiles = self.profile_manager.list_profiles()
                self.ui.display_profiles(profiles)
                self.log_action("Listed profiles")
                input("\n⏎ Press Enter to continue...")
            
            elif choice == "2":
                profiles = self.profile_manager.list_profiles()
                if self.ui.display_profiles(profiles):
                    try:
                        n = int(input("\n🔢 Select profile number: "))
                        if 1 <= n <= len(profiles):
                            self.ui.show_profile_details(profiles[n-1])
                            self.log_action(f"Viewed details for {profiles[n-1]}")
                    except ValueError:
                        self.ui.show_error("Please enter a valid number.")
                input("\n⏎ Press Enter to continue...")
            
            elif choice == "3":
                current_info = self.get_current_wifi()
                self.ui.display_current_wifi(current_info)
                self.log_action("Checked current Wi-Fi")
                input("\n⏎ Press Enter to continue...")
            
            elif choice == "4":
                networks = self.network_scanner.scan_networks()
                self.ui.display_networks(networks)
                self.log_action("Scanned networks")
                input("\n⏎ Press Enter to continue...")
            
            elif choice == "5":
                self.export_manager.export_profiles()
                self.log_action("Exported profiles")
                input("\n⏎ Press Enter to continue...")
            
            elif choice == "6":
                self.security_manager.show_security_score()
                input("\n⏎ Press Enter to continue...")
            
            elif choice == "7":
                profiles = self.profile_manager.list_profiles()
                if self.ui.display_profiles(profiles):
                    self._delete_profile_flow(profiles)
                input("\n⏎ Press Enter to continue...")
            
            elif choice == "8":
                self._advanced_tools_menu()
            
            elif choice == "9":
                self.ui.show_goodbye()
                time.sleep(1)
                break
            
            else:
                self.ui.show_error("Invalid choice. Please select 1-9.")
                time.sleep(1)
    
    def _delete_profile_flow(self, profiles: List[str]):
        """Handle profile deletion flow"""
        try:
            n = int(input("\n🗑️  Enter profile number to delete: "))
            if 1 <= n <= len(profiles):
                confirm = input(f"⚠️  Are you sure you want to delete '{profiles[n-1]}'? (y/n): ")
                if confirm.lower() == 'y':
                    result = self.profile_manager.delete_profile(profiles[n-1])
                    self.ui.show_success(result)
                    self.log_action(f"Deleted profile {profiles[n-1]}")
                else:
                    self.ui.show_info("Deletion cancelled.")
            else:
                self.ui.show_error("Invalid selection.")
        except ValueError:
            self.ui.show_error("Please enter a valid number.")
    
    def _advanced_tools_menu(self):
        """Display advanced tools menu"""
        while True:
            self.ui.clear_screen()
            print("\n" + "═"*50)
            print("🔧 ADVANCED TOOLS")
            print("═"*50)
            print(" 1. 📊 View Statistics")
            print(" 2. 🔄 Backup Profiles")
            print(" 3. 📝 View Activity Log")
            print(" 4. 🔐 Change Password (Coming Soon)")
            print(" 5. 📶 Signal Strength Monitor")
            print(" 6. 🔙 Back to Main Menu")
            print("═"*50)
            
            choice = input("\n👉 Enter your choice: ").strip()
            
            if choice == "1":
                stats = self.get_stats()
                self.ui.display_stats(stats)
                self.log_action("Viewed statistics")
                input("\n⏎ Press Enter to continue...")
            elif choice == "2":
                self.export_manager.backup_profiles()
                self.log_action("Backed up profiles")
                input("\n⏎ Press Enter to continue...")
            elif choice == "3":
                self.ui.display_history(self.history)
                input("\n⏎ Press Enter to continue...")
            elif choice == "4":
                self.ui.show_info("Feature coming soon!")
                time.sleep(1)
            elif choice == "5":
                self.ui.monitor_signal_strength()
                input("\n⏎ Press Enter to continue...")
            elif choice == "6":
                break
            else:
                self.ui.show_error("Invalid choice.")
                time.sleep(1)
    
    def get_current_wifi(self) -> Dict:
        """Get current Wi-Fi connection details"""
        output = self.run_command("netsh wlan show interfaces")
        
        if "There is no wireless interface" in output:
            return {'error': 'No wireless interface found'}
        
        info = {
            'ssid': None,
            'signal': None,
            'state': None,
            'radio_type': None,
            'bssid': None
        }
        
        for line in output.splitlines():
            if "SSID" in line and "BSSID" not in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    info['ssid'] = parts[1].strip()
            elif "Signal" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    info['signal'] = parts[1].strip()
            elif "State" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    info['state'] = parts[1].strip()
            elif "Radio type" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    info['radio_type'] = parts[1].strip()
            elif "BSSID" in line:
                parts = line.split(":", 1)
                if len(parts) == 2:
                    info['bssid'] = parts[1].strip()
        
        return info