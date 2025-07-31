import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from research_agent import ResearchAgent, ResearchState
from scholar_api import ScholarResult
from document_processor import DocumentChunk

class TestResearchAgent:
    """Test suite for ResearchAgent"""
    
    @pytest.fixture
    def mock_config(self):
        with patch('research_agent.config') as mock_config:
            mock_config.OPENAI_MODEL = "gpt-4-turbo-preview"
            mock_config.TEMPERATURE = 0.3
            mock_config.MAX_TOKENS = 4000
            mock_config.CACHE_DIR = "./test_cache"
            mock_config.VECTOR_DB_PATH = "./test_chroma_db"
            mock_config.EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
            mock_config.MAX_RESULTS = 10
            yield mock_config
    
    @pytest.fixture
    def mock_research_agent(self, mock_config):
        with patch('research_agent.ChatOpenAI'), \
             patch('research_agent.GoogleScholarAPI'), \
             patch('research_agent.DocumentProcessor'), \
             patch('research_agent.VectorStore'):
            agent = ResearchAgent()
            return agent
    
    @pytest.fixture
    def sample_scholar_results(self):
        return [
            ScholarResult(
                title="Sample Paper 1",
                authors=["John Doe", "Jane Smith"],
                abstract="This is a sample abstract",
                year=2023,
                citation_count=50,
                pdf_url="https://example.com/paper1.pdf",
                scholar_url="https://scholar.google.com/paper1",
                venue="Conference A"
            ),
            ScholarResult(
                title="Sample Paper 2",
                authors=["Alice Johnson"],
                abstract="Another sample abstract",
                year=2024,
                citation_count=25,
                pdf_url="https://example.com/paper2.pdf",
                scholar_url="https://scholar.google.com/paper2",
                venue="Journal B"
            )
        ]
    
    @pytest.fixture
    def sample_document_chunks(self):
        return [
            DocumentChunk(
                text="This is the first chunk of text from the paper.",
                metadata={
                    'title': 'Sample Paper',
                    'page': 1,
                    'chunk_id': 'page_1_chunk_0'
                },
                source="https://example.com/paper.pdf",
                page_number=1
            ),
            DocumentChunk(
                text="This is the second chunk of text from the paper.",
                metadata={
                    'title': 'Sample Paper',
                    'page': 1,
                    'chunk_id': 'page_1_chunk_1'
                },
                source="https://example.com/paper.pdf",
                page_number=1
            )
        ]
    
    def test_research_agent_initialization(self, mock_research_agent):
        """Test that ResearchAgent initializes correctly"""
        assert mock_research_agent.llm is not None
        assert mock_research_agent.scholar_api is not None
        assert mock_research_agent.document_processor is not None
        assert mock_research_agent.vector_store is not None
        assert mock_research_agent.graph is not None
    
    @pytest.mark.asyncio
    async def test_refine_query(self, mock_research_agent):
        """Test query refinement"""
        # Mock the LLM response
        mock_response = Mock()
        mock_response.content = "refined machine learning algorithms"
        mock_research_agent.llm.invoke = Mock(return_value=mock_response)
        
        state = ResearchState(
            original_query="machine learning",
            refined_query="",
            search_results=[],
            processed_documents=[],
            context_chunks=[],
            final_answer="",
            error=None,
            step="initialized"
        )
        
        result = await mock_research_agent._refine_query(state)
        
        assert result['refined_query'] == "refined machine learning algorithms"
        assert result['step'] == "query_refined"
        assert result['error'] is None
    
    @pytest.mark.asyncio
    async def test_search_papers(self, mock_research_agent, sample_scholar_results):
        """Test paper search functionality"""
        # Mock scholar API
        mock_research_agent.scholar_api.search_papers = AsyncMock(return_value=sample_scholar_results)
        
        state = ResearchState(
            original_query="machine learning",
            refined_query="machine learning algorithms",
            search_results=[],
            processed_documents=[],
            context_chunks=[],
            final_answer="",
            error=None,
            step="query_refined"
        )
        
        result = await mock_research_agent._search_papers(state)
        
        assert len(result['search_results']) == 2
        assert result['step'] == "papers_found"
        assert result['error'] is None
    
    @pytest.mark.asyncio
    async def test_process_documents(self, mock_research_agent, sample_scholar_results, sample_document_chunks):
        """Test document processing"""
        # Mock document processor
        mock_research_agent.document_processor.process_paper = AsyncMock(return_value=sample_document_chunks)
        mock_research_agent.vector_store.add_documents = Mock(return_value=True)
        
        state = ResearchState(
            original_query="machine learning",
            refined_query="machine learning algorithms",
            search_results=sample_scholar_results,
            processed_documents=[],
            context_chunks=[],
            final_answer="",
            error=None,
            step="papers_found"
        )
        
        result = await mock_research_agent._process_documents(state)
        
        assert len(result['processed_documents']) == 2
        assert result['step'] == "documents_processed"
        assert result['error'] is None
    
    @pytest.mark.asyncio
    async def test_extract_context(self, mock_research_agent):
        """Test context extraction"""
        # Mock vector store search
        mock_results = [
            ("This is relevant text", {"title": "Sample Paper"}, 0.8),
            ("Another relevant text", {"title": "Another Paper"}, 0.7)
        ]
        mock_research_agent.vector_store.hybrid_search = Mock(return_value=mock_results)
        
        state = ResearchState(
            original_query="machine learning",
            refined_query="machine learning algorithms",
            search_results=[],
            processed_documents=["Sample Paper", "Another Paper"],
            context_chunks=[],
            final_answer="",
            error=None,
            step="documents_processed"
        )
        
        result = await mock_research_agent._extract_context(state)
        
        assert len(result['context_chunks']) == 2
        assert result['step'] == "context_extracted"
        assert result['error'] is None
    
    @pytest.mark.asyncio
    async def test_generate_answer(self, mock_research_agent):
        """Test answer generation"""
        # Mock LLM response
        mock_response = Mock()
        mock_response.content = "Based on the research papers, machine learning algorithms have evolved significantly..."
        mock_research_agent.llm.invoke = Mock(return_value=mock_response)
        
        state = ResearchState(
            original_query="machine learning",
            refined_query="machine learning algorithms",
            search_results=[],
            processed_documents=[],
            context_chunks=[
                {
                    'text': 'Machine learning has advanced',
                    'metadata': {'title': 'ML Paper'},
                    'score': 0.8
                }
            ],
            final_answer="",
            error=None,
            step="context_extracted"
        )
        
        result = await mock_research_agent._generate_answer(state)
        
        assert "machine learning algorithms have evolved" in result['final_answer']
        assert result['step'] == "answer_generated"
        assert result['error'] is None
    
    @pytest.mark.asyncio
    async def test_full_research_workflow(self, mock_research_agent, sample_scholar_results, sample_document_chunks):
        """Test the full research workflow"""
        # Mock all components
        mock_research_agent.query_refinement_tool._run = Mock(return_value="refined ML query")
        mock_research_agent.scholar_api.search_papers = AsyncMock(return_value=sample_scholar_results)
        mock_research_agent.document_processor.process_paper = AsyncMock(return_value=sample_document_chunks)
        mock_research_agent.vector_store.add_documents = Mock(return_value=True)
        mock_research_agent.vector_store.hybrid_search = Mock(return_value=[
            ("ML content", {"title": "ML Paper"}, 0.9)
        ])
        
        mock_response = Mock()
        mock_response.content = "Machine learning is a fascinating field..."
        mock_research_agent.llm.invoke = Mock(return_value=mock_response)
        
        result = await mock_research_agent.research("What is machine learning?")
        
        assert result['status'] == 'success'
        assert result['query'] == "What is machine learning?"
        assert len(result['sources']) == 2
        assert len(result['processed_papers']) == 2
        assert result['context_chunks_count'] == 1
        assert "Machine learning is a fascinating field" in result['answer']
    
    @pytest.mark.asyncio
    async def test_error_handling(self, mock_research_agent):
        """Test error handling in research workflow"""
        # Mock an error in the scholar API
        mock_research_agent.scholar_api.search_papers = AsyncMock(side_effect=Exception("API Error"))
        
        result = await mock_research_agent.research("test query")
        
        assert result['status'] == 'error'
        assert 'API Error' in result['error']
        assert result['sources'] == []
        assert result['processed_papers'] == []
    
    def test_get_vector_store_stats(self, mock_research_agent):
        """Test getting vector store statistics"""
        mock_stats = {
            'total_chunks': 100,
            'unique_papers': 10,
            'papers': ['Paper 1', 'Paper 2']
        }
        mock_research_agent.vector_store.get_collection_stats = Mock(return_value=mock_stats)
        
        stats = mock_research_agent.get_vector_store_stats()
        
        assert stats['total_chunks'] == 100
        assert stats['unique_papers'] == 10
        assert len(stats['papers']) == 2
    
    def test_clear_vector_store(self, mock_research_agent):
        """Test clearing vector store"""
        mock_research_agent.vector_store.clear_collection = Mock(return_value=True)
        
        result = mock_research_agent.clear_vector_store()
        
        assert result is True
        mock_research_agent.vector_store.clear_collection.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])