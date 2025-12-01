INSERT INTO attorneys (attorney_id, first_name, last_name, patronymic, email, phone, hashed_password)
VALUES
    ('32/142-в', 'Иван', 'Иванов', 'Иванович', 'ivanov@example.com', '1234567890', 'hashed_password_1'),
    ('45/56-г', 'Петр', 'Петров', 'Петрович', 'petrov@example.com', '0987654321', 'hashed_password_2'),
    ('12/134-д', 'Сергей', 'Сергеев', 'Сергеевич', 'sergeev@example.com', '1122334455', 'hashed_password_3'),
    ('78/99-к', 'Алексей', 'Алексеев', 'Алексеевич', 'alekseev@example.com', '2233445566', 'hashed_password_4'),
    ('56/78-м', 'Мария', 'Мариева', 'Мариевна', 'marieva@example.com', '3344556677', 'hashed_password_5');


INSERT INTO clients (name, type, email, phone, personal_info, address, messenger, messenger_handle, created_at, owner_attorney_id)
VALUES
    ('ООО "Техно",', FALSE, 'techno@example.com', '1112223333', '1234567890', 'Москва, ул. Ленина, д. 10', 'Telegram', '@techno', timezone('utc', now()), 1),
    ('Иванов Иван', TRUE, 'ivanov@mail.ru', '3334445555', '1234 567890', 'Питер, ул. Садовая, д. 5', 'Viber', '@ivanov_ivan', timezone('utc', now()), 2),
    ('Петрова Ольга', TRUE, 'petrova@mail.ru', '5556667777', '1234 678901', 'Казань, ул. Вишневая, д. 3', 'WhatsApp', '@petrova_olga', timezone('utc', now()), 3);

INSERT INTO cases (name, client_id, attorney_id, status, description, created_at)
VALUES
    ('Дело №1234: Защита интересов ООО "Техно"', 1, 1, 'В процессе', 'Защита интересов компании в судебном разбирательстве.', timezone('utc', now())),
    ('Дело №5678: Иск к Петрову Ивану', 2, 2, 'Закрыто', 'Иск к Ивану за нарушение условий договора.', timezone('utc', now())),
    ('Дело №9876: Нарушение авторских прав', 3, 3, 'В процессе', 'Юридическая консультация по делу о нарушении авторских прав.', timezone('utc', now()));

INSERT INTO contacts (name, personal_info, phone, email, created_at, case_id)
VALUES
    ('Сергей Иванов', '1234 567890', '123-456-7890', 'sergey@example.com', timezone('utc', now()), 1),
    ('Марина Петрова', '1234 678901', '111-222-3333', 'marina@example.com', timezone('utc', now()), 2),
    ('Никита Смирнов', '1111 234567', '555-444-3333', 'nikita@example.com', timezone('utc', now()), 3);

INSERT INTO events (name, description, event_type, event_date, case_id, attorney_id)
VALUES
    ('Слушание по делу №1234', 'Слушание в суде по делу о защите интересов ООО "Техно".', 'Судебное заседание', '2025-11-01 10:00:00+00', 1, 1),
    ('Судебное заседание по делу №5678', 'Заседание суда по иску к Петрову Ивану.', 'Судебное заседание', '2025-11-10 11:00:00+00', 2, 2),
    ('Консультация по делу №9876', 'Консультация по авторским правам.', 'Консультация', '2025-11-15 15:00:00+00', 3, 3);

INSERT INTO documents (file_name, storage_path, checksum, case_id, attorney_id, created_at)
VALUES
    ('Документ_защита_ООО_Техно.pdf', '/files/documents/techno_1234.pdf', 'abcd1234hash', 1, 1, timezone('utc', now())),
    ('Иск_к_Петрову_Ивану.docx', '/files/documents/petrov_5678.docx', 'efgh5678hash', 2, 2, timezone('utc', now())),
    ('Нарушение_авторских_прав.pdf', '/files/documents/authors_right_9876.pdf', 'ijkl9012hash', 3, 3, timezone('utc', now()));
