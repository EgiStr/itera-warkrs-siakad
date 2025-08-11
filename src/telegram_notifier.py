"""
Telegram Notification Service
Handles sending notifications via Telegram Bot API
"""

import asyncio
import logging
from typing import Optional, List
from datetime import datetime
import os

try:
    from telegram import Bot
    from telegram.error import TelegramError
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """
    Telegram notification service for WAR KRS automation
    Follows Single Responsibility Principle
    """
    
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        """
        Initialize Telegram notifier
        
        Args:
            bot_token: Telegram bot token
            chat_id: Telegram chat ID to send messages to
        """
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        self.bot = None
        self.enabled = False
        
        if not TELEGRAM_AVAILABLE:
            logger.warning("python-telegram-bot not installed. Telegram notifications disabled.")
            return
        
        if self.bot_token and self.chat_id:
            try:
                self.bot = Bot(token=self.bot_token)
                self.enabled = True
                logger.info("Telegram notifications enabled")
            except Exception as e:
                logger.error(f"Failed to initialize Telegram bot: {e}")
        else:
            logger.info("Telegram credentials not configured. Notifications disabled.")
    
    def is_enabled(self) -> bool:
        """Check if Telegram notifications are enabled"""
        return self.enabled and self.bot is not None
    
    async def _send_message_async(self, message: str, parse_mode: str = "HTML") -> bool:
        """
        Send message asynchronously
        
        Args:
            message: Message to send
            parse_mode: Telegram parse mode (HTML, Markdown, etc.)
            
        Returns:
            True if message sent successfully, False otherwise
        """
        if not self.is_enabled():
            return False
        
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=parse_mode
            )
            return True
        except TelegramError as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Telegram message: {e}")
            return False
    
    def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """
        Send message synchronously (wrapper for async function)
        
        Args:
            message: Message to send
            parse_mode: Telegram parse mode
            
        Returns:
            True if message sent successfully, False otherwise
        """
        if not self.is_enabled():
            logger.debug("Telegram notifications disabled, skipping message")
            return False
        
        try:
            # Run async function in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._send_message_async(message, parse_mode))
            loop.close()
            return result
        except Exception as e:
            logger.error(f"Error in send_message: {e}")
            return False
    
    def notify_start(self, target_courses: List[str]) -> bool:
        """
        Notify that WAR KRS automation has started
        
        Args:
            target_courses: List of target course codes
            
        Returns:
            True if notification sent successfully
        """
        courses_list = "\n".join([f"• <code>{code}</code>" for code in target_courses])
        message = f"""
🚀 <b>WAR KRS DIMULAI</b>

📅 <b>Waktu:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

🎯 <b>Target Mata Kuliah:</b>
{courses_list}

⏳ Sistem akan terus mencoba mendaftarkan mata kuliah hingga berhasil...
        """.strip()
        
        return self.send_message(message)
    
    def notify_course_success(self, course_code: str, course_name: str = None) -> bool:
        """
        Notify successful course registration
        
        Args:
            course_code: Course code that was registered
            course_name: Optional course name
            
        Returns:
            True if notification sent successfully
        """
        name_text = f" - {course_name}" if course_name else ""
        message = f"""
✅ <b>MATA KULIAH BERHASIL DITAMBAHKAN!</b>

📚 <b>Mata Kuliah:</b> <code>{course_code}</code>{name_text}
📅 <b>Waktu:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

🎉 Selamat! Mata kuliah berhasil masuk ke KRS Anda.
        """.strip()
        
        return self.send_message(message)
    
    def notify_all_completed(self, successful_courses: List[str], total_time: str = None) -> bool:
        """
        Notify that all target courses have been completed
        
        Args:
            successful_courses: List of successfully registered courses
            total_time: Optional total execution time
            
        Returns:
            True if notification sent successfully
        """
        courses_list = "\n".join([f"✅ <code>{code}</code>" for code in successful_courses])
        time_text = f"\n⏱️ <b>Total Waktu:</b> {total_time}" if total_time else ""
        
        message = f"""
🎉 <b>WAR KRS SELESAI - SEMUA TARGET BERHASIL!</b>

📅 <b>Waktu Selesai:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{time_text}

📚 <b>Mata Kuliah yang Berhasil:</b>
{courses_list}

🏆 Selamat! Semua mata kuliah target telah berhasil didaftarkan ke KRS Anda.
        """.strip()
        
        return self.send_message(message)
    
    def notify_error(self, error_message: str, course_code: str = None) -> bool:
        """
        Notify about errors
        
        Args:
            error_message: Error message to send
            course_code: Optional course code related to error
            
        Returns:
            True if notification sent successfully
        """
        course_text = f"\n📚 <b>Mata Kuliah:</b> <code>{course_code}</code>" if course_code else ""
        message = f"""
❌ <b>WAR KRS ERROR</b>

📅 <b>Waktu:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{course_text}

🚨 <b>Error:</b> {error_message}

💡 Silakan periksa aplikasi atau coba restart.
        """.strip()
        
        return self.send_message(message)
    
    def notify_session_expired(self) -> bool:
        """
        Notify that session has expired
        
        Returns:
            True if notification sent successfully
        """
        message = f"""
🔒 <b>SESSION EXPIRED</b>

📅 <b>Waktu:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

⚠️ Session SIAKAD Anda telah expired. Silakan:
1. Login ulang ke SIAKAD ITERA
2. Update cookies di file .env
3. Restart aplikasi WAR KRS

💡 Gunakan <code>python setup.py</code> untuk update cookies.
        """.strip()
        
        return self.send_message(message)
    
    def test_connection(self) -> bool:
        """
        Test Telegram connection
        
        Returns:
            True if connection test successful
        """
        if not self.is_enabled():
            return False
        
        message = f"""
🧪 <b>TEST KONEKSI TELEGRAM</b>

📅 <b>Waktu:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

✅ Koneksi Telegram berhasil! WAR KRS siap mengirim notifikasi.
        """.strip()
        
        return self.send_message(message)
