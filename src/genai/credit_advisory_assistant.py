"""
Generative AI - Credit Advisory Assistant

Implements a Retrieval-Augmented Generation (RAG) system for answering
credit policy questions using HuggingFace embeddings and FAISS vector search.
"""

import os
import logging
from typing import List, Dict
from pathlib import Path

try:
    from langchain.document_loaders import DirectoryLoader, TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.embeddings.huggingface import HuggingFaceEmbeddings
    from langchain.vectorstores import FAISS
    from langchain.llms.huggingface_pipeline import HuggingFacePipeline
    from langchain.chains import RetrievalQA
    from transformers import pipeline as hf_pipeline
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logging.warning("LangChain not fully installed. RAG features limited.")

logger = logging.getLogger(__name__)


class CreditPolicyAdvisor:
    """
    RAG-based credit policy advisor using HuggingFace embeddings and FAISS.
    """
    
    def __init__(
        self,
        policy_docs_path: str = "data/raw/policy_docs",
        index_path: str = "data/processed/credit_policy_index",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        """
        Initialize the credit policy advisor.
        
        Args:
            policy_docs_path: Path to policy documentation
            index_path: Path to save/load FAISS index
            embedding_model: HuggingFace embedding model name
        """
        self.policy_docs_path = policy_docs_path
        self.index_path = index_path
        self.embedding_model_name = embedding_model
        self.embeddings = None
        self.vector_store = None
        self.qa_chain = None
        
        if LANGCHAIN_AVAILABLE:
            self._initialize()
        else:
            logger.warning("LangChain not available. Using mock responses.")
    
    def _initialize(self):
        """
        Initialize embeddings and vector store.
        """
        try:
            logger.info("Initializing HuggingFace embeddings...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model_name
            )
            
            # Check if index exists
            if os.path.exists(self.index_path):
                logger.info(f"Loading existing FAISS index from {self.index_path}")
                self.vector_store = FAISS.load_local(self.index_path, self.embeddings)
            else:
                logger.info("Creating new FAISS index from policy documents...")
                self._build_index()
            
            if self.vector_store:
                self._setup_qa_chain()
        
        except Exception as e:
            logger.error(f"Error initializing credit advisor: {e}")
    
    def _build_index(self):
        """
        Build FAISS index from policy documents.
        """
        try:
            # Create sample policy documents if directory doesn't exist
            os.makedirs(self.policy_docs_path, exist_ok=True)
            
            # Load documents
            loader = DirectoryLoader(
                self.policy_docs_path,
                glob="**/*.txt",
                loader_cls=TextLoader
            )
            
            documents = loader.load()
            logger.info(f"Loaded {len(documents)} documents")
            
            if not documents:
                logger.warning("No documents found. Creating sample policy.")
                self._create_sample_policy()
                documents = loader.load()
            
            # Split documents
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            splits = splitter.split_documents(documents)
            logger.info(f"Split into {len(splits)} chunks")
            
            # Create FAISS index
            self.vector_store = FAISS.from_documents(
                splits,
                self.embeddings
            )
            
            # Save index
            os.makedirs(self.index_path, exist_ok=True)
            self.vector_store.save_local(self.index_path)
            logger.info(f"FAISS index saved to {self.index_path}")
        
        except Exception as e:
            logger.error(f"Error building index: {e}")
    
    def _create_sample_policy(self):
        """
        Create sample credit policy document.
        """
        sample_policy = """
        UAE BANKING - CREDIT POLICY GUIDELINES
        
        1. CREDIT LIMITS
        - UAE Nationals: Maximum AED 1,000,000 for personal loans
        - GCC Nationals: Maximum AED 500,000 for personal loans
        - Expat Residents: Maximum AED 300,000 for personal loans
        
        2. INTEREST RATES
        - Base rate: 2.5% per annum
        - Personal loans: 4.0-5.5% per annum
        - Home loans: 2.0-3.5% per annum
        - Auto loans: 3.0-4.0% per annum
        
        3. DOCUMENTATION REQUIREMENTS
        - Valid ID/Passport
        - Salary certificate (last 3 months)
        - Bank statement (last 3 months)
        - Proof of address
        - Employment contract
        
        4. APPROVAL CRITERIA
        - Debt-to-income ratio: Maximum 40%
        - Age: Minimum 21, Maximum 65 years
        - Credit score: Minimum 600 (if available)
        - Employment stability: Minimum 1 year
        
        5. DEFAULT POLICY
        - After 30 days overdue: Warning notification
        - After 90 days overdue: Escalation to recovery team
        - After 180 days overdue: Legal action initiated
        
        6. SPECIAL CASES
        - PEP (Politically Exposed Persons): Enhanced due diligence required
        - High-risk countries: Restricted lending
        - Sanctions list: Automatic rejection
        """
        
        policy_file = os.path.join(self.policy_docs_path, "credit_policy.txt")
        os.makedirs(self.policy_docs_path, exist_ok=True)
        
        with open(policy_file, 'w') as f:
            f.write(sample_policy)
        
        logger.info(f"Sample policy created at {policy_file}")
    
    def _setup_qa_chain(self):
        """
        Setup RetrievalQA chain.
        """
        try:
            if not LANGCHAIN_AVAILABLE:
                return
            
            # Create LLM using Flan-T5
            logger.info("Setting up LLM pipeline...")
            llm_pipeline = hf_pipeline(
                "text2text-generation",
                model="google/flan-t5-base",
                device=-1  # CPU
            )
            
            llm = HuggingFacePipeline(
                model_kwargs={"temperature": 0.1},
                pipeline=llm_pipeline
            )
            
            # Create QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(
                    search_kwargs={"k": 3}
                )
            )
            
            logger.info("QA chain initialized successfully")
        
        except Exception as e:
            logger.error(f"Error setting up QA chain: {e}")
    
    def answer_question(self, question: str) -> str:
        """
        Answer a credit policy question.
        
        Args:
            question: User question about credit policies
        
        Returns:
            str: Answer based on policy documents
        
        Examples:
            advisor = CreditPolicyAdvisor()
            answer = advisor.answer_question("What are the credit limits for UAE nationals?")
        """
        try:
            if not self.qa_chain:
                return self._get_mock_answer(question)
            
            logger.info(f"Answering question: {question}")
            response = self.qa_chain.run(question)
            return response
        
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return self._get_mock_answer(question)
    
    def _get_mock_answer(self, question: str) -> str:
        """
        Provide mock answer when RAG is not available.
        
        Args:
            question: User question
        
        Returns:
            str: Mock answer
        """
        if "credit limit" in question.lower():
            return "UAE nationals have a maximum credit limit of AED 1,000,000. GCC nationals: AED 500,000. Expat residents: AED 300,000."
        elif "interest" in question.lower():
            return "Base interest rate is 2.5%. Personal loans: 4.0-5.5%. Home loans: 2.0-3.5%. Auto loans: 3.0-4.0%."
        elif "document" in question.lower():
            return "Required documents: Valid ID/Passport, salary certificate (3 months), bank statement (3 months), proof of address, employment contract."
        elif "default" in question.lower():
            return "After 30 days overdue: warning. After 90 days: escalation. After 180 days: legal action."
        else:
            return "Please refer to the credit policy documentation or contact the credit operations team."


if __name__ == "__main__":
    # Initialize advisor
    advisor = CreditPolicyAdvisor()
    
    # Example questions
    questions = [
        "What are the credit limits for UAE nationals?",
        "What is the interest rate for home loans?",
        "What documents are required for a personal loan?",
        "What happens if a customer defaults on a loan?"
    ]
    
    print("\n=== Credit Policy Advisor ===")
    for question in questions:
        print(f"\nQ: {question}")
        answer = advisor.answer_question(question)
        print(f"A: {answer}")
