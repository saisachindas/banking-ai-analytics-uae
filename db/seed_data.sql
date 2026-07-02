-- =====================================================
-- UAE Banking AI Analytics Platform - Seed Data
-- =====================================================
-- Sample realistic UAE banking data for development
-- and demonstration purposes.
-- =====================================================

-- =====================================================
-- 1. INSERT BRANCHES
-- =====================================================
INSERT INTO BRANCHES (branch_name, emirate, city, region, branch_type, staff_count, created_date) VALUES
('Downtown Dubai Main Branch', 'Dubai', 'Dubai', 'Downtown', 'Main', 150, '2010-01-15'),
('Al Barsha Sub Branch', 'Dubai', 'Dubai', 'Al Barsha', 'Sub', 45, '2015-03-22'),
('Abu Dhabi Corniche Branch', 'Abu Dhabi', 'Abu Dhabi', 'Corniche', 'Main', 120, '2008-06-10'),
('Sharjah City Center Branch', 'Sharjah', 'Sharjah', 'City Center', 'Sub', 35, '2012-09-05'),
('Ajman Service Center', 'Ajman', 'Ajman', 'Central', 'Service Center', 15, '2018-11-20');

-- =====================================================
-- 2. INSERT PRODUCTS
-- =====================================================
INSERT INTO PRODUCTS (product_name, product_category, product_type, currency, min_balance_aed, max_balance_aed, interest_rate_per_annum, annual_fee_aed, is_active, launch_date) VALUES
('Premium Savings Account', 'Deposits', 'Savings Account', 'AED', 5000, 1000000, 3.5, 0, TRUE, '2020-01-01'),
('Checking Plus Account', 'Deposits', 'Checking Account', 'AED', 1000, 500000, 0.5, 100, TRUE, '2019-06-15'),
('Personal Loan - Standard', 'Loans', 'Personal Loan', 'AED', 0, 500000, 4.5, 0, TRUE, '2015-03-01'),
('Home Loan - Competitive', 'Loans', 'Home Loan', 'AED', 0, 5000000, 2.75, 0, TRUE, '2018-01-01'),
('Credit Card - Gold', 'Cards', 'Credit Card', 'AED', 0, 100000, 0, 500, TRUE, '2016-05-10'),
('Credit Card - Platinum', 'Cards', 'Credit Card', 'AED', 0, 500000, 0, 1500, TRUE, '2017-02-20'),
('Business Account', 'Deposits', 'Business Checking', 'AED', 10000, 5000000, 2.0, 250, TRUE, '2019-01-01'),
('Auto Loan', 'Loans', 'Auto Loan', 'AED', 0, 1000000, 3.5, 0, TRUE, '2020-06-01');

-- =====================================================
-- 3. INSERT CUSTOMERS
-- =====================================================
INSERT INTO CUSTOMERS (customer_name, customer_type, email, phone, date_of_birth, nationality, emirate, address, account_open_date, account_status, customer_segment, uae_resident_since, visa_type, employment_sector, annual_income_aed, pep_flag, sanctions_flag, aml_risk_score, kyc_status, kyc_completion_date) VALUES
('Ahmed Al Mansouri', 'Individual', 'ahmed.mansouri@email.com', '+971501234567', '1980-05-15', 'UAE National', 'Dubai', '123 Sheikh Zayed Road, Dubai', '2018-03-10', 'Active', 'Premium', '1980-05-15', 'UAE National', 'Finance', 500000, FALSE, FALSE, 15, 'Verified', '2018-04-01'),
('Fatima Al Noor', 'Individual', 'fatima.noor@email.com', '+971502345678', '1985-08-20', 'UAE National', 'Abu Dhabi', '456 Corniche Road, Abu Dhabi', '2019-07-22', 'Active', 'Standard', '1985-08-20', 'UAE National', 'Healthcare', 250000, FALSE, FALSE, 20, 'Verified', '2019-08-15'),
('Mohammed Al Suwaidi', 'Individual', 'mohammed.suwaidi@email.com', '+971503456789', '1975-12-10', 'UAE National', 'Dubai', '789 Deira District, Dubai', '2017-01-05', 'Active', 'Premium', '1975-12-10', 'UAE National', 'Oil & Gas', 750000, TRUE, FALSE, 45, 'Verified', '2017-02-01'),
('Layla Al Khaleej', 'Individual', 'layla.khaleej@email.com', '+971504567890', '1988-03-25', 'GCC National', 'Dubai', '321 Marina District, Dubai', '2020-05-11', 'Active', 'Standard', '2010-01-01', 'Visit Visa', 'Engineering', 180000, FALSE, FALSE, 25, 'Verified', '2020-06-15'),
('Abdullah Al Mazrouei', 'Corporate', 'abdullah@almazrouei.ae', '+971505678901', NULL, 'UAE National', 'Abu Dhabi', '654 Business Bay, Abu Dhabi', '2016-02-14', 'Active', 'Premium', NULL, 'Business', 'Trading', 2000000, FALSE, FALSE, 18, 'Verified', '2016-03-10'),
('Noor Al Shamsi', 'Individual', 'noor.shamsi@email.com', '+971506789012', '1990-07-18', 'UAE National', 'Sharjah', '987 Sharjah District', '2021-09-30', 'Active', 'Mass Market', '1990-07-18', 'UAE National', 'Retail', 120000, FALSE, FALSE, 30, 'Verified', '2021-10-25'),
('Khaled Al Mansoori', 'Individual', 'khaled.mansoori@email.com', '+971507890123', '1972-11-05', 'UAE National', 'Dubai', '111 Downtown Dubai', '2015-04-20', 'Active', 'Premium', '1972-11-05', 'UAE National', 'Construction', 600000, FALSE, FALSE, 35, 'Verified', '2015-05-15'),
('Zainab Al Kaabi', 'Individual', 'zainab.kaabi@email.com', '+971508901234', '1986-09-12', 'UAE National', 'Abu Dhabi', '222 Island Road', '2019-11-08', 'Dormant', 'Standard', '1986-09-12', 'UAE National', 'Education', 200000, FALSE, FALSE, 22, 'Verified', '2019-12-01');

