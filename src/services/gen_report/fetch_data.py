async def fetch_report_data(conn, attempt_id: int):
    """
    Fetches all necessary data in 2 efficient DB queries using JOINs.
    """
    meta_query = """
        SELECT 
            t.id as test_id, t.name as test_name, 
            a.started_at, a.finished_at, a.score
        FROM attempts a
        JOIN tests t ON a.test_id = t.id
        WHERE a.id = $1
    """
    metadata = await conn.fetchrow(meta_query, attempt_id)
    
    if not metadata:
        return None, None

    details_query = """
        SELECT 
            q.id as q_id, q.question, q.type as q_type,
            o.id as o_id, o.label, o.answer, o.is_correct,
            CASE WHEN ans.id IS NOT NULL THEN TRUE ELSE FALSE END as user_selected
        FROM questions q
        JOIN options o ON o.question_id = q.id
        LEFT JOIN answers ans ON (ans.option_id = o.id AND ans.attempt_id = $1)
        WHERE q.test_id = $2
        ORDER BY q.id, o.label
    """
    rows = await conn.fetch(details_query, attempt_id, metadata['test_id'])
    
    return metadata, rows
