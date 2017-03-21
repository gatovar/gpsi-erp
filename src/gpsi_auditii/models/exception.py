# -*- coding: utf-8 -*-


class AuditiiException(Exception):
    DUPLICATE_USER_EMAIL = 1
    
    def __init__(self, code):
        self.code = code
