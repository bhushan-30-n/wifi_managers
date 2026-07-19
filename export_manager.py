"""Export Manager - Handles exporting and backup"""

import json
import csv
from datetime import datetime
from typing import List
from .profile_manager import ProfileManager

class ExportManager:
    """Manages exporting profiles"""
    
    def __init__(self):
        self.profile_manager = ProfileManager()
    
    def export_profiles(self):
        """Export profiles to file"""
        print("\n💾 EXPORT PROFILES")
        print("═"*50)
        print(" 1. Export to JSON")
        print(" 2. Export to CSV")
        print(" 3. Export to TXT")
        print(" 4. Cancel")
        print("═"*50)
        
        choice = input("\n👉 Choose export format: ").strip()
        
        if choice == "1":
            self._export_json()
        elif choice == "2":
            self._export_csv()
        elif choice == "3":
            self._export_txt()
        elif choice == "4":
            return
        else:
            print("❌ Invalid choice")
    
    def _export_json(self):
        """Export to JSON"""
        profiles = self.profile_manager.list_profiles()
        data = []
        
        for profile in profiles:
            details = self.profile_manager.get_profile_details(profile, show_password=True)
            data.append(details)
        
        filename = f"wifi_profiles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Exported to {filename}")
    
    def _export_csv(self):
        """Export to CSV"""
        profiles = self.profile_manager.list_profiles()
        
        filename = f"wifi_profiles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['SSID', 'Authentication', 'Encryption', 'Password'])
            
            for profile in profiles:
                details = self.profile_manager.get_profile_details(profile, show_password=True)
                writer.writerow([
                    details.get('ssid', profile),
                    details.get('authentication', ''),
                    details.get('encryption', ''),
                    details.get('key_content', '')
                ])
        
        print(f"✅ Exported to {filename}")
    
    def _export_txt(self):
        """Export to TXT"""
        profiles = self.profile_manager.list_profiles()
        
        filename = f"wifi_profiles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("WI-FI PROFILES EXPORT\n")
            f.write("="*50 + "\n")
            f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*50 + "\n\n")
            
            for profile in profiles:
                details = self.profile_manager.get_profile_details(profile, show_password=True)
                f.write(f"SSID: {details.get('ssid', profile)}\n")
                f.write(f"Authentication: {details.get('authentication', '')}\n")
                f.write(f"Encryption: {details.get('encryption', '')}\n")
                f.write(f"Password: {details.get('key_content', 'Not available')}\n")
                f.write("-"*30 + "\n")
        
        print(f"✅ Exported to {filename}")
    
    def backup_profiles(self):
        """Backup profiles"""
        print("\n🔄 CREATING BACKUP...")
        self._export_json()
        print("✅ Backup created successfully!")