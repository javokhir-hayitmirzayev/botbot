from typing import List, Dict, Any, Tuple, Optional

from src.database import db
from src.utilities.logger import logger

async def save_test_data(test_details: Dict[str, Any], questions_data: List[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
    """
    Saves a test, its questions, and their options using a single transaction.
    """
    try:
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                
                # create test
                test_name = test_details.get('name')
                if not test_name:
                    raise ValueError("Test 'name' is required")
                
                test_id = await conn.fetchval(
                    """
                    INSERT INTO tests (name, description) 
                    VALUES ($1, $2) 
                    RETURNING id
                    """,
                    test_name, 
                    test_details.get('description')
                )
                logger.info("Created test '%s' with ID: %s", test_name, test_id)

                # 2. Insert questions and options
                for q_data in questions_data:
                    question_id = await conn.fetchval(
                        """
                        INSERT INTO questions (test_id, question, type) 
                        VALUES ($1, $2, $3) 
                        RETURNING id
                        """,
                        test_id, 
                        q_data['question_text'], 
                        q_data['question_type']
                    )

                    # 3. Insert options using executemany for high performance
                    options_to_insert = [
                        (question_id, opt['label'], opt['answer_text'], opt['is_correct'])
                        for opt in q_data['options']
                    ]
                    
                    await conn.executemany(
                        """
                        INSERT INTO options (question_id, label, answer, is_correct) 
                        VALUES ($1, $2, $3, $4)
                        """,
                        options_to_insert
                    )

        logger.info("Transaction successful. Test data has been saved to the database.")
        return True, None

    except Exception as e:
        logger.exception("An error occurred saving test data: %s", e)
        return False, str(e)