-- =====================================================
-- 4. INSERT ACCOUNTS
-- =====================================================
INSERT INTO ACCOUNTS (customer_id, branch_id, product_id, account_number, account_type, account_status, currency, current_balance_aed, available_balance_aed, account_open_date, account_manager, kyc_verified) VALUES
(1, 1, 1, 'AED-001-2018-03010', 'Savings', 'Active', 'AED', 250000, 250000, '2018-03-10', 'Rashid Al Manara', TRUE),
(1, 1, 3, 'AED-001-2018-03015', 'Loan Account', 'Active', 'AED', -150000, 150000, '2018-05-20', 'Rashid Al Manara', TRUE),
(2, 3, 2, 'AED-002-2019-07022', 'Checking', 'Active', 'AED', 45000, 45000, '2019-07-22', 'Amira Al Hosani', TRUE),
(3, 1, 1, 'AED-003-2017-01005', 'Savings', 'Active', 'AED', 800000, 800000, '2017-01-05', 'Rashid Al Manara', TRUE),
(3, 1, 4, 'AED-003-2017-01010', 'Loan Account', 'Active', 'AED', -2500000, 2500000, '2017-06-15', 'Rashid Al Manara', TRUE),
(4, 1, 2, 'AED-004-2020-05011', 'Checking', 'Active', 'AED', 65000, 65000, '2020-05-11', 'Rashid Al Manara', TRUE),
(5, 3, 7, 'AED-005-2016-02014', 'Business', 'Active', 'AED', 1200000, 1200000, '2016-02-14', 'Hassan Al Mansoori', TRUE),
(6, 4, 1, 'AED-006-2021-09030', 'Savings', 'Active', 'AED', 35000, 35000, '2021-09-30', 'Salim Al Qasimi', TRUE),
(7, 1, 1, 'AED-007-2015-04020', 'Savings', 'Active', 'AED', 450000, 450000, '2015-04-20', 'Rashid Al Manara', TRUE),
(8, 3, 2, 'AED-008-2019-11008', 'Checking', 'Dormant', 'AED', 12000, 12000, '2019-11-08', 'Hassan Al Mansoori', TRUE);

