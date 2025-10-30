-- ПОЛУЧИТЬ ВСЕ ДЕЛА АДВОКАТА
SELECT 
    cases.name AS case_name,
    cases.status AS case_status,
    clients.name AS client_name,
    MIN(events.event_date) AS first_event_date
FROM 
    cases
JOIN 
    clients ON cases.client_id = clients.id
JOIN 
    events ON events.case_id = cases.id
WHERE 
    cases.attorney_id = :attorney_id  -- Параметр для фильтрации по адвокату
GROUP BY 
    cases.id, clients.name
ORDER BY 
    first_event_date;

-- ПОЛУЧИТЬ КАРТОЧКУ ДЕЛА
SELECT 
    cases.name AS case_name,
    cases.status AS case_status,
    cases.description AS case_description,
    clients.name AS client_name,
    clients.email AS client_email,
    clients.phone AS client_phone,
    clients.personal_info AS client_personal_info,
    clients.address AS client_address,
    clients.messenger AS client_messenger,
    clients.messenger_handle AS client_messenger_handle,
    documents.id AS document_id
FROM 
    cases
JOIN 
    clients ON cases.client_id = clients.id
LEFT JOIN 
    documents ON documents.case_id = cases.id
WHERE 
    cases.id = :case_id;
