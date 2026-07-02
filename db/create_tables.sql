-- =====================================================
-- UAE Banking AI Analytics Platform - Database Schema
-- =====================================================
-- This script creates the complete database schema for
-- banking analytics, including customer, account, transaction,
-- and risk management tables.
-- =====================================================

-- Drop existing tables (for fresh setup)
DROP TABLE IF EXISTS RISK_FACTORS CASCADE;
DROP TABLE IF EXISTS COMPLAINTS CASCADE;
DROP TABLE IF EXISTS KYC_DOCUMENTS CASCADE;
DROP TABLE IF EXISTS DIGITAL_CHANNEL_EVENTS CASCADE;
DROP TABLE IF EXISTS CARDS CASCADE;
DROP TABLE IF EXISTS LOANS CASCADE;
DROP TABLE IF EXISTS TRANSACTIONS CASCADE;
DROP TABLE IF EXISTS ACCOUNTS CASCADE;
DROP TABLE IF EXISTS BRANCHES CASCADE;
DROP TABLE IF EXISTS PRODUCTS CASCADE;
DROP TABLE IF EXISTS CUSTOMERS CASCADE;

-- =====================================================
-- 1. BRANCHES TABLE
-- =====================================================
CREATE TABLE BRANCHES (
    branch_id SERIAL PRIMARY KEY,
    branch_name VARCHAR(255) NOT NULL,
    emirate VARCHAR(50) NOT NULL,  -- Abu Dhabi, Dubai, Sharjah, etc.
    city VARCHAR(100) NOT NULL,
    region VARCHAR(100),
    branch_type VARCHAR(50),  -- Main, Sub, Service Center
    staff_count INT,
    created_date DATE DEFAULT CURRENT_DATE,
    UNIQUE(branch_name, emirate)
);

CREATE INDEX idx_branches_emirate ON BRANCHES(emirate);
CREATE INDEX idx_branches_city ON BRANCHES(city);

