# 📚 Research Agent

An intelligent research assistant that helps you find, analyze, and synthesize information from academic papers using AI-powered search and analysis.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.0.350+-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)

## 🌟 Features

- **Intelligent Query Refinement**: Automatically refines user questions for optimal academic search results
- **Academic Paper Search**: Integrates with Google Scholar API to find relevant research papers
- **Document Processing**: Downloads and processes PDF papers for content extraction
- **Vector Storage**: Stores processed documents in a vector database for efficient retrieval
- **AI-Powered Analysis**: Uses advanced language models to analyze papers and generate comprehensive answers
- **Interactive Web Interface**: Beautiful Streamlit-based UI with real-time search and visualization
- **Chat History**: Maintains conversation history for context-aware responses
- **System Monitoring**: Real-time statistics and health monitoring

## 🏗️ Architecture

The Research Agent is built using a **LangGraph-based workflow** that orchestrates the following components:

1. **Query Refinement**: Converts user questions into effective academic search queries
2. **Paper Search**: Searches Google Scholar for relevant research papers
3. **Document Processing**: Downloads and extracts content from PDF papers
4. **Vector Storage**: Stores processed content in ChromaDB for similarity search
5. **Context Extraction**: Retrieves relevant information based on the user query
6. **Answer Generation**: Synthesizes findings into comprehensive, well-sourced answers

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Research_Agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4
   TEMPERATURE=0.1
   MAX_TOKENS=4000
   MAX_RESULTS=10
   CACHE_DIR=./files
   VECTOR_DB_PATH=./vector_db
   EMBEDDING_MODEL=all-MiniLM-L6-v2
   APP_TITLE=Research Agent
   APP_DESCRIPTION=AI-Powered Academic Research Assistant
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the web interface**
   Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
Research_Agent/
├── .venv/                      # Virtual environment
├── files/                      # Document cache
├── tests/                      # Test files
├── vector_db/                  # Vector database storage
├── .env                        # Environment variables
├── .gitignore                  # Git ignore file
├── app.py                      # Streamlit web application
├── config.py                   # Configuration management
├── dev.ipynb                   # Development notebook
├── docker-compose.yaml         # Docker compose configuration
├── dockerfile                  # Docker container definition
├── document_processor.py       # PDF processing and text extraction
├── health_check.py             # System health monitoring
├── logging_config.py.py        # Logging configuration
├── Makerfile                   # Make commands
├── requirements.txt            # Python dependencies
├── research_agent.py           # Main agent logic with LangGraph
├── scholar_api.py              # Google Scholar API integration
├── setup.py                    # Package setup
└── vector_store.py             # Vector database operations
```

## 💻 Usage

### Web Interface

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Ask research questions** such as:
   - "What are the latest developments in transformer architectures?"
   - "How does climate change affect biodiversity in marine ecosystems?"
   - "What are the most effective methods for few-shot learning?"
   - "Recent advances in quantum computing error correction"

3. **View results** with:
   - Comprehensive answers based on multiple research papers
   - Source citations and references
   - Visual statistics and system status
   - Chat history for context

## 🔧 Configuration

Key configuration options in your `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4` |
| `TEMPERATURE` | Response creativity (0.0-1.0) | `0.1` |
| `MAX_RESULTS` | Maximum papers to analyze | `10` |
| `CACHE_DIR` | Directory for cached documents | `./files` |
| `VECTOR_DB_PATH` | Vector database storage path | `./vector_db` |

## 🐳 Docker Support

Run with Docker Compose:

```bash
docker-compose up -d
```

Or build and run manually:

```bash
docker build -t research-agent .
docker run -p 8501:8501 --env-file .env research-agent
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=.

# Run specific test file
python -m pytest tests/test_research_agent.py
```

## 📊 Monitoring

The application includes built-in health monitoring and system statistics:

- **Document Statistics**: Total documents, unique papers, processing status
- **Vector Store Metrics**: Storage utilization, search performance
- **API Health**: OpenAI API status, rate limiting information
- **Error Tracking**: Comprehensive error logging and reporting

Access health check endpoint:
```bash
python health_check.py
```

## 🛠️ Development

### Setting up development environment

1. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Making Changes

1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Run the test suite
5. Submit a pull request

## 📚 Dependencies

Key dependencies and their purposes:

- **LangChain**: Framework for building LLM applications
- **LangGraph**: Orchestration of multi-step AI workflows
- **Streamlit**: Web application framework
- **OpenAI**: Language model API
- **ChromaDB**: Vector database for document storage
- **Beautiful Soup**: Web scraping and HTML parsing
- **PyPDF2**: PDF processing and text extraction
- **Sentence Transformers**: Text embedding models

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.



