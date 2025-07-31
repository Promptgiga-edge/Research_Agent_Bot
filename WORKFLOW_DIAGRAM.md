# Research Agent - Complete Workflow & Architecture Diagram

## 🏗️ **Project Architecture Overview**

```
Research_Agent/
├── 📱 app.py                    # Streamlit Web Application (Entry Point)
├── ⚙️ config.py               # Configuration Management
├── 🤖 research_agent.py       # Main Research Agent (LangGraph Workflow)
├── 📄 document_processor.py   # PDF/HTML Document Processing
├── 🗃️ vector_store.py         # ChromaDB Vector Database Management
├── 🔍 scholar_api.py          # Google Scholar API Integration
├── 🧠 gemini_client.py        # Google Gemini AI Client
├── 🔧 geminiClientWrapper.py  # Alternative Gemini Client Wrapper
├── 🔧 health_check.py         # Logging Setup
├── 🔧 logging_config.py.py    # Logging Configuration (Duplicate)
├── 🧪 test_gemini.py         # Gemini API Tests
├── 🧪 test_full_integration.py # Full Integration Tests
└── 📦 setup.py               # Package Setup
```

---

## 📋 **Complete Workflow - File by File**

### 1. **📱 app.py** - Streamlit Web Application
**Main Entry Point** | **User Interface**

#### Classes:
- `StreamlitApp` - Main application class

#### Key Methods:
```python
StreamlitApp.__init__()                 # Initialize app
StreamlitApp.initialize_agent()         # Setup research agent
StreamlitApp.run()                      # Main app runner
StreamlitApp.render_sidebar()           # Sidebar with stats/controls
StreamlitApp.render_main_content()      # Main query interface
StreamlitApp.process_query(query: str)  # Process user queries
StreamlitApp.display_chat_history()     # Show previous Q&A
StreamlitApp.display_user_message()     # Format user messages
StreamlitApp.display_assistant_message() # Format AI responses
StreamlitApp.display_error_message()    # Error message formatting
StreamlitApp.create_visualizations()    # Generate charts & graphs
StreamlitApp._format_authors()          # Format author names
StreamlitApp._format_authors_list()     # Format author lists
main()                                  # Application entry point
```

#### Dependencies & Calls:
```
→ ResearchAgent (from research_agent.py)
→ config (from config.py)
→ Uses Streamlit, Plotly, Pandas
→ Calls: agent.research(), agent.get_vector_store_stats(), agent.clear_vector_store()
```

---

### 2. **⚙️ config.py** - Configuration Management
**Settings & Environment Variables**

#### Classes:
- `Config` - Configuration dataclass

#### Key Attributes:
```python
Config.GEMINI_API_KEY          # Google Gemini API key
Config.GEMINI_MODEL           # Model name (gemini-2.5-flash)
Config.SERPAPI_KEY            # SerpAPI key for Google Scholar
Config.MAX_RESULTS            # Maximum search results
Config.MAX_TOKENS             # Token limit for AI responses
Config.TEMPERATURE            # AI creativity setting
Config.VECTOR_DB_PATH         # ChromaDB storage path
Config.EMBEDDING_MODEL        # Sentence transformer model
Config.CACHE_DIR              # Document cache directory
Config.CACHE_EXPIRY_HOURS     # Cache expiration time
Config.APP_TITLE              # Application title
Config.APP_DESCRIPTION        # App description
```

#### Key Methods:
```python
Config.validate() -> bool      # Validate required settings
```

#### Dependencies:
```
→ os, dataclasses, dotenv
→ Loads from .env file
```

---

### 3. **🤖 research_agent.py** - Main Research Agent
**Core AI Workflow Engine** | **LangGraph Implementation**

#### Classes:
- `ResearchState` - TypedDict for workflow state
- `QueryRefinementTool` - Query optimization tool  
- `PaperAnalysisTool` - Paper content analysis tool
- `ResearchAgent` - Main agent orchestrator