-- =====================================================
-- 2. CUSTOMERS TABLE
-- =====================================================
CREATE TABLE CUSTOMERS (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    customer_type VARCHAR(50),  -- Individual, Corporate
    email VARCHAR(100),
    phone VARCHAR(20),
    date_of_birth DATE,
    nationality VARCHAR(100),
    emirate VARCHAR(50),  -- Resident emirate
    address VARCHAR(500),
    account_open_date DATE DEFAULT CURRENT_DATE,
    account_status VARCHAR(50) DEFAULT 'Active',  -- Active, Inactive, Dormant
    customer_segment VARCHAR(100),  -- Premium, Standard, Mass Market
    -- UAE/GCC specific fields
    uae_resident_since DATE,
    visa_type VARCHAR(50),
    employment_sector VARCHAR(100),
    annual_income_aed DECIMAL(15, 2),
    pep_flag BOOLEAN DEFAULT FALSE,  -- Politically Exposed Person
    sanctions_flag BOOLEAN DEFAULT FALSE,  -- Sanctions list check
    aml_risk_score INT DEFAULT 0,  -- 0-100
    kyc_status VARCHAR(50) DEFAULT 'Pending',  -- Pending, Verified, Failed
    kyc_completion_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customers_email ON CUSTOMERS(email);
CREATE INDEX idx_customers_phone ON CUSTOMERS(phone);
CREATE INDEX idx_customers_emirate ON CUSTOMERS(emirate);
CREATE INDEX idx_customers_pep_flag ON CUSTOMERS(pep_flag);
CREATE INDEX idx_customers_aml_risk ON CUSTOMERS(aml_risk_score);
CREATE INDEX idx_customers_kyc_status ON CUSTOMERS(kyc_status);

-- =====================================================
-- 3. PRODUCTS TABLE
-- =====================================================
CREATE TABLE PRODUCTS (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    product_category VARCHAR(100),  -- Deposits, Loans, Cards, Digital Services
    product_type VARCHAR(100),  -- Savings Account, Term Loan, Credit Card, etc.
    currency VARCHAR(3) DEFAULT 'AED',
    min_balance_aed DECIMAL(15, 2),
    max_balance_aed DECIMAL(15, 2),
    interest_rate_per_annum DECIMAL(5, 2),
    annual_fee_aed DECIMAL(10, 2),
    is_active BOOLEAN DEFAULT TRUE,
    launch_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_category ON PRODUCTS(product_category);
CREATE INDEX idx_products_type ON PRODUCTS(product_type);

-- =====================================================
-- 4. ACCOUNTS TABLE
-- =====================================================
CREATE TABLE ACCOUNTS (
    account_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    branch_id INT NOT NULL,
    product_id INT NOT NULL,
    account_number VARCHAR(50) UNIQUE NOT NULL,
    account_type VARCHAR(50),  -- Checking, Savings, Money Market
    account_status VARCHAR(50) DEFAULT 'Active',
    currency VARCHAR(3) DEFAULT 'AED',
    current_balance_aed DECIMAL(15, 2) DEFAULT 0,
    available_balance_aed DECIMAL(15, 2) DEFAULT 0,
    account_open_date DATE DEFAULT CURRENT_DATE,
    account_close_date DATE,
    account_manager VARCHAR(100),
    kyc_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id),
    FOREIGN KEY (branch_id) REFERENCES BRANCHES(branch_id),
    FOREIGN KEY (product_id) REFERENCES PRODUCTS(product_id)
);

CREATE INDEX idx_accounts_customer ON ACCOUNTS(customer_id);
CREATE INDEX idx_accounts_branch ON ACCOUNTS(branch_id);
CREATE INDEX idx_accounts_product ON ACCOUNTS(product_id);
CREATE INDEX idx_accounts_status ON ACCOUNTS(account_status);
CREATE INDEX idx_accounts_open_date ON ACCOUNTS(account_open_date);

-- =====================================================
-- 5. TRANSACTIONS TABLE
-- =====================================================
CREATE TABLE TRANSACTIONS (
    transaction_id SERIAL PRIMARY KEY,
    account_id INT NOT NULL,
    customer_id INT NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_time TIME NOT NULL,
    transaction_amount_aed DECIMAL(15, 2) NOT NULL,
    transaction_type VARCHAR(50),  -- Debit, Credit, Transfer
    transaction_category VARCHAR(100),  -- Salary, Bill Payment, Withdrawal, etc.
    merchant_name VARCHAR(255),
    merchant_category VARCHAR(100),
    channel VARCHAR(50),  -- ATM, Online, Branch, Mobile App, Card
    description VARCHAR(500),
    reference_number VARCHAR(100),
    counterparty_account VARCHAR(50),
    counterparty_bank VARCHAR(255),
    fraud_flag BOOLEAN DEFAULT FALSE,
    fraud_score DECIMAL(5, 2) DEFAULT 0,  -- 0-100
    status VARCHAR(50) DEFAULT 'Completed',  -- Completed, Pending, Failed, Reversed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES ACCOUNTS(account_id),
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id)
);

CREATE INDEX idx_transactions_account ON TRANSACTIONS(account_id);
CREATE INDEX idx_transactions_customer ON TRANSACTIONS(customer_id);
CREATE INDEX idx_transactions_date ON TRANSACTIONS(transaction_date);
CREATE INDEX idx_transactions_fraud ON TRANSACTIONS(fraud_flag);
CREATE INDEX idx_transactions_channel ON TRANSACTIONS(channel);
CREATE INDEX idx_txn_account_date ON TRANSACTIONS(account_id, transaction_date);

-- =====================================================
-- 6. LOANS TABLE
-- =====================================================
CREATE TABLE LOANS (
    loan_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    branch_id INT NOT NULL,
    loan_account_number VARCHAR(50) UNIQUE NOT NULL,
    loan_type VARCHAR(100),  -- Personal, Home, Auto, Business, Trade Finance
    loan_amount_aed DECIMAL(15, 2) NOT NULL,
    loan_currency VARCHAR(3) DEFAULT 'AED',
    outstanding_balance_aed DECIMAL(15, 2),
    interest_rate_per_annum DECIMAL(5, 2),
    loan_term_months INT,
    monthly_payment_aed DECIMAL(15, 2),
    origination_date DATE NOT NULL,
    maturity_date DATE,
    purpose VARCHAR(255),
    collateral_type VARCHAR(100),
    collateral_value_aed DECIMAL(15, 2),
    loan_status VARCHAR(50),  -- Active, Closed, Default, Restructured
    -- NPL (Non-Performing Loan) flags
    npl_flag BOOLEAN DEFAULT FALSE,
    days_overdue INT DEFAULT 0,
    -- Credit rating
    credit_rating VARCHAR(10),  -- AAA, AA, A, BBB, BB, B, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id),
    FOREIGN KEY (branch_id) REFERENCES BRANCHES(branch_id)
);

CREATE INDEX idx_loans_customer ON LOANS(customer_id);
CREATE INDEX idx_loans_branch ON LOANS(branch_id);
CREATE INDEX idx_loans_status ON LOANS(loan_status);
CREATE INDEX idx_loans_npl ON LOANS(npl_flag);
CREATE INDEX idx_loans_maturity ON LOANS(maturity_date);

-- =====================================================
-- 7. CARDS TABLE
-- =====================================================
CREATE TABLE CARDS (
    card_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    account_id INT NOT NULL,
    card_number VARCHAR(50) NOT NULL,
    card_type VARCHAR(50),  -- Debit, Credit, Prepaid
    card_brand VARCHAR(50),  -- Visa, Mastercard, American Express
    card_status VARCHAR(50) DEFAULT 'Active',
    issue_date DATE,
    expiry_date DATE,
    cvv VARCHAR(10),
    credit_limit_aed DECIMAL(15, 2),
    current_balance_aed DECIMAL(15, 2),
    is_primary BOOLEAN DEFAULT TRUE,
    fraud_flag BOOLEAN DEFAULT FALSE,
    blocked_flag BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id),
    FOREIGN KEY (account_id) REFERENCES ACCOUNTS(account_id)
);

CREATE INDEX idx_cards_customer ON CARDS(customer_id);
CREATE INDEX idx_cards_account ON CARDS(account_id);
CREATE INDEX idx_cards_status ON CARDS(card_status);
CREATE INDEX idx_cards_fraud ON CARDS(fraud_flag);

-- =====================================================
-- 8. DIGITAL_CHANNEL_EVENTS TABLE
-- =====================================================
CREATE TABLE DIGITAL_CHANNEL_EVENTS (
    event_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    channel VARCHAR(100),  -- Mobile App, Web Portal, SMS, Chatbot
    event_type VARCHAR(100),  -- Login, Transaction, View Statement, Support Request
    event_category VARCHAR(100),  -- Authentication, Transaction, Inquiry, Support
    feature_used VARCHAR(255),  -- Feature or service accessed
    device_type VARCHAR(50),  -- Mobile, Desktop, Tablet
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    session_duration_seconds INT,
    page_views INT,
    transaction_value_aed DECIMAL(15, 2),
    success_flag BOOLEAN DEFAULT TRUE,
    error_message VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id)
);

CREATE INDEX idx_events_customer ON DIGITAL_CHANNEL_EVENTS(customer_id);
CREATE INDEX idx_events_channel ON DIGITAL_CHANNEL_EVENTS(channel);
CREATE INDEX idx_events_date ON DIGITAL_CHANNEL_EVENTS(event_date);
CREATE INDEX idx_events_session ON DIGITAL_CHANNEL_EVENTS(session_id);

-- =====================================================
-- 9. KYC_DOCUMENTS TABLE
-- =====================================================
CREATE TABLE KYC_DOCUMENTS (
    document_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    document_type VARCHAR(100),  -- ID Card, Passport, Employment Letter, Proof of Address, etc.
    document_number VARCHAR(100),
    issue_date DATE,
    expiry_date DATE,
    verification_status VARCHAR(50) DEFAULT 'Pending',  -- Pending, Verified, Rejected, Expired
    verified_by VARCHAR(100),
    verification_date DATE,
    rejection_reason VARCHAR(500),
    document_path VARCHAR(500),  -- Path to stored document
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id)
);

