#!/usr/bin/env python3
"""Main entry point for Wi-Fi Manager"""

from wifi_manager.core import WiFiManager

def main():
    """Main function"""
    try:
        app = WiFiManager()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()