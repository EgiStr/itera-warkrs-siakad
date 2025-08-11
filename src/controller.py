"""
WAR KRS Controller
Main controller orchestrating the WAR KRS process
"""

import time
import os
from typing import Dict, Set
import logging

from .session import SiakadSession
from .krs_service import KRSService

logger = logging.getLogger(__name__)


class WARKRSController:
    """
    Main controller for WAR KRS automation
    Follows SOLID principles and implements the main business logic
    """
    
    def __init__(self, cookies: Dict[str, str], urls: Dict[str, str], 
                 target_courses: Dict[str, str], settings: Dict):
        """
        Initialize WAR KRS controller
        
        Args:
            cookies: Authentication cookies
            urls: SIAKAD URLs
            target_courses: Target courses mapping (code -> class_id)
            settings: Configuration settings
        """
        self.target_courses = target_courses.copy()
        self.settings = settings
        
        # Initialize session and service
        session = SiakadSession(cookies, settings.get('request_timeout', 20))
        self.krs_service = KRSService(session, urls)
        
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
        enrolled = self.krs_service.get_enrolled_courses()
        enrolled_str = ', '.join(sorted(enrolled)) if enrolled else 'Tidak ada'
        print(f"MK Terdaftar Saat Ini: {enrolled_str}")
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
                return True
            else:
                print(f"❌  GAGAL. [{course_code}] belum masuk KRS. "
                      "(Kemungkinan kuota penuh atau sudah diambil).")
                return False
                
        except Exception as e:
            logger.error(f"Error processing course {course_code}: {e}")
            print(f"[ERROR] Terjadi kesalahan saat mencoba mendaftar [{course_code}]: {e}")
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
        
        delay_seconds = self.settings.get('delay_seconds', 45)
        
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
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}")
                print(f"\\n[ERROR] Terjadi kesalahan tidak terduga: {e}")
                print("Mencoba melanjutkan dalam 30 detik...")
                time.sleep(30)
        
        if not self.remaining_targets:
            print("\\n🎉 SELAMAT! Semua mata kuliah target telah berhasil diproses.")
            logger.info("All target courses successfully processed")
        
        logger.info("WAR KRS automation finished")
