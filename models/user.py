from datetime import datetime
import re

class User:
    ROLES = ['admin', 'manager', 'developer']
    def __init__(self, username, email, role) -> None:
        self.id = None
        self.username = username
        self.email = email
        if role not in self.ROLES:
            raise ValueError(f'Invalid role: {role}')
        self.role = role
        self.registration_date = datetime.now()
        if not self._is_valid_email(email):
            raise ValueError('Invalid email address')

    def _is_valid_email(self, email) -> bool:
        pattern = r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,}$'
        return re.match(pattern, email) is not None

    def update_info(self, username=None, email=None, role=None) -> None:
        if username is not None:
            self.username = username
        if email is not None:
            self.email = email
        if role is not None:
            if role not in self.ROLES:
                raise ValueError('Unexpected role')
            self.role = role

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'registration_date': str(self.registration_date),
        }
