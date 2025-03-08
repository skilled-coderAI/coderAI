from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import re
import hashlib

@dataclass
class SecurityVulnerability:
    vulnerability_id: str
    severity: str
    description: str
    file_path: str
    line_number: int
    detected_at: datetime
    status: str
    remediation_steps: Optional[str] = None

class SecurityService:
    def __init__(self):
        self.vulnerabilities: Dict[str, SecurityVulnerability] = {}
        self.security_patterns = {
            'sql_injection': r'(?i)(select|insert|update|delete|drop).*?(?:from|into|table|database).*?(?:where|values|set)',
            'hardcoded_secrets': r'(?i)(?:password|secret|key|token)\s*=\s*[\'\"][^\'\"].*?[\'\"]',
            'insecure_functions': r'(?i)eval\(|exec\(|system\(|shell_exec\(',
            'path_traversal': r'\.\./|\.\\',
            'xss_vulnerable': r'(?i)innerHTML|document\.write\(|eval\(.*?\)'
        }

    def scan_file(self, file_path: str, content: str) -> List[SecurityVulnerability]:
        """Scan a file for security vulnerabilities"""
        vulnerabilities = []
        lines = content.split('\n')

        for line_number, line in enumerate(lines, 1):
            for pattern_name, pattern in self.security_patterns.items():
                if re.search(pattern, line):
                    vuln_id = self._generate_vulnerability_id(file_path, line_number, pattern_name)
                    vulnerability = SecurityVulnerability(
                        vulnerability_id=vuln_id,
                        severity=self._determine_severity(pattern_name),
                        description=self._get_vulnerability_description(pattern_name),
                        file_path=file_path,
                        line_number=line_number,
                        detected_at=datetime.now(),
                        status='detected',
                        remediation_steps=self._get_remediation_steps(pattern_name)
                    )
                    self.vulnerabilities[vuln_id] = vulnerability
                    vulnerabilities.append(vulnerability)

        return vulnerabilities

    def get_vulnerability(self, vulnerability_id: str) -> Optional[SecurityVulnerability]:
        """Get details of a specific vulnerability"""
        return self.vulnerabilities.get(vulnerability_id)

    def update_vulnerability_status(self, vulnerability_id: str, status: str) -> bool:
        """Update the status of a vulnerability"""
        if vulnerability_id not in self.vulnerabilities:
            return False

        self.vulnerabilities[vulnerability_id].status = status
        return True

    def get_active_vulnerabilities(self) -> List[Dict]:
        """Get all active vulnerabilities"""
        return [
            {
                'id': vuln.vulnerability_id,
                'severity': vuln.severity,
                'description': vuln.description,
                'file_path': vuln.file_path,
                'line_number': vuln.line_number,
                'detected_at': vuln.detected_at.isoformat(),
                'status': vuln.status
            }
            for vuln in self.vulnerabilities.values()
            if vuln.status != 'resolved'
        ]

    def _generate_vulnerability_id(self, file_path: str, line_number: int, pattern_name: str) -> str:
        """Generate a unique identifier for a vulnerability"""
        content = f"{file_path}:{line_number}:{pattern_name}"
        return hashlib.md5(content.encode()).hexdigest()

    def _determine_severity(self, pattern_name: str) -> str:
        """Determine the severity level of a vulnerability"""
        severity_levels = {
            'sql_injection': 'critical',
            'hardcoded_secrets': 'high',
            'insecure_functions': 'high',
            'path_traversal': 'medium',
            'xss_vulnerable': 'high'
        }
        return severity_levels.get(pattern_name, 'medium')

    def _get_vulnerability_description(self, pattern_name: str) -> str:
        """Get description for a vulnerability type"""
        descriptions = {
            'sql_injection': 'Potential SQL injection vulnerability detected',
            'hardcoded_secrets': 'Hardcoded secret or credential found',
            'insecure_functions': 'Use of potentially insecure function',
            'path_traversal': 'Potential path traversal vulnerability',
            'xss_vulnerable': 'Potential Cross-Site Scripting (XSS) vulnerability'
        }
        return descriptions.get(pattern_name, 'Unknown vulnerability type')

    def _get_remediation_steps(self, pattern_name: str) -> str:
        """Get remediation steps for a vulnerability type"""
        remediation = {
            'sql_injection': 'Use parameterized queries or ORM',
            'hardcoded_secrets': 'Move secrets to environment variables or secure vault',
            'insecure_functions': 'Use secure alternatives or implement proper input validation',
            'path_traversal': 'Implement proper path validation and sanitization',
            'xss_vulnerable': 'Use proper output encoding and content security policies'
        }
        return remediation.get(pattern_name, 'Review and implement security best practices')