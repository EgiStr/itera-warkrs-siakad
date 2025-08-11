#!/usr/bin/env python3
"""
WAR KRS SIAKAD ITERA - Main Entry Point
Automation tool for course registration at SIAKAD ITERA

Usage:
    python main.py [options]

Options:
    --config, -c     Path to configuration file (default: config/config.json)
    --help, -h       Show this help message
    --setup          Show configuration setup guide
    --log-level      Set logging level (DEBUG, INFO, WARNING, ERROR)
    --log-file       Path to log file
"""

import sys
import argparse
from pathlib import Path
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))
sys.path.insert(0, str(Path(__file__).parent / 'config'))

from src.controller import WARKRSController
from src.utils import setup_logging, validate_cookies, validate_target_courses, print_banner, print_configuration_help
from config.settings import Config


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='WAR KRS SIAKAD ITERA - Automation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--config', '-c',
        default='config/config.json',
        help='Path to configuration file (default: config/config.json)'
    )
    
    parser.add_argument(
        '--setup',
        action='store_true',
        help='Show configuration setup guide'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Set logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--log-file',
        help='Path to log file (optional)'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show current configuration status'
    )
    
    parser.add_argument(
        '--test-telegram',
        action='store_true',
        help='Test Telegram notification connection'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode (saves HTML content for troubleshooting)'
    )
    
    return parser.parse_args()


def validate_configuration(config: Config) -> bool:
    """
    Validate application configuration
    
    Args:
        config: Configuration object
        
    Returns:
        True if configuration is valid, False otherwise
    """
    if not config.is_configured():
        print("❌ Konfigurasi cookie belum diatur!")
        print("   Silakan edit file config/config.json dan isi nilai cookies.")
        print("   Gunakan --setup untuk panduan konfigurasi.")
        return False
    
    if not validate_cookies(config.cookies):
        print("❌ Konfigurasi cookie tidak valid!")
        return False
    
    if not validate_target_courses(config.target_courses):
        print("❌ Konfigurasi target mata kuliah tidak valid!")
        print("   Pastikan ada setidaknya satu mata kuliah target di config.json")
        return False
    
    return True


def main():
    """Main application entry point"""
    args = parse_arguments()
    
    # Setup logging
    setup_logging(args.log_level, args.log_file)
    
    # Show setup guide if requested
    if args.setup:
        print_configuration_help()
        return 0
    
    # Show configuration status if requested
    if args.status:
        try:
            config = Config(args.config)
            print_banner()
            print("📊 CONFIGURATION STATUS:")
            print(f"   Config file: {args.config}")
            print(f"   Cookies configured: {'✅ Yes' if config.is_configured() else '❌ No'}")
            print(f"   Target courses: {len(config.target_courses)} mata kuliah")
            print(f"   Environment file: {'.env found' if Path('.env').exists() else '.env not found'}")
            if config.telegram:
                print(f"   Telegram configured: {'✅ Yes' if config.telegram.get('bot_token') and config.telegram.get('chat_id') else '❌ No'}")
            print()
            print("🎯 Target Courses:")
            for code, class_id in config.target_courses.items():
                print(f"   - {code}: {class_id}")
            print()
            print("⚙️ Settings:")
            settings = config.settings
            for key, value in settings.items():
                print(f"   - {key}: {value}")
            return 0
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return 1
    
    # Test Telegram connection if requested
    if args.test_telegram:
        try:
            config = Config(args.config)
            if not config.telegram or not config.telegram.get('bot_token') or not config.telegram.get('chat_id'):
                print("❌ Telegram belum dikonfigurasi!")
                print("   Silakan jalankan setup.py untuk mengatur Telegram.")
                return 1
            
            print("🔍 Testing Telegram connection...")
            from src.telegram_notifier import TelegramNotifier
            
            notifier = TelegramNotifier(
                bot_token=config.telegram['bot_token'],
                chat_id=config.telegram['chat_id']
            )
            
            if notifier.test_connection():
                print("✅ Telegram connection successful!")
                print("   Bot dapat mengirim notifikasi ke chat yang ditentukan.")
            else:
                print("❌ Telegram connection failed!")
                print("   Periksa bot token dan chat ID Anda.")
            return 0
            
        except Exception as e:
            print(f"❌ Error testing Telegram: {e}")
            return 1
    
    # Load configuration
    try:
        config = Config(args.config)
    except Exception as e:
        print(f"❌ Gagal memuat konfigurasi: {e}")
        return 1
    
    # Show banner
    print_banner()
    
    # Validate configuration
    if not validate_configuration(config):
        print("\\n💡 Gunakan --setup untuk panduan konfigurasi.")
        return 1
    
    # Show current configuration
    print("📋 KONFIGURASI SAAT INI:")
    print(f"   Target Courses: {len(config.target_courses)} mata kuliah")
    print(f"   Delay: {config.settings.get('delay_seconds', 45)} detik")
    print(f"   Timeout: {config.settings.get('request_timeout', 20)} detik")
    print()
    
    # Confirm execution
    try:
        confirm = input("🚀 Mulai WAR KRS automation? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Dibatalkan oleh user.")
            return 0
    except KeyboardInterrupt:
        print("\\n❌ Dibatalkan oleh user.")
        return 0
    
    # Initialize and run controller
    try:
        controller = WARKRSController(
            cookies=config.cookies,
            urls=config.urls,
            target_courses=config.target_courses,
            settings=config.settings,
            telegram_config=config.telegram,
            debug_mode=args.debug  # Pass debug mode to controller
        )
        
        controller.run()
        return 0
        
    except KeyboardInterrupt:
        print("\\n\\n⏹️  Proses dihentikan oleh user.")
        return 130
    except Exception as e:
        print(f"\\n❌ Terjadi kesalahan fatal: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
