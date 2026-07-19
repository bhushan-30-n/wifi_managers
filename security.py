"""Security Manager - Handles security analysis"""

from typing import Dict
from .profile_manager import ProfileManager

class SecurityManager:
    """Manages security analysis"""
    
    def __init__(self):
        self.profile_manager = ProfileManager()
    
    def show_security_score(self):
        """Calculate and display security score"""
        profiles = self.profile_manager.list_profiles()
        
        if not profiles:
            print("❌ No profiles to analyze")
            return
        
        print("\n🛡️  SECURITY ANALYSIS")
        print("═"*50)
        
        total = len(profiles)
        secure = 0
        weak = 0
        vulnerabilities = []
        
        for profile in profiles:
            details = self.profile_manager.get_profile_details(profile, show_password=False)
            
            auth = details.get('authentication', '')
            encryption = details.get('encryption', '')
            
            if 'WPA2' in auth or 'WPA3' in auth:
                secure += 1
            elif 'WPA' in auth:
                weak += 1
                vulnerabilities.append(f"{profile}: Uses WPA (less secure)")
            else:
                weak += 1
                vulnerabilities.append(f"{profile}: Uses {auth or 'Unknown'} (insecure)")
        
        # Display results
        print(f"📋 Total Profiles: {total}")
        print(f"🔒 Secure (WPA2/WPA3): {secure}")
        print(f"⚠️  Weak/Insecure: {weak}")
        
        # Security score (out of 100)
        score = (secure / total * 100) if total > 0 else 0
        print(f"\n📊 Security Score: {score:.1f}/100")
        
        if score >= 80:
            print("✅ Status: Excellent security!")
        elif score >= 60:
            print("⚠️  Status: Good, but improvements needed")
        else:
            print("❌ Status: Poor security - immediate action required!")
        
        if vulnerabilities:
            print("\n📝 Recommendations:")
            for vuln in vulnerabilities[:5]:
                print(f"  • {vuln}")
    
    def analyze_profile_security(self, profile_name: str) -> Dict:
        """Analyze security for a specific profile"""
        details = self.profile_manager.get_profile_details(profile_name)
        
        return {
            'profile': profile_name,
            'auth_type': details.get('authentication', 'Unknown'),
            'encryption': details.get('encryption', 'Unknown'),
            'security_key': details.get('security_key', 'Unknown'),
            'is_secure': 'WPA2' in details.get('authentication', '') or 'WPA3' in details.get('authentication', '')
        }