#### Key Methods:
```python
# ResearchAgent
ResearchAgent.__init__()                    # Initialize all components
ResearchAgent._build_graph() -> StateGraph  # Build LangGraph workflow
ResearchAgent._refine_query()               # Step 1: Optimize search query
ResearchAgent._search_papers()              # Step 2: Find relevant papers
ResearchAgent._process_documents()          # Step 3: Extract paper content
ResearchAgent._extract_context()            # Step 4: Get relevant chunks
ResearchAgent._generate_answer()            # Step 5: Create AI response
ResearchAgent._error_handler()              # Handle workflow errors
ResearchAgent.research(query: str) -> Dict  # Main research function
ResearchAgent.get_vector_store_stats()      # Get database stats
ResearchAgent.clear_vector_store()          # Clear stored documents

# QueryRefinementTool
QueryRefinementTool.__init__(llm)          # Initialize with LLM
QueryRefinementTool.refine_query() -> str  # Optimize search query

# PaperAnalysisTool  
PaperAnalysisTool.__init__(llm)            # Initialize with LLM
PaperAnalysisTool.analyze_paper() -> str   # Analyze paper relevance
```

#### Workflow Steps:
```
1. refine_query    → Optimize user query for academic search
2. search_papers   → Find papers via Google Scholar API
3. process_documents → Download & extract paper content
4. extract_context → Find relevant text chunks
5. generate_answer → Create comprehensive response
6. error_handler   → Handle any workflow failures
```

#### Dependencies & Calls:
```
→ GoogleScholarAPI (from scholar_api.py)
→ DocumentProcessor (from document_processor.py)  
→ VectorStore (from vector_store.py)
→ GeminiClient (from gemini_client.py)
→ config (from config.py)
→ LangGraph, LangChain Core
```

---

### 4. **📄 document_processor.py** - Document Processing
**PDF & HTML Content Extraction**

#### Classes:
- `DocumentChunk` - Data container for text chunks
- `DocumentProcessor` - Main processing engine

#### Key Methods:
```python
# DocumentProcessor
DocumentProcessor.__init__(cache_dir: str)              # Initialize with cache
DocumentProcessor.process_paper(url, title) -> List     # Main processing entry
DocumentProcessor._download_document(url) -> bytes      # Download from URL
DocumentProcessor._process_pdf(content, title) -> List  # Extract from PDF
DocumentProcessor._process_html(content, title) -> List # Extract from HTML  
DocumentProcessor._extract_sections(soup) -> Dict       # Parse HTML sections
DocumentProcessor._clean_text(text: str) -> str         # Clean extracted text
DocumentProcessor._chunk_text(text, max_size) -> List   # Split into chunks
DocumentProcessor._generate_cache_key(url) -> str       # Create cache key
DocumentProcessor._get_from_cache(key) -> List          # Retrieve from cache
DocumentProcessor._save_to_cache(key, chunks)           # Save to cache

# DocumentChunk  
DocumentChunk.text           # The actual text content
DocumentChunk.metadata       # Title, page, section info
DocumentChunk.source         # Original document URL
DocumentChunk.page_number    # Page number (if PDF)
DocumentChunk.section        # Section name (if HTML)
```

#### Processing Flow:
```
URL → Download → [PDF/HTML Detection] → Extract Text → Clean → Chunk → Cache → Return
```

#### Dependencies & Calls:
```
→ PyPDF2, BeautifulSoup4, aiohttp
→ Called by: ResearchAgent._process_documents()
→ Outputs to: VectorStore.add_documents()
```

---

### 5. **🗃️ vector_store.py** - Vector Database Management
**ChromaDB Integration & Semantic Search**

#### Classes:
- `VectorStore` - Main vector database interface

#### Key Methods:
```python
VectorStore.__init__(persist_dir, embedding_model)     # Initialize ChromaDB
VectorStore.add_documents(chunks) -> bool              # Store document chunks
VectorStore.similarity_search(query, k) -> List       # Semantic search
VectorStore.search_by_paper(title, query) -> List     # Search within paper
VectorStore.get_paper_content(title) -> List          # Get all paper content
VectorStore.delete_paper(title) -> bool               # Remove paper data
VectorStore.get_collection_stats() -> Dict            # Database statistics
VectorStore.clear_collection() -> bool                # Clear all data
VectorStore.hybrid_search(query, k) -> List           # Combined search
VectorStore._keyword_search(query, k) -> List         # Keyword matching
VectorStore._combine_search_results() -> List         # Merge search results
```

