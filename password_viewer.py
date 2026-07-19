import subprocess
import os
import platform
import re
from datetime import datetime
import time

class WiFiManager:
    def __init__(self):
        self.clear_screen()
        self.check_admin()
        
    def clear_screen(self):
        """Clear terminal screen for better UI"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def check_admin(self):
        """Check if running as administrator (required for some operations)"""
        if platform.system() == "Windows":
            try:
                import ctypes
                is_admin = ctypes.windll.shell32.IsUserAnAdmin()
                if not is_admin:
                    print("⚠️  Warning: Some features require Administrator privileges!")
                    print("   Please run as Administrator for full functionality.\n")
                    time.sleep(2)
            except:
                pass
    
    def run_command(self, command):
        """Execute command and return output"""
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
    
    def list_profiles(self):
        """Get list of saved Wi-Fi profiles"""
        output = self.run_command("netsh wlan show profiles")
        profiles = []
        
        for line in output.splitlines():
            if "All User Profile" in line or "所有用户配置文件" in line:
                profile_name = line.split(":")[1].strip() if ":" in line else None
                if profile_name:
                    profiles.append(profile_name)
        
        return profiles
    
    def get_profile_details(self, name, show_password=False):
        """Get detailed profile information including password"""
        command = f'netsh wlan show profile name="{name}" key=clear' if show_password else f'netsh wlan show profile name="{name}"'
        return self.run_command(command)
    
    def get_current_wifi(self):
        """Get current Wi-Fi connection details"""
        output = self.run_command("netsh wlan show interfaces")
        
        if "There is no wireless interface" in output:
            return "❌ No wireless interface found."
        
        # Parse current connection
        current_ssid = None
        signal = None
        state = None
        
        for line in output.splitlines():
            if "SSID" in line and "BSSID" not in line:
                current_ssid = line.split(":")[1].strip() if ":" in line else None
            elif "Signal" in line:
                signal = line.split(":")[1].strip() if ":" in line else None
            elif "State" in line:
                state = line.split(":")[1].strip() if ":" in line else None
        
        result = f"📶 Current Wi-Fi Status:\n{'='*40}\n"
        result += f"🌐 SSID: {current_ssid or 'Not connected'}\n"
        result += f"📊 Signal: {signal or 'N/A'}\n"
        result += f"📡 State: {state or 'N/A'}\n"
        
        return result
    
    def delete_profile(self, name):
        """Delete a saved Wi-Fi profile"""
        result = self.run_command(f'netsh wlan delete profile name="{name}"')
        return "✅ Profile deleted successfully!" if "successfully" in result.lower() else f"❌ Failed to delete profile.\n{result}"
    
    def get_all_wifi_networks(self):
        """Scan for available Wi-Fi networks"""
        output = self.run_command("netsh wlan show networks")
        networks = []
        current_ssid = None
        
        for line in output.splitlines():
            if "SSID" in line and "BSSID" not in line:
                current_ssid = line.split(":")[1].strip() if ":" in line else None
            elif "Authentication" in line and current_ssid:
                auth = line.split(":")[1].strip() if ":" in line else None
                if current_ssid and current_ssid not in [n[0] for n in networks]:
                    networks.append([current_ssid, auth])
                current_ssid = None
        
        return networks
    
    def display_banner(self):
        """Display attractive banner"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██╗    ██╗██╗███████╗██╗     ███╗   ███╗ █████╗ ███╗   ██╗
