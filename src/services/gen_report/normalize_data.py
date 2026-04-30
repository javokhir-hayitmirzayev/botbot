def process_rows_into_questions(rows):
    """
    Transforms flat SQL rows into a structured list of questions.
    """
    questions_map = {}
    
    for row in rows:
        q_id = row['q_id']
        
        if q_id not in questions_map:
            questions_map[q_id] = {
                'text': row['question'],
                'type': row['q_type'],
                'options': [],
                'correct_labels': [],
                'user_labels': []
            }
        
        questions_map[q_id]['options'].append({
            'label': row['label'],
            'text': row['answer']
        })
        
        if row['is_correct']:
            questions_map[q_id]['correct_labels'].append(row['label'])
            
        if row['user_selected']:
            questions_map[q_id]['user_labels'].append(row['label'])

    return questions_map.values()
