import pandas as pd
from typing import List, Dict, Any

from src.utilities.types import QUESTION_TYPES
from src.utilities.logger import logger


def extract_questions(file_obj) -> List[Dict[str, Any]]:
    """Read Excel file and transform rows into structured question dictionaries."""
    try:
        df = pd.read_excel(file_obj, dtype=str).fillna("")
        logger.info("Successfully loaded %d rows from file", len(df))
    except Exception as e:
        logger.exception("An error occurred while reading the Excel file: %s", e)
        return []

    parsed_questions = []
    option_columns = ["A", "B", "C", "D", "E"]

    for index, row in df.iterrows():
        try:
            question_text = row["questions"]
            if not question_text:
                logger.warning(
                    "Skipping row %d because the 'questions' column is empty.",
                    index + 2,
                )
                continue

            # get question type
            is_multi = str(row.get("multi_correct", "no")).strip().lower() == "yes"
            question_type = (
                QUESTION_TYPES.MULTI_CORRECT.value
                if is_multi
                else QUESTION_TYPES.MULTI_CHOICE.value
            )

            # get correct answers
            correct_answers = {
                ans.strip() for ans in str(row["answer"]).split(",") if ans.strip()
            }

            # get the options
            options_list = []
            for label in option_columns:
                answer_text = str(row.get(label, "")).strip()
                if answer_text:
                    options_list.append(
                        {
                            "label": label,
                            "answer_text": answer_text,
                            "is_correct": label in correct_answers,
                        }
                    )

            if not options_list:
                logger.warning(
                    "Skipping question '%s' on row %d as it has no options.",
                    question_text,
                    index + 2,
                )
                continue

            # put everything together
            question_data = {
                "question_text": question_text,
                "question_type": question_type,
                "options": options_list,
            }
            parsed_questions.append(question_data)

        except Exception as e:
            logger.exception(
                "Could not parse row %d. Error: %s",
                index + 2,
                e,
            )

    return parsed_questions