#### Search Flow:
```
Query → [Semantic + Keyword Search] → Rank Results → Return Top K
```

#### Dependencies & Calls:
```
→ ChromaDB, SentenceTransformers
→ Called by: ResearchAgent (for context extraction)
→ Input from: DocumentProcessor (document chunks)
```

---

### 6. **🔍 scholar_api.py** - Google Scholar Integration
**Academic Paper Discovery**

#### Classes:
- `ScholarResult` - Paper metadata container
- `GoogleScholarAPI` - Scholar search interface

#### Key Methods:
```python
# GoogleScholarAPI
GoogleScholarAPI.__init__(api_key)                    # Initialize with SerpAPI
GoogleScholarAPI.search_papers(query, max) -> List   # Search for papers
GoogleScholarAPI._parse_serpapi_results() -> List    # Parse API response
GoogleScholarAPI.refine_query(query) -> str          # Add academic keywords

# ScholarResult
ScholarResult.title          # Paper title
ScholarResult.authors        # Author list
ScholarResult.abstract       # Paper abstract
ScholarResult.year           # Publication year
ScholarResult.citation_count # Citation count
ScholarResult.pdf_url        # PDF download link
ScholarResult.scholar_url    # Google Scholar page
ScholarResult.venue          # Publication venue
```

#### Search Flow:
```
Query → SerpAPI → Google Scholar → Parse Results → Return ScholarResult[]
```

#### Dependencies & Calls:
```
→ SerpAPI (Google Search API)
→ Called by: ResearchAgent._search_papers()
```

---

### 7. **🧠 gemini_client.py** - Google Gemini AI Client
**AI Language Model Interface**

#### Classes:
- `GeminiClient` - Main Gemini API wrapper

#### Key Methods:
```python
GeminiClient.__init__(api_key, model, temp, tokens)   # Initialize Gemini
GeminiClient.test_connection() -> bool                # Test API access
GeminiClient.get_model_info() -> Dict                 # Model information
GeminiClient.invoke(messages) -> AIMessage           # Generate response
GeminiClient._convert_messages_to_text() -> str      # Format input
GeminiClient.ainvoke(messages) -> AIMessage          # Async version
```

#### AI Flow:
```
Messages → Format → Gemini API → Safety Check → Parse Response → AIMessage
```

#### Dependencies & Calls:
```
→ google.generativeai
→ LangChain Core (for message compatibility)
→ Called by: ResearchAgent (all AI operations)
```

---

### 8. **🔧 geminiClientWrapper.py** - Alternative Client
**Alternative Gemini Implementation**

#### Classes:
- `ChatMessage` - Simple message format
- `GeminiClient` - Alternative implementation
- `ChatPromptTemplate` - Prompt formatting

#### Key Methods:
```python
GeminiClient.invoke(messages) -> ChatMessage          # Sync generation
GeminiClient.ainvoke(messages) -> ChatMessage         # Async generation
GeminiClient.chat(message) -> str                     # Simple chat
GeminiClient.achat(message) -> str                    # Async chat
GeminiClient.get_model_info() -> Dict                 # Model details
GeminiClient.test_connection() -> bool                # Connection test
ChatPromptTemplate.from_template(template)           # Create template
ChatPromptTemplate.format_messages(**kwargs)         # Format with data
```

---

### 9. **🔧 health_check.py & logging_config.py.py** - Logging Setup
**Application Logging Configuration**

#### Functions:
```python
setup_logging(log_level, log_file) -> Logger         # Configure logging
```

#### Logging Setup:
```
Console Handler → File Handler (Rotating) → Logger Configuration
```

---

### 10. **🧪 Test Files** - Quality Assurance