-- =====================================================
-- 5. INSERT TRANSACTIONS (Sample)
-- =====================================================
INSERT INTO TRANSACTIONS (account_id, customer_id, transaction_date, transaction_time, transaction_amount_aed, transaction_type, transaction_category, merchant_name, merchant_category, channel, description, reference_number, fraud_flag, status) VALUES
(1, 1, CURRENT_DATE - INTERVAL '5 days', '09:30:00', 15000, 'Debit', 'Salary', 'Company XYZ', 'Employer', 'Online', 'Monthly salary payment', 'REF-001-2024', FALSE, 'Completed'),
(1, 1, CURRENT_DATE - INTERVAL '4 days', '14:15:00', 5000, 'Debit', 'Bill Payment', 'DEWA', 'Utilities', 'Mobile App', 'Electricity bill payment', 'REF-002-2024', FALSE, 'Completed'),
(1, 1, CURRENT_DATE - INTERVAL '3 days', '10:45:00', 2500, 'Debit', 'Shopping', 'Carrefour', 'Retail', 'Card', 'Grocery shopping', 'REF-003-2024', FALSE, 'Completed'),
(2, 1, CURRENT_DATE - INTERVAL '2 days', '11:20:00', 50000, 'Debit', 'Loan Payment', 'Internal Transfer', 'Bank', 'Online', 'Monthly loan payment', 'REF-004-2024', FALSE, 'Completed'),
(3, 2, CURRENT_DATE - INTERVAL '4 days', '13:00:00', 8000, 'Debit', 'Transfer', 'Friend Account', 'Personal', 'Online', 'Transfer to friend', 'REF-005-2024', FALSE, 'Completed'),
(4, 3, CURRENT_DATE - INTERVAL '6 days', '16:30:00', 100000, 'Debit', 'Business', 'Supplier Payment', 'B2B', 'Online', 'Supplier invoice payment', 'REF-006-2024', FALSE, 'Completed'),
(4, 3, CURRENT_DATE - INTERVAL '1 day', '22:45:00', 5000, 'Debit', 'Cash Withdrawal', 'ATM', 'ATM', 'ATM', 'Night time withdrawal', 'REF-007-2024', TRUE, 'Completed'),
(6, 4, CURRENT_DATE - INTERVAL '2 days', '09:00:00', 3000, 'Debit', 'Shopping', 'Lulu Hypermarket', 'Retail', 'Card', 'Weekly shopping', 'REF-008-2024', FALSE, 'Completed');

-- =====================================================
-- 6. INSERT LOANS
-- =====================================================
INSERT INTO LOANS (customer_id, branch_id, loan_account_number, loan_type, loan_amount_aed, loan_currency, outstanding_balance_aed, interest_rate_per_annum, loan_term_months, monthly_payment_aed, origination_date, maturity_date, purpose, collateral_type, collateral_value_aed, loan_status, npl_flag, days_overdue, credit_rating) VALUES
(1, 1, 'LOAN-001-2018-03015', 'Personal Loan', 200000, 'AED', 150000, 4.5, 60, 3800, '2018-05-20', '2023-05-20', 'Personal use', 'None', 0, 'Active', FALSE, 0, 'A'),
(3, 1, 'LOAN-003-2017-01010', 'Home Loan', 3000000, 'AED', 2500000, 2.75, 360, 11500, '2017-06-15', '2047-06-15', 'Property purchase', 'Mortgage', 4000000, 'Active', FALSE, 0, 'AAA'),
(5, 3, 'LOAN-005-2016-02014', 'Business Loan', 1500000, 'AED', 800000, 3.5, 120, 13500, '2016-02-14', '2026-02-14', 'Business expansion', 'Business Assets', 2000000, 'Active', FALSE, 0, 'AA'),
(7, 1, 'LOAN-007-2015-04020', 'Auto Loan', 250000, 'AED', 75000, 3.5, 84, 3200, '2015-04-20', '2022-04-20', 'Vehicle purchase', 'Vehicle', 200000, 'Closed', FALSE, 0, 'A'),
(2, 3, 'LOAN-002-2019-12015', 'Personal Loan', 100000, 'AED', 45000, 5.0, 48, 2200, '2019-12-10', '2023-12-10', 'Personal use', 'None', 0, 'Active', TRUE, 120, 'B');

