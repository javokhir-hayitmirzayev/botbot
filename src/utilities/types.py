from enum import Enum

class DB_TABLES(str, Enum):
    USERS = 'users'
    TESTS = 'tests'
    QUESTIONS = 'questions'
    ATTEMPTS = 'attempts'
    QUESTION_OPTIONS = 'options'
    ATTEMPT_ANSWERS = 'answers'


# User roles
class USER_ROLES(str, Enum):
    SUPREME = 'SUPREME'
    ADMIN = 'ADMIN'
    CONSUMER = 'CONSUMER'

# Question types
class QUESTION_TYPES(str, Enum):
    MULTI_CHOICE = 'MULTI_CHOICE'
    MULTI_CORRECT = 'MULTI_CORRECT'

# Attempt status
class ATTEMPT_STATUS(str, Enum):
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    ABANDONED = 'ABANDONED'

class LanguageEnum(str, Enum):
    ENGLISH = "en"
    RUSSIAN = "ru"
    UZBEK = "uz"


class TestStates(str, Enum):
    """States for test creation and management"""
    WAITING_FOR_TEST_NAME = "waiting_for_test_name"
    WAITING_FOR_TEST_DESCRIPTION = "waiting_for_test_description"
    WAITING_FOR_TEST_FILE = "waiting_for_test_file"