║   ██║    ██║██║██╔════╝██║     ████╗ ████║██╔══██╗████╗  ██║
║   ██║ █╗ ██║██║█████╗  ██║     ██╔████╔██║███████║██╔██╗ ██║
║   ██║███╗██║██║██╔══╝  ██║     ██║╚██╔╝██║██╔══██║██║╚██╗██║
║   ╚███╔███╔╝██║██║     ███████╗██║ ╚═╝ ██║██║  ██║██║ ╚████║
║    ╚══╝╚══╝ ╚═╝╚═╝     ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
║                                                           ║
║              🌟 Professional Wi-Fi Manager 🌟            ║
╚═══════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
    
    def display_menu(self):
        """Display main menu with options"""
        menu = """
╔═══════════════════════════════════════════════════════════╗
║                     📋 MAIN MENU                         ║
╠═══════════════════════════════════════════════════════════╣
║  1. 📋 List Saved Wi-Fi Profiles                        ║
║  2. 🔍 Show Profile Details (With Password)            ║
║  3. 📡 Show Current Wi-Fi Connection                   ║
║  4. 🔎 Scan Available Wi-Fi Networks                   ║
║  5. 🗑️  Delete a Saved Profile                         ║
║  6. 🔄 Refresh & Scan Networks                        ║
║  7. 🚪 Exit                                           ║
╚═══════════════════════════════════════════════════════════╝
        """
        print(menu)
    
    def display_profiles(self, profiles):
        """Display profiles in a formatted table"""
        if not profiles:
            print("\n❌ No saved Wi-Fi profiles found.")
            return False
        
        print("\n📋 SAVED WI-FI PROFILES")
        print("═"*50)
        for i, p in enumerate(profiles, 1):
            print(f"  {i:2}. {p}")
        print("═"*50)
        return True
    
    def show_profile_with_password(self, name):
        """Show profile details including password"""
        print(f"\n🔍 Details for: {name}")
        print("═"*50)
        
        # Get profile details with password
        output = self.get_profile_details(name, show_password=True)
        
        # Parse and display nicely
        key_content = None
        security_key = None
        authentication = None
        encryption = None
        
        for line in output.splitlines():
            if "Key Content" in line:
                key_content = line.split(":")[1].strip() if ":" in line else None
            elif "Security key" in line:
                security_key = line.split(":")[1].strip() if ":" in line else None
            elif "Authentication" in line:
                authentication = line.split(":")[1].strip() if ":" in line else None
            elif "Encryption" in line:
                encryption = line.split(":")[1].strip() if ":" in line else None
        
        # Display parsed information
        if authentication:
            print(f"🔐 Authentication: {authentication}")
        if encryption:
            print(f"🔑 Encryption: {encryption}")
        if security_key:
            print(f"🔒 Security Key: {security_key}")
        if key_content:
            print(f"🔑 PASSWORD: {key_content}")
            print("─"*40)
            print("⚠️  Copy the password: " + key_content)
        else:
            print("\n❌ No password found (Profile might not have a saved key)")
            print("   Try running as Administrator to view passwords")
        
        # Show additional details
        if "Name" in output:
            for line in output.splitlines():
                if any(opt in line for opt in ["Name", "SSID", "Network type", "Radio type", "Vendor"]):
                    if "Key Content" not in line and "Security key" not in line:
                        parts = line.split(":", 1)
                        if len(parts) == 2:
                            print(f"  {parts[0].strip()}: {parts[1].strip()}")
        
        print("═"*50)
    
    def scan_networks(self):
        """Scan and display available networks"""
        print("\n🔎 SCANNING FOR AVAILABLE NETWORKS...")
        print("═"*50)
        
        networks = self.get_all_wifi_networks()
        
        if not networks:
            print("❌ No networks found or Wi-Fi adapter not available.")
            return
        
        print(f"📡 Found {len(networks)} network(s):\n")
        for i, (ssid, auth) in enumerate(networks, 1):
            signal_bars = "📶" + "█" * min(int(i % 5), 5) + "░" * (5 - min(int(i % 5), 5))
            print(f"  {i:2}. {ssid}")
            print(f"      🔒 {auth}")
            print(f"      {signal_bars}")
            print()
    
    def run(self):
        """Main application loop"""
        while True:
            self.clear_screen()
            self.display_banner()
            self.display_menu()
            
            choice = input("\n👉 Enter your choice (1-7): ").strip()
            
            if choice == "1":
                profiles = self.list_profiles()
                self.display_profiles(profiles)
                input("\n⏎ Press Enter to continue...")
            
            elif choice == "2":
                profiles = self.list_profiles()
                if self.display_profiles(profiles):
                    try:
                        n = int(input("\n🔢 Select profile number: "))
                        if 1 <= n <= len(profiles):
                            self.show_profile_with_password(profiles[n-1])
                        else:
                            print("❌ Invalid selection.")
                    except ValueError:
                        print("❌ Please enter a valid number.")
                input("\n⏎ Press Enter to continue...")
            
            elif choice == "3":
                print("\n" + self.get_current_wifi())
                input("\n⏎ Press Enter to continue...")
            
            elif choice == "4":
                self.scan_networks()
                input("\n⏎ Press Enter to continue...")
            
            elif choice == "5":
                profiles = self.list_profiles()
                if self.display_profiles(profiles):
                    try:
                        n = int(input("\n🗑️  Enter profile number to delete: "))
                        if 1 <= n <= len(profiles):
                            confirm = input(f"⚠️  Are you sure you want to delete '{profiles[n-1]}'? (y/n): ")
                            if confirm.lower() == 'y':
                                result = self.delete_profile(profiles[n-1])
                                print(result)
                        else:
                            print("❌ Invalid selection.")
                    except ValueError:
                        print("❌ Please enter a valid number.")
                input("\n⏎ Press Enter to continue...")
            
            elif choice == "6":
                print("\n🔄 Refreshing network list...")
                self.scan_networks()
                input("\n⏎ Press Enter to continue...")
            
            elif choice == "7":
                print("\n👋 Thank you for using Wi-Fi Manager!")
                print("   Goodbye! 👋")
                time.sleep(1)
                break
            
            else:
                print("❌ Invalid choice. Please select 1-7.")
                time.sleep(1)

if __name__ == "__main__":
    try:
        app = WiFiManager()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        input("\nPress Enter to exit...")