-- =====================================================
-- 7. INSERT CARDS
-- =====================================================
INSERT INTO CARDS (customer_id, account_id, card_number, card_type, card_brand, card_status, issue_date, expiry_date, cvv, credit_limit_aed, current_balance_aed, is_primary, fraud_flag, blocked_flag) VALUES
(1, 1, '4111111111111111', 'Credit', 'Visa', 'Active', '2020-03-15', '2025-03-15', '123', 100000, 25000, TRUE, FALSE, FALSE),
(2, 3, '4111111111111112', 'Credit', 'Mastercard', 'Active', '2021-06-10', '2026-06-10', '456', 50000, 8000, TRUE, FALSE, FALSE),
(3, 4, '4111111111111113', 'Credit', 'Visa', 'Active', '2019-01-20', '2024-01-20', '789', 200000, 45000, TRUE, FALSE, FALSE),
(4, 6, '4111111111111114', 'Debit', 'Visa', 'Active', '2020-05-11', '2025-05-11', '234', 0, 0, TRUE, FALSE, FALSE),
(5, 7, '4111111111111115', 'Credit', 'Mastercard', 'Active', '2016-02-14', '2025-02-14', '567', 300000, 85000, TRUE, FALSE, FALSE),
(6, 8, '4111111111111116', 'Credit', 'Visa', 'Active', '2021-09-30', '2026-09-30', '890', 30000, 5000, TRUE, FALSE, FALSE),
(7, 9, '4111111111111117', 'Credit', 'Mastercard', 'Active', '2015-04-20', '2024-04-20', '321', 150000, 30000, TRUE, FALSE, FALSE);

-- =====================================================
-- 8. INSERT DIGITAL_CHANNEL_EVENTS (Sample)
-- =====================================================
INSERT INTO DIGITAL_CHANNEL_EVENTS (customer_id, session_id, event_date, event_time, channel, event_type, event_category, feature_used, device_type, user_agent, session_duration_seconds, page_views, transaction_value_aed, success_flag) VALUES
(1, 'SES-001-2024-06-27', CURRENT_DATE, '09:30:00', 'Mobile App', 'Login', 'Authentication', 'Login', 'Mobile', 'Mobile App iOS', 300, 5, 0, TRUE),
(1, 'SES-001-2024-06-27', CURRENT_DATE, '09:35:00', 'Mobile App', 'Transaction', 'Transaction', 'Bill Payment', 'Mobile', 'Mobile App iOS', 300, 5, 5000, TRUE),
(2, 'SES-002-2024-06-27', CURRENT_DATE - INTERVAL '1 day', '14:00:00', 'Web Portal', 'Login', 'Authentication', 'Login', 'Desktop', 'Chrome Browser', 600, 12, 0, TRUE),
(3, 'SES-003-2024-06-27', CURRENT_DATE - INTERVAL '2 days', '22:15:00', 'Mobile App', 'Login', 'Authentication', 'Login', 'Mobile', 'Mobile App Android', 180, 3, 0, TRUE),
(3, 'SES-003-2024-06-27', CURRENT_DATE - INTERVAL '2 days', '22:30:00', 'Mobile App', 'Transaction', 'Transaction', 'Cash Withdrawal', 'Mobile', 'Mobile App Android', 180, 3, 5000, TRUE),
(4, 'SES-004-2024-06-27', CURRENT_DATE - INTERVAL '3 days', '10:45:00', 'Web Portal', 'Inquiry', 'Inquiry', 'Statement View', 'Desktop', 'Safari Browser', 450, 8, 0, TRUE),
(6, 'SES-006-2024-06-27', CURRENT_DATE - INTERVAL '1 day', '11:20:00', 'Mobile App', 'Login', 'Authentication', 'Login', 'Mobile', 'Mobile App iOS', 240, 4, 0, TRUE);

-- =====================================================
-- 9. INSERT KYC_DOCUMENTS
-- =====================================================
INSERT INTO KYC_DOCUMENTS (customer_id, document_type, document_number, issue_date, expiry_date, verification_status, verified_by, verification_date, document_path) VALUES
(1, 'UAE ID Card', '784-1980-5123456-7', '2018-03-15', '2028-03-15', 'Verified', 'KYC Officer 1', '2018-04-01', '/docs/customer_1/uae_id.pdf'),
(1, 'Salary Certificate', 'SC-2024-001', '2024-01-15', '2025-01-15', 'Verified', 'KYC Officer 1', '2018-04-01', '/docs/customer_1/salary_cert.pdf'),
(2, 'UAE ID Card', '784-1985-8123456-8', '2019-08-20', '2029-08-20', 'Verified', 'KYC Officer 2', '2019-08-15', '/docs/customer_2/uae_id.pdf'),
(3, 'UAE ID Card', '784-1975-12123456-9', '2017-02-01', '2027-02-01', 'Verified', 'KYC Officer 1', '2017-02-01', '/docs/customer_3/uae_id.pdf'),
(3, 'Business License', 'BL-2024-ABC123', '2024-01-10', '2025-01-10', 'Verified', 'KYC Officer 1', '2017-02-01', '/docs/customer_3/business_lic.pdf'),
(4, 'Passport', 'P123456789', '2015-06-01', '2030-06-01', 'Verified', 'KYC Officer 2', '2020-06-15', '/docs/customer_4/passport.pdf'),
(5, 'UAE ID Card', '784-1970-03123456-0', '2020-03-15', '2030-03-15', 'Verified', 'KYC Officer 3', '2016-03-10', '/docs/customer_5/uae_id.pdf'),
(6, 'UAE ID Card', '784-1990-07123456-1', '2021-09-15', '2031-09-15', 'Verified', 'KYC Officer 3', '2021-10-25', '/docs/customer_6/uae_id.pdf');

