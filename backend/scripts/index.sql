CREATE INDEX IF NOT EXISTS ix_attorneys_email ON attorneys (email);

CREATE INDEX IF NOT EXISTS ix_clients_email             ON clients (email);
CREATE INDEX IF NOT EXISTS ix_clients_owner_attorney_id ON clients (owner_attorney_id);

CREATE INDEX IF NOT EXISTS ix_cases_client_id   ON cases (client_id);
CREATE INDEX IF NOT EXISTS ix_cases_attorney_id ON cases (attorney_id);

CREATE INDEX IF NOT EXISTS ix_contacts_case_id ON contacts (case_id);

CREATE INDEX IF NOT EXISTS ix_events_case_id     ON events (case_id);
CREATE INDEX IF NOT EXISTS ix_events_attorney_id ON events (attorney_id);
CREATE INDEX IF NOT EXISTS ix_events_event_date  ON events (event_date);

CREATE INDEX IF NOT EXISTS ix_documents_case_id     ON documents (case_id);
CREATE INDEX IF NOT EXISTS ix_documents_attorney_id ON documents (attorney_id);