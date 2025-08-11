"""
KRS Parser Module
Handles parsing of KRS-related HTML content
"""

from bs4 import BeautifulSoup
from typing import Set, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class KRSParser:
    """Parser for KRS-related HTML content following Single Responsibility Principle"""
    
    @staticmethod
    def parse_enrolled_courses(html_content: str) -> Set[str]:
        """
        Parse enrolled courses from KRS page HTML
        
        Args:
            html_content: HTML content of the KRS page
            
        Returns:
            Set of course codes that are currently enrolled
        """
        enrolled_codes = set()
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find the KRS table by its unique ID
            krs_table = soup.find('table', id='tabelkrs')
            
            if not krs_table:
                logger.warning("KRS table with id 'tabelkrs' not found")
                return enrolled_codes
            
            # Find table body to avoid header/footer rows
            table_body = krs_table.find('tbody')
            if not table_body:
                logger.info("No tbody found in KRS table")
                return enrolled_codes
            
            rows = table_body.find_all('tr')
            
            for row in rows:
                cols = row.find_all('td')
                
                # Ensure row has enough columns
                if len(cols) > 1:
                    # Second column (index 1) contains 'CODE - COURSE_NAME'
                    full_course_text = cols[1].text.strip()
                    course_code = full_course_text.split(' - ')[0]
                    
                    if course_code:
                        enrolled_codes.add(course_code)
                        
        except Exception as e:
            logger.error(f"Failed to parse enrolled courses: {e}")
        
        return enrolled_codes
    
    @staticmethod
    def parse_course_options(html_content: str) -> List[Dict[str, str]]:
        """
        Parse available course options from selection page
        
        Args:
            html_content: HTML content of the course selection page
            
        Returns:
            List of dictionaries containing course information
        """
        courses = []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find course selection dropdown/options
            options = soup.find_all('option')
            
            for option in options:
                value = option.get('value', '').strip()
                text = option.text.strip()
                
                if value and text and '-' in text:
                    # Parse course code from text
                    parts = text.split(' - ')
                    if len(parts) >= 2:
                        course_code = parts[0].strip()
                        course_name = parts[1].strip()
                        
                        courses.append({
                            'code': course_code,
                            'name': course_name,
                            'value': value,
                            'full_text': text
                        })
                        
        except Exception as e:
            logger.error(f"Failed to parse course options: {e}")
        
        return courses
    
    @staticmethod
    def extract_alert_message(html_content: str) -> str:
        """
        Extract alert message from response HTML
        
        Args:
            html_content: HTML content that may contain alert messages
            
        Returns:
            Alert message if found, empty string otherwise
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Look for JavaScript alert in script tags
            scripts = soup.find_all('script')
            
            for script in scripts:
                if script.string and 'alert(' in script.string:
                    # Extract message from alert("message")
                    start = script.string.find('alert("') + 7
                    end = script.string.find('")', start)
                    
                    if start > 6 and end > start:
                        return script.string[start:end]
            
            # Also look for other common alert patterns
            alert_patterns = ['alert(\'', 'alert("']
            
            for pattern in alert_patterns:
                if pattern in html_content:
                    start_idx = html_content.find(pattern) + len(pattern)
                    end_char = pattern[-1]  # ' or "
                    end_idx = html_content.find(end_char + ')', start_idx)
                    
                    if end_idx > start_idx:
                        return html_content[start_idx:end_idx]
                        
        except Exception as e:
            logger.error(f"Failed to extract alert message: {e}")
        
        return ""
