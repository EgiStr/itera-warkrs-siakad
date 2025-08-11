"""
KRS Service Module
Core business logic for KRS operations
"""

import time
from typing import Set, Dict, Optional
import logging

from .session import SiakadSession
from .parser import KRSParser

logger = logging.getLogger(__name__)


class KRSService:
    """
    Core KRS service handling all KRS-related operations
    Follows Single Responsibility and Open/Closed principles
    """
    
    def __init__(self, session: SiakadSession, urls: Dict[str, str]):
        """
        Initialize KRS service
        
        Args:
            session: Authenticated SIAKAD session
            urls: Dictionary containing required URLs
        """
        self.session = session
        self.urls = urls
        self.parser = KRSParser()
    
    def get_enrolled_courses(self, debug_mode: bool = False) -> Set[str]:
        """
        Get currently enrolled courses
        
        Args:
            debug_mode: If True, save HTML content for debugging
            
        Returns:
            Set of enrolled course codes
        """
        try:
            response = self.session.get(self.urls['pilih_mk'])
            
            if debug_mode:
                self.parser.debug_html_structure(response.text, "debug_enrolled_courses.html")
                analysis = self.parser.analyze_page_structure(response.text)
                logger.info(f"Page analysis: {analysis}")
            
            enrolled = self.parser.parse_enrolled_courses(response.text)
            logger.info(f"Found {len(enrolled)} enrolled courses: {', '.join(sorted(enrolled)) if enrolled else 'None'}")
            
            return enrolled
        except Exception as e:
            logger.error(f"Failed to get enrolled courses: {e}")
            return set()
    
    def is_course_enrolled(self, course_code: str) -> bool:
        """
        Check if a specific course is already enrolled
        
        Args:
            course_code: Course code to check
            
        Returns:
            True if course is enrolled, False otherwise
        """
        enrolled_courses = self.get_enrolled_courses()
        return course_code in enrolled_courses
    
    def register_course(self, class_id: str) -> bool:
        """
        Attempt to register for a course
        
        Args:
            class_id: ID of the class to register for
            
        Returns:
            True if registration was successful, False otherwise
        """
        try:
            payload = {'idkelas': class_id}
            response = self.session.post(self.urls['simpan_krs'], data=payload)
            
            # Check response for success/failure indicators
            if response.status_code in [200, 303]:
                # Extract any alert messages from response
                alert_message = self.parser.extract_alert_message(response.text)
                if alert_message:
                    logger.info(f"Server response: {alert_message}")
                
                return True
            else:
                logger.warning(f"Unexpected status code: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to register course {class_id}: {e}")
            return False
    
    def verify_registration(self, course_code: str, delay: int = 2) -> bool:
        """
        Verify if course registration was successful
        
        Args:
            course_code: Course code to verify
            delay: Delay before verification in seconds
            
        Returns:
            True if course is now enrolled, False otherwise
        """
        if delay > 0:
            time.sleep(delay)
        
        enrolled_courses = self.get_enrolled_courses()
        return course_code in enrolled_courses
    
    def register_and_verify(self, course_code: str, class_id: str, 
                          verification_delay: int = 2) -> bool:
        """
        Register for a course and verify the registration
        
        Args:
            course_code: Course code for verification
            class_id: Class ID for registration
            verification_delay: Delay before verification
            
        Returns:
            True if registration was successful and verified
        """
        # Attempt registration
        registration_success = self.register_course(class_id)
        
        if not registration_success:
            return False
        
        # Verify registration
        return self.verify_registration(course_code, verification_delay)
    
    def is_course_enrolled(self, course_code: str) -> bool:
        """
        Check if a specific course is already enrolled
        
        Args:
            course_code: Course code to check
            
        Returns:
            True if course is enrolled, False otherwise
        """
        enrolled_courses = self.get_enrolled_courses()
        return course_code in enrolled_courses
