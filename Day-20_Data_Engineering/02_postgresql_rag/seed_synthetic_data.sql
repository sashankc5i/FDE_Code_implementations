INSERT INTO rag.documents
(title, department, document_type, region, access_level)
VALUES
('Customer 360 Architecture', 'Engineering', 'architecture', 'Global', 'internal'),
('Customer Churn Policy', 'Finance', 'policy', 'Global', 'internal'),
('India Leave Policy', 'HR', 'policy', 'India', 'internal'),
('Azure Authentication Troubleshooting', 'Engineering', 'troubleshooting', 'Global', 'internal');

INSERT INTO rag.document_chunks
(document_id, chunk_number, content, metadata, embedding)
VALUES
(1, 1, 'Customer 360 uses a medallion-style data architecture with governed customer entities.',
 '{"department":"Engineering","document_type":"architecture","region":"Global","access_level":"internal"}',
 '[0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80]'),

(2, 1, 'The customer churn policy defines retention and escalation guidance for customer accounts.',
 '{"department":"Finance","document_type":"policy","region":"Global","access_level":"internal"}',
 '[0.20,0.10,0.40,0.30,0.60,0.50,0.80,0.70]'),

(3, 1, 'Employees working in India follow the organization leave policy for annual and special leave.',
 '{"department":"HR","document_type":"policy","region":"India","access_level":"internal"}',
 '[0.70,0.60,0.50,0.40,0.30,0.20,0.10,0.15]'),

(4, 1, 'AADSTS500011 commonly indicates that the requested resource principal was not found in the tenant.',
 '{"department":"Engineering","document_type":"troubleshooting","region":"Global","access_level":"internal"}',
 '[0.90,0.80,0.70,0.60,0.50,0.40,0.30,0.20]');
