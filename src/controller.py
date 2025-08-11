"""
WAR KRS Controller
Main controller orchestrating the WAR KRS process
"""

import time
import os
from typing import Dict, Set
import logging
from datetime import datetime

from .session import SiakadSession
from .krs_service import KRSService
from .telegram_notifier import TelegramNotifier

logger = logging.getLogger(__name__)


class WARKRSController:
    """
    Main controller for WAR KRS automation
    Follows SOLID principles and implements the main business logic
    """
    
    def __init__(self, cookies: Dict[str, str], urls: Dict[str, str], 
                 target_courses: Dict[str, str], settings: Dict, telegram_config: Dict = None,
                 debug_mode: bool = False):
        """
        Initialize WAR KRS controller
        
        Args:
            cookies: Authentication cookies
            urls: SIAKAD URLs
            target_courses: Target courses mapping (code -> class_id)
            settings: Configuration settings
            telegram_config: Telegram configuration (optional)
            debug_mode: Enable debug mode for troubleshooting
        """
        self.target_courses = target_courses.copy()
        self.settings = settings
        self.debug_mode = debug_mode
        self.start_time = datetime.now()
        self.successful_courses = []
        
        # Initialize session and service
        session = SiakadSession(cookies, settings.get('request_timeout', 20))
        self.krs_service = KRSService(session, urls)
        
        # Initialize Telegram notifier
        if telegram_config and telegram_config.get('bot_token') and telegram_config.get('chat_id'):
            self.telegram = TelegramNotifier(
                bot_token=telegram_config['bot_token'],
                chat_id=telegram_config['chat_id']
            )
        else:
            self.telegram = None
        
        # Track remaining targets
        self.remaining_targets = set(target_courses.keys())
    
    def clear_screen(self) -> None:
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_status(self) -> None:
        """Display current status of WAR KRS process"""
        self.clear_screen()
        print("=" * 50)
        print("    WAR KRS OTOMATIS SIAKAD ITERA")
        print("=" * 50)
        print(f"Target Tersisa: {', '.join(sorted(self.remaining_targets))}")
        print("=" * 50)
        print()
        
        # Show currently enrolled courses
        enrolled = self.krs_service.get_enrolled_courses(debug_mode=self.debug_mode)
        enrolled_str = ', '.join(sorted(enrolled)) if enrolled else 'Tidak ada'
        print(f"MK Terdaftar Saat Ini: {enrolled_str}")
        
        if self.debug_mode:
            print("🔍 DEBUG MODE: HTML content saved to debug_enrolled_courses.html")
        
        # Show Telegram status
        if self.telegram and self.telegram.is_enabled():
            print("📱 Telegram notifications: ENABLED")
        else:
            print("📱 Telegram notifications: DISABLED")
        print()
    
    def process_single_course(self, course_code: str) -> bool:
        """
        Process registration for a single course
        
        Args:
            course_code: Course code to process
            
        Returns:
            True if course was successfully registered
        """
        class_id = self.target_courses[course_code]
        
        # Check if already enrolled
        if self.krs_service.is_course_enrolled(course_code):
            print(f"✔️  [{course_code}] sudah ada di KRS. Menghapus dari target.")
            self.remaining_targets.discard(course_code)
            self.successful_courses.append(course_code)
            return True
        
        print(f"⏳  Mencoba mendaftarkan [{course_code}] dengan ID Kelas: {class_id}...")
        
        try:
            # Attempt registration and verification
            success = self.krs_service.register_and_verify(
                course_code, 
                class_id, 
                self.settings.get('verification_delay', 2)
            )
            
            if success:
                print(f"✅  BERHASIL! [{course_code}] telah ditambahkan ke KRS.")
                self.remaining_targets.discard(course_code)
                self.successful_courses.append(course_code)
                
                # Send Telegram notification for successful registration
                if self.telegram:
                    self.telegram.notify_course_success(course_code)
                
                return True
            else:
                print(f"❌  GAGAL. [{course_code}] belum masuk KRS. "
                      "(Kemungkinan kuota penuh atau sudah diambil).")
                return False
                
        except Exception as e:
            logger.error(f"Error processing course {course_code}: {e}")
            print(f"[ERROR] Terjadi kesalahan saat mencoba mendaftar [{course_code}]: {e}")
            
            # Send error notification for critical errors
            if self.telegram:
                if "session" in str(e).lower() or "unauthorized" in str(e).lower():
                    self.telegram.notify_session_expired()
                else:
                    self.telegram.notify_error(str(e), course_code)
            
            return False
    
    def run_single_cycle(self) -> None:
        """Run a single cycle of course registration attempts"""
        self.display_status()
        
        for course_code in list(self.remaining_targets):
            self.process_single_course(course_code)
            
            # Short delay between requests in the same cycle
            inter_delay = self.settings.get('inter_request_delay', 2)
            if inter_delay > 0:
                time.sleep(inter_delay)
    
    def run(self) -> None:
        """
        Main execution method for WAR KRS automation
        Runs continuously until all target courses are obtained
        """
        logger.info("Starting WAR KRS automation")
        
        if not self.remaining_targets:
            print("❌ Tidak ada mata kuliah target yang dikonfigurasi.")
            return
        
        # Send start notification
        if self.telegram:
            self.telegram.notify_start(list(self.remaining_targets))
        
        delay_seconds = self.settings.get('delay_seconds', 45)
        
        try:
            while self.remaining_targets:
                try:
                    self.run_single_cycle()
                    
                    if not self.remaining_targets:
                        break
                    
                    print(f"\\n--- Siklus selesai. Menunggu {delay_seconds} detik "
                          "sebelum memulai siklus berikutnya ---")
                    time.sleep(delay_seconds)
                    
                except KeyboardInterrupt:
                    print("\\n\\n⏹️  Proses dihentikan oleh user.")
                    logger.info("Process interrupted by user")
                    if self.telegram:
                        self.telegram.notify_error("Proses dihentikan oleh user")
                    break
                except Exception as e:
                    logger.error(f"Unexpected error in main loop: {e}")
                    print(f"\\n[ERROR] Terjadi kesalahan tidak terduga: {e}")
                    print("Mencoba melanjutkan dalam 30 detik...")
                    if self.telegram:
                        self.telegram.notify_error(f"Kesalahan tidak terduga: {e}")
                    time.sleep(30)
            
            if not self.remaining_targets:
                # Calculate total time
                total_time = datetime.now() - self.start_time
                hours, remainder = divmod(int(total_time.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                time_str = f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s"
                
                print("\\n🎉 SELAMAT! Semua mata kuliah target telah berhasil diproses.")
                logger.info("All target courses successfully processed")
                
                # Send completion notification
                if self.telegram:
                    self.telegram.notify_all_completed(self.successful_courses, time_str)
        
        except Exception as e:
            logger.error(f"Fatal error in WAR KRS automation: {e}")
            if self.telegram:
                self.telegram.notify_error(f"Fatal error: {e}")
            raise
        
        logger.info("WAR KRS automation finished")
