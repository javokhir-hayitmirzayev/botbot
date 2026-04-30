from datetime import datetime, timedelta
import time

from src.database.intances import (
    test_table,
    user_table,
    attempt_table,
    question_table,
    option_table,
    answer_table,
)
from src.sections.consumer.messages import ConsumerMessages
from src.utilities import ATTEMPT_STATUS
from src.services import generate_test_report


async def get_all_tests(user_id: int):
    tests = await test_table.all()

    if not tests:
        return []

    tests_with_status = []

    for test in tests:
        # Updated: await + $1 placeholder
        # NOTE: params must be a tuple, so use (user_id,) not (user_id)
        user = await user_table.get("tg_id = $1", (user_id,))

        attempt = None
        if user:
            # Updated: await + placeholders
            attempt = await attempt_table.get(
                "user_id = $1 AND test_id = $2", (user["id"], test["id"])
            )

        status = ""
        if attempt:
            if attempt["status"] == "COMPLETED":
                status = " ✅"
            elif attempt["status"] == "IN_PROGRESS":
                status = " 🟡"

        tests_with_status.append(
            {
                "id": test["id"],
                "name": test["name"],
                "status": status,
            }
        )
    return tests_with_status


async def build_question_context(test_id: int, attempt_id: int, question_index: int | None):
    """Prepare all data needed to render a question screen"""

    questions = await question_table.filter("test_id = $1 ORDER BY id", (test_id,))

    if not questions:
        return None

    if question_index is None:
        question_index = 0
    if question_index < 0:
        question_index = 0
    if question_index >= len(questions):
        question_index = len(questions) - 1

    current_question = questions[question_index]
    total_questions = len(questions)

    options = await option_table.filter(
        "question_id = $1 ORDER BY id", (current_question["id"],)
    )

    current_answers = await answer_table.filter(
        "attempt_id = $1 AND question_id = $2", (attempt_id, current_question["id"])
    )
    selected_option_ids = [a["option_id"] for a in current_answers]

    question_text = (
        f"<b>Question {question_index + 1} of {total_questions}</b>\n"
        f"‌\n"
        f"<b>{current_question['question']}</b>\n\n"
        f"<i>Select an answer below:</i>"
    )

    return {
        "question_text": question_text,
        "current_question": current_question,
        "options": options,
        "selected_option_ids": selected_option_ids,
        "total_questions": total_questions,
        "normalized_index": question_index,
    }   


async def finalize_attempt_and_generate_report(
    attempt_id: int, test_id: int, start_time: float | None
):
    """Compute score, update attempt row, build result text and Excel report"""
    # TODO: optimize db queries
    if start_time is None:
        start_time = time.time()

    time_taken_seconds = int(time.time() - start_time)

    questions = await question_table.filter("test_id = $1", (test_id,))
    total_questions = len(questions)
    answers = await answer_table.filter("attempt_id = $1", (attempt_id,))

    correct_questions_count = 0
    for q in questions:
        q_options = await option_table.filter("question_id = $1", (q["id"],))
        q_answers = [a for a in answers if a["question_id"] == q["id"]]

        correct_option_ids = {o["id"] for o in q_options if o["is_correct"]}
        user_selected_ids = {a["option_id"] for a in q_answers}

        if correct_option_ids == user_selected_ids and len(correct_option_ids) > 0:
            correct_questions_count += 1

    final_score_percent = (
        int((correct_questions_count / total_questions) * 100)
        if total_questions > 0
        else 0
    )

    await attempt_table.update(
        data={
            "status": ATTEMPT_STATUS.COMPLETED.value,
            "finished_at": datetime.now(),
            "duration_ms": time_taken_seconds * 1000,
            "score": final_score_percent,
        },
        condition="id = $5",
        params=(attempt_id,),
    )

    test = await test_table.get("id = $1", (test_id,))
    time_str = str(timedelta(seconds=time_taken_seconds)).split(".")[0]

    result_text = ConsumerMessages.TEST_RESULTS.format(
        test_name=test["name"],
        correct_answers=correct_questions_count,
        incorrect_answers=total_questions - correct_questions_count,
        time_taken=time_str,
        score=final_score_percent,
    )

    excel_file = await generate_test_report(attempt_id)

    return result_text, excel_file, test