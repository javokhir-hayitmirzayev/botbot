class ConsumerMessages:
    # Test Selection
    WELCOME = "👋 Welcome to the Test Center! Choose a test to begin:"
    NO_TESTS_AVAILABLE = "ℹ️ There are no tests available at the moment. Please check back later."
    TEST_SELECTION = "📝 Available Tests:"
    
    # Test Instructions
    TEST_STARTED = "📝 *{test_name}*\n\n{description}\n\nClick 'Start Test' when you're ready to begin!"
    TEST_INSTRUCTIONS = (
        "📋 *Test Instructions:*\n\n"
        "1. Read each question carefully\n"
        "2. Select your answer(s)\n"
        "3. You can change your answer before submitting\n"
        "4. Answer all questions before submitting\n"
        "5. Click 'Submit Test' when finished\n\n"
        "Good luck! 🍀"
    )
    
    # Questions
    QUESTION_PROGRESS = "❓ *Question {current} of {total}*"
    TEXT_ANSWER_INSTRUCTION = "✏️ Please type your answer:"
    SELECT_ONE_ANSWER = "Select one correct answer:"
    SELECT_MULTIPLE_ANSWERS = "Select all correct answers (one or more):"
    ANSWER_SAVED = "✅ Answer saved!"
    
    # Navigation
    PREVIOUS_QUESTION = "⬅️ Previous"
    NEXT_QUESTION = "Next ➡️"
    SUBMIT_TEST = "✅ Submit Test"
    CONFIRM_SUBMIT = "Are you sure you want to submit your test? You won't be able to make changes after submission."
    TEST_SUBMITTED = "✅ Test submitted successfully!"
    TEST_TIMED_OUT = "⏰ Time's up! Your test has been automatically submitted."
    
    # Results
    TEST_RESULTS = (
        "📊 *Test Results: {test_name}*\n\n"
        "✅ Correct: {correct_answers}\n"
        "❌ Incorrect: {incorrect_answers}\n"
        "⏱️ Time taken: {time_taken}\n\n"
        "Your score: {score}%"
    )
    
    # Errors
    TEST_ALREADY_TAKEN = "ℹ️ You've already taken this test. Your previous attempt will be used."
    TEST_IN_PROGRESS = "ℹ️ You have a test in progress. Would you like to continue?"
    TEST_NOT_FOUND = "❌ Test not found. Please try selecting a test again."
    INVALID_ANSWER = "⚠️ Please provide a valid answer before proceeding."
    TEST_COMPLETED = "ℹ️ You've already completed this test. Check your results below:"