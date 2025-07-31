#!/usr/bin/env python3
"""
Health check module for Research Agent Bot
"""

import asyncio
import logging
import sys
from typing import Dict, Any, Optional
from datetime import datetime

from config import config
from gemini_client import GeminiClient
from vector_store import VectorStore
from scholar_api import GoogleScholarAPI

logger = logging.getLogger(__name__)

class HealthChecker:
    """Health checker for the Research Agent Bot"""
    
    def __init__(self):
        self.checks = {
            'gemini_api': self._check_gemini_api,
            'vector_store': self._check_vector_store,
            'scholar_api': self._check_scholar_api,
            'config': self._check_config
        }
    
    async def check_all(self) -> Dict[str, Any]:
        """Run all health checks"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy',
            'checks': {}
        }
        
        for check_name, check_func in self.checks.items():
            try:
                result = await check_func()
                results['checks'][check_name] = result
                
                if not result['healthy']:
                    results['status'] = 'unhealthy'
                    
            except Exception as e:
                results['checks'][check_name] = {
                    'healthy': False,
                    'error': str(e),
                    'message': f"Health check failed: {e}"
                }
                results['status'] = 'unhealthy'
        
        return results
    
    async def _check_gemini_api(self) -> Dict[str, Any]:
        """Check Gemini API connectivity"""
        try:
            if not config.GEMINI_API_KEY:
                return {
                    'healthy': False,
                    'message': 'Gemini API key not configured'
                }
            
            client = GeminiClient(
                api_key=config.GEMINI_API_KEY,
                model=config.GEMINI_MODEL
            )
            
            is_connected = client.test_connection()
            
            return {
                'healthy': is_connected,
                'message': 'Gemini API connection successful' if is_connected else 'Gemini API connection failed',
                'model': config.GEMINI_MODEL
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e),
                'message': f'Gemini API check failed: {e}'
            }
    
    async def _check_vector_store(self) -> Dict[str, Any]:
        """Check vector store connectivity"""
        try:
            vector_store = VectorStore(
                persist_directory=config.VECTOR_DB_PATH,
                embedding_model=config.EMBEDDING_MODEL
            )
            
            # Try to get collection stats
            stats = vector_store.get_collection_stats()
            
            return {
                'healthy': True,
                'message': 'Vector store connection successful',
                'stats': stats,
                'path': config.VECTOR_DB_PATH
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e),
                'message': f'Vector store check failed: {e}'
            }
    
    async def _check_scholar_api(self) -> Dict[str, Any]:
        """Check Scholar API connectivity"""
        try:
            if not config.SERPAPI_KEY:
                return {
                    'healthy': False,
                    'message': 'SerpAPI key not configured'
                }
            
            scholar_api = GoogleScholarAPI(config.SERPAPI_KEY)
            
            # Try a simple search
            results = await scholar_api.search_papers("machine learning", max_results=1)
            
            return {
                'healthy': len(results) >= 0,  # Even 0 results is OK for health check
                'message': 'Scholar API connection successful',
                'test_results_count': len(results)
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e),
                'message': f'Scholar API check failed: {e}'
            }
    
    async def _check_config(self) -> Dict[str, Any]:
        """Check configuration validity"""
        try:
            config.validate()
            
            return {
                'healthy': True,
                'message': 'Configuration is valid',
                'config': {
                    'gemini_model': config.GEMINI_MODEL,
                    'max_results': config.MAX_RESULTS,
                    'temperature': config.TEMPERATURE,
                    'vector_db_path': config.VECTOR_DB_PATH,
                    'embedding_model': config.EMBEDDING_MODEL
                }
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'error': str(e),
                'message': f'Configuration check failed: {e}'
            }

async def main():
    """Main health check function for CLI usage"""
    logging.basicConfig(level=logging.INFO)
    
    checker = HealthChecker()
    results = await checker.check_all()
    
    # Print results
    print(f"Health Check Results - {results['timestamp']}")
    print(f"Overall Status: {results['status'].upper()}")
    print("-" * 50)
    
    for check_name, check_result in results['checks'].items():
        status = "✅ HEALTHY" if check_result['healthy'] else "❌ UNHEALTHY"
        print(f"{check_name}: {status}")
        print(f"  Message: {check_result['message']}")
        
        if 'error' in check_result:
            print(f"  Error: {check_result['error']}")
        
        if 'stats' in check_result:
            print(f"  Stats: {check_result['stats']}")
        
        print()
    
    # Exit with appropriate code
    sys.exit(0 if results['status'] == 'healthy' else 1)

if __name__ == "__main__":
    asyncio.run(main())