-- =====================================================
-- 10. INSERT COMPLAINTS
-- =====================================================
INSERT INTO COMPLAINTS (customer_id, branch_id, complaint_date, complaint_time, complaint_category, complaint_type, complaint_description, severity, status, assigned_to, resolution_notes, resolution_date, resolution_time_days, customer_satisfaction) VALUES
(1, 1, '2024-06-20', '10:30:00', 'Transaction', 'Delayed Transfer', 'My fund transfer took longer than expected', 'Medium', 'Resolved', 'Officer Ahmed', 'Fund transfer completed within 2 hours. Network issue resolved.', '2024-06-20', 1, 4),
(2, 3, '2024-06-15', '14:00:00', 'Service', 'Application Error', 'Mobile app crashes during login', 'High', 'Resolved', 'Officer Layla', 'App updated. Customer reinstalled and working fine.', '2024-06-17', 2, 3),
(3, 1, '2024-06-10', '11:15:00', 'Card', 'Card Declined', 'Credit card declined at merchant', 'Medium', 'Resolved', 'Officer Rashid', 'Merchant processing issue. Card reactivated.', '2024-06-11', 1, 5),
(4, 1, '2024-06-05', '09:45:00', 'Loan', 'Interest Query', 'Question about loan interest calculation', 'Low', 'Resolved', 'Officer Hassan', 'Explained interest calculation methodology. Customer satisfied.', '2024-06-06', 1, 5),
(6, 4, '2024-05-30', '16:20:00', 'Account', 'Statement Issue', 'Missing transactions in statement', 'High', 'Open', 'Officer Salim', 'Investigation in progress. Multiple transactions verified and added.', NULL, NULL, NULL);

-- =====================================================
-- 11. INSERT RISK_FACTORS
-- =====================================================
INSERT INTO RISK_FACTORS (customer_id, risk_type, risk_category, risk_score, risk_level, assessment_date, last_review_date, next_review_date, pep_status, sanctions_list_match, adverse_media_flag, credit_default_history, high_transaction_velocity, unusual_activity_flag, monitoring_frequency, assigned_to) VALUES
(1, 'Compliance Risk', 'PEP', 45, 'Medium', '2024-01-15', '2024-06-27', '2024-09-27', TRUE, FALSE, FALSE, FALSE, FALSE, FALSE, 'Quarterly', 'Compliance Officer 1'),
(2, 'Credit Risk', 'Credit Profile', 25, 'Low', '2024-01-20', '2024-06-27', '2024-12-27', FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 'Quarterly', 'Risk Officer 1'),
(3, 'Operational Risk', 'Transaction Monitoring', 55, 'Medium', '2024-02-01', '2024-06-27', '2024-08-27', FALSE, FALSE, FALSE, FALSE, TRUE, FALSE, 'Monthly', 'Risk Officer 2'),
(4, 'Credit Risk', 'Credit Profile', 30, 'Low', '2024-02-10', '2024-06-27', '2024-12-27', FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 'Quarterly', 'Risk Officer 1'),
(5, 'Compliance Risk', 'AML Screening', 35, 'Low', '2024-03-01', '2024-06-27', '2024-12-27', FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 'Quarterly', 'Compliance Officer 2'),
(6, 'Credit Risk', 'Credit Profile', 28, 'Low', '2024-03-15', '2024-06-27', '2024-12-27', FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 'Quarterly', 'Risk Officer 1'),
(7, 'Compliance Risk', 'AML Screening', 20, 'Low', '2024-04-01', '2024-06-27', '2024-12-27', FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 'Quarterly', 'Compliance Officer 1'),
(8, 'Credit Risk', 'Credit Profile', 65, 'High', '2024-04-10', '2024-06-27', '2024-07-27', FALSE, FALSE, FALSE, TRUE, FALSE, FALSE, 'Monthly', 'Risk Officer 2');

-- =====================================================
-- Data insertion complete
-- =====================================================