#### **test_gemini.py** - Gemini API Tests
```python
test_gemini_connection()           # Test API connectivity
test_simple_generation()           # Test basic text generation
test_research_query_processing()   # Test query refinement
main()                            # Run all tests
```

#### **test_full_integration.py** - End-to-End Tests
```python
test_research_agent()             # Full workflow test
test_gemini_model_comparison()    # Model comparison
main()                           # Integration test runner
```

---

## 🔄 **Complete Execution Flow**

### **🚀 Application Startup**
```
1. main() in app.py
2. StreamlitApp.__init__()
3. StreamlitApp.initialize_agent()
4. ResearchAgent.__init__()
   ├── GeminiClient.__init__()
   ├── GoogleScholarAPI.__init__()
   ├── DocumentProcessor.__init__()
   ├── VectorStore.__init__()
   └── _build_graph() → LangGraph workflow
```

### **🔍 Query Processing Workflow** 
```
User Query → app.py
    ↓
StreamlitApp.process_query()
    ↓
ResearchAgent.research() → LangGraph Execution:
    ↓
1. _refine_query()
   └── QueryRefinementTool.refine_query()
       └── GeminiClient.invoke()
    ↓
2. _search_papers()
   └── GoogleScholarAPI.search_papers()
       └── SerpAPI → Google Scholar
    ↓
3. _process_documents()
   └── DocumentProcessor.process_paper()
       ├── _download_document()
       ├── _process_pdf() OR _process_html()
       ├── _chunk_text()
       └── VectorStore.add_documents()
    ↓
4. _extract_context()
   └── VectorStore.hybrid_search()
       ├── similarity_search() (semantic)
       └── _keyword_search() (keyword)
    ↓
5. _generate_answer()
   └── GeminiClient.invoke() → Final Response
    ↓
Return to app.py → Display Results
```

---

## 🎯 **Key Components Interaction Map**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│  Research Agent  │────│   Gemini AI     │
│   (app.py)      │    │ (research_agent) │    │ (gemini_client) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         │                        ▼                        │
         │              ┌──────────────────┐               │
         │              │  Google Scholar  │               │
         │              │  (scholar_api)   │               │
         │              └──────────────────┘               │
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Config        │    │ Document Processor│    │  Vector Store   │
│   (config.py)   │    │(document_processor)│   │ (vector_store)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                               │                        │
                               ▼                        │
                    ┌──────────────────┐               │
                    │    Cache         │               │
                    │  (file system)   │               │
                    └──────────────────┘               │
                                                      │
                                         ┌─────────────────┐
                                         │   ChromaDB      │
                                         │   (database)    │
                                         └─────────────────┘
```

---

## 📊 **Technology Stack**

### **🎨 Frontend**
- **Streamlit** - Web interface
- **Plotly** - Data visualizations  
- **Pandas** - Data manipulation

### **🤖 AI & ML**
- **Google Gemini 2.5 Flash** - Language model
- **SentenceTransformers** - Text embeddings
- **LangGraph** - Workflow orchestration
- **LangChain Core** - AI framework components

### **🔍 Search & Data**
- **SerpAPI** - Google Scholar access
- **ChromaDB** - Vector database
- **PyPDF2** - PDF processing
- **BeautifulSoup4** - HTML parsing
- **aiohttp** - Async HTTP requests

### **🔧 Infrastructure**
- **Python 3.11+** - Runtime
- **asyncio** - Async programming
- **dotenv** - Environment management
- **logging** - Application logging

---

## 🎯 **Summary**

This Research Agent is a **sophisticated AI-powered academic research assistant** that:

1. **🎨 Provides** an intuitive Streamlit web interface
2. **🔍 Searches** Google Scholar for relevant academic papers
3. **📄 Processes** PDF and HTML documents automatically  
4. **🧠 Uses** Google Gemini AI for intelligent query processing
5. **🗃️ Stores** document embeddings in a vector database
6. **🤖 Generates** comprehensive, citation-backed responses
7. **📊 Visualizes** research insights with interactive charts

The architecture follows **modern best practices** with clear separation of concerns, async processing, comprehensive error handling, and extensive testing coverage.