CREATE INDEX idx_kyc_customer ON KYC_DOCUMENTS(customer_id);
CREATE INDEX idx_kyc_status ON KYC_DOCUMENTS(verification_status);
CREATE INDEX idx_kyc_expiry ON KYC_DOCUMENTS(expiry_date);

-- =====================================================
-- 10. COMPLAINTS TABLE
-- =====================================================
CREATE TABLE COMPLAINTS (
    complaint_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    branch_id INT NOT NULL,
    complaint_date DATE NOT NULL,
    complaint_time TIME NOT NULL,
    complaint_category VARCHAR(100),  -- Service, Transaction, Card, Loan, Digital, etc.
    complaint_type VARCHAR(100),  -- Billing Error, Fraudulent Transaction, Service Delay, etc.
    complaint_description TEXT NOT NULL,
    severity VARCHAR(50),  -- Low, Medium, High, Critical
    status VARCHAR(50) DEFAULT 'Open',  -- Open, In Progress, Resolved, Closed
    assigned_to VARCHAR(100),
    resolution_notes TEXT,
    resolution_date DATE,
    resolution_time_days INT,
    customer_satisfaction INT,  -- 1-5 rating
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id),
    FOREIGN KEY (branch_id) REFERENCES BRANCHES(branch_id)
);

CREATE INDEX idx_complaints_customer ON COMPLAINTS(customer_id);
CREATE INDEX idx_complaints_branch ON COMPLAINTS(branch_id);
CREATE INDEX idx_complaints_date ON COMPLAINTS(complaint_date);
CREATE INDEX idx_complaints_status ON COMPLAINTS(status);
CREATE INDEX idx_complaints_category ON COMPLAINTS(complaint_category);

-- =====================================================
-- 11. RISK_FACTORS TABLE
-- =====================================================
CREATE TABLE RISK_FACTORS (
    risk_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    risk_type VARCHAR(100),  -- Credit Risk, Operational Risk, Compliance Risk, Fraud Risk
    risk_category VARCHAR(100),  -- PEP, Sanctions, AML, CDD, EDD, etc.
    risk_score INT DEFAULT 0,  -- 0-100
    risk_level VARCHAR(50),  -- Low, Medium, High, Critical
    assessment_date DATE NOT NULL,
    last_review_date DATE,
    next_review_date DATE,
    -- Specific risk factors
    pep_status BOOLEAN DEFAULT FALSE,
    sanctions_list_match BOOLEAN DEFAULT FALSE,
    adverse_media_flag BOOLEAN DEFAULT FALSE,
    credit_default_history BOOLEAN DEFAULT FALSE,
    high_transaction_velocity BOOLEAN DEFAULT FALSE,
    unusual_activity_flag BOOLEAN DEFAULT FALSE,
    -- Mitigation measures
    mitigation_applied VARCHAR(500),
    monitoring_frequency VARCHAR(50),  -- Daily, Weekly, Monthly, Quarterly
    assigned_to VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id)
);

CREATE INDEX idx_risk_customer ON RISK_FACTORS(customer_id);
CREATE INDEX idx_risk_type ON RISK_FACTORS(risk_type);
CREATE INDEX idx_risk_level ON RISK_FACTORS(risk_level);
CREATE INDEX idx_risk_assessment ON RISK_FACTORS(assessment_date);

-- =====================================================
-- SUMMARY
-- =====================================================
-- Total Tables: 11
-- - BRANCHES: Banking branch locations
-- - CUSTOMERS: Customer master data with UAE/GCC fields
-- - PRODUCTS: Banking products
-- - ACCOUNTS: Customer accounts
-- - TRANSACTIONS: Account transactions (high volume)
-- - LOANS: Loan portfolio
-- - CARDS: Card portfolio
-- - DIGITAL_CHANNEL_EVENTS: Digital interaction tracking
-- - KYC_DOCUMENTS: KYC verification documents
-- - COMPLAINTS: Customer complaint tracking
-- - RISK_FACTORS: Customer risk assessment
-- =====================================================
