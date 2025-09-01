# ============================================================================
# COMPLETE FIXED RAG SYSTEM - INCLUDES AUTHORS AND ALL PAPERS
# ============================================================================

# Install required packages first
# !pip install sentence-transformers faiss-cpu

import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from IPython.display import display, HTML
import pandas as pd
from neo4j import GraphDatabase
import os
from datetime import datetime

# ============================================================================
# CELL: Test Your Knowledge Graph Connection
# ============================================================================

def check_kg_status():
    try:
        kg = BirminghamKG(database="neo4j")
        stats = kg.get_statistics()
        
        print("Current Knowledge Graph Status:")
        for key, value in stats.items():
            print(f"   {key.replace('_', ' ').title()}: {value:,}")
        
        kg.close()
        return stats['total_nodes'] > 0
        
    except Exception as e:
        print(f"Error connecting to Neo4j: {e}")
        print("Make sure Neo4j is running on localhost:7687")
        return False

# ============================================================================
# FIXED RAG SYSTEM CLASS
# ============================================================================

class FixedAcademicRAGSystem:
    def __init__(self, neo4j_uri="neo4j://127.0.0.1:7687", 
                 neo4j_user="neo4j", neo4j_password="12345678", 
                 database="neo4j"):
        
        # Neo4j connection
        try:
            self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
            self.database = database
            
            # Test connection
            with self.driver.session(database=self.database) as session:
                session.run("RETURN 1").single()
            
            print("Connected to Neo4j successfully!")
            
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")
            return
        
        # Embedding model for semantic search
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # FAISS index components
        self.faiss_index = None
        self.document_embeddings = {}
        self.index_to_doc_id = {}
        self.doc_id_to_index = {}
        
        print("Fixed Academic RAG System initialized!")
    
    def get_session(self):
        return self.driver.session(database=self.database)
    
    def diagnose_database(self):
        """Diagnose what's in the database"""
        queries = [
            ("Total papers", "MATCH (d:Document) RETURN count(d) as count"),
            ("Papers with abstracts", "MATCH (d:Document) WHERE d.abstract IS NOT NULL AND d.abstract <> '' RETURN count(d) as count"),
            ("Papers without abstracts", "MATCH (d:Document) WHERE d.abstract IS NULL OR d.abstract = '' RETURN count(d) as count"),
            ("CS-related papers", """MATCH (d:Document) 
               WHERE toLower(d.title) CONTAINS 'computer' 
               OR toLower(d.title) CONTAINS 'machine learning'
               OR toLower(d.title) CONTAINS 'algorithm'
               OR toLower(d.title) CONTAINS 'software'
               OR toLower(d.title) CONTAINS 'AI'
               OR toLower(d.title) CONTAINS 'artificial intelligence'
               OR toLower(d.title) CONTAINS 'neural'
               OR toLower(d.title) CONTAINS 'deep learning'
               RETURN count(d) as count"""),
            ("Authors", "MATCH (a:Author) RETURN count(a) as count"),
            ("Affiliations", "MATCH (af:Affiliation) RETURN count(af) as count")
        ]
        
        print("Database Diagnosis:")
        print("=" * 40)
        
        with self.get_session() as session:
            for label, query in queries:
                try:
                    result = session.run(query).single()
                    count = result['count']
                    print(f"{label}: {count:,}")
                except Exception as e:
                    print(f"{label}: Error - {e}")
        
        # Sample CS papers
        cs_sample_query = """
        MATCH (d:Document) 
        WHERE toLower(d.title) CONTAINS 'machine learning'
        OR toLower(d.title) CONTAINS 'computer'
        RETURN d.title, d.year, d.citation_count
        ORDER BY d.citation_count DESC
        LIMIT 5
        """
        
        print(f"\nSample CS Papers:")
        with self.get_session() as session:
            result = session.run(cs_sample_query)
            for i, record in enumerate(result, 1):
                title = record['d.title'][:60] + "..." if len(record['d.title']) > 60 else record['d.title']
                print(f"  {i}. {title} ({record['d.year']}) - {record['d.citation_count']} citations")
    
    def build_document_embeddings_fixed(self):
        """FIXED: Build embeddings that include ALL papers (including CS papers)"""
        print("Building document embeddings (FIXED VERSION)...")
        
        # More inclusive query - no citation ordering, includes all papers
        query = """
        MATCH (d:Document)
        WHERE d.title IS NOT NULL AND d.title <> ''
        RETURN d.document_id as doc_id, d.title as title, 
               d.abstract as abstract, d.year as year,
               d.citation_count as citations
        ORDER BY d.document_id
        """
        
        documents = []
        doc_metadata = {}
        skipped = 0
        
        with self.get_session() as session:
            result = session.run(query)
            for record in result:
                doc_id = record['doc_id']
                title = record['title'] or ""
                abstract = record['abstract'] or ""
                
                # More lenient filtering - just need a title
                if title.strip():
                    # Use title, add abstract if available
                    text_content = title
                    if abstract and abstract.strip():
                        text_content = f"{title}. {abstract}"
                    
                    documents.append(text_content)
                    doc_metadata[len(documents)-1] = {
                        'doc_id': doc_id,
                        'title': title,
                        'abstract': abstract,
                        'year': record['year'],
                        'citations': record['citations'] or 0
                    }
                else:
                    skipped += 1
        
        print(f"Processed {len(documents):,} documents, skipped {skipped}")
        
        if not documents:
            print("No documents found in Neo4j!")
            return
        
        print(f"Generating embeddings for {len(documents):,} documents...")
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(documents, show_progress_bar=True)
        
        # Build FAISS index
        dimension = embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatIP(dimension)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        self.faiss_index.add(embeddings.astype(np.float32))
        
        # Store mappings
        for idx, metadata in doc_metadata.items():
            doc_id = metadata['doc_id']
            self.index_to_doc_id[idx] = doc_id
            self.doc_id_to_index[doc_id] = idx
            self.document_embeddings[doc_id] = metadata
        
        print(f"Built FAISS index with {len(documents):,} documents")
        
        # Test CS paper inclusion
        cs_test = [doc for doc in documents if any(term in doc.lower() for term in ['machine learning', 'computer', 'algorithm', 'artificial intelligence'])]
        print(f"CS-related papers in index: {len(cs_test):,}")
    
    def semantic_search_with_authors(self, query: str, top_k: int = 10):
        """FIXED: Semantic search that includes author information"""
        if self.faiss_index is None:
            print("FAISS index not built! Run build_document_embeddings_fixed() first")
            return []
        
        # Encode query
        query_embedding = self.embedding_model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.faiss_index.search(query_embedding.astype(np.float32), top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:
                doc_id = self.index_to_doc_id[idx]
                doc_info = self.document_embeddings[doc_id].copy()
                doc_info['similarity_score'] = float(score)
                
                # GET AUTHORS FROM NEO4J
                author_query = """
                MATCH (d:Document {document_id: $doc_id})<-[:AUTHOR_OF]-(a:Author)
                OPTIONAL MATCH (a)-[:AFFILIATED_WITH]->(af:Affiliation)
                RETURN collect(DISTINCT a.full_name)[0..5] as authors,
                       collect(DISTINCT af.name)[0] as main_affiliation
                """
                
                try:
                    with self.get_session() as session:
                        result = session.run(author_query, doc_id=doc_id)
                        record = result.single()
                        
                        if record:
                            doc_info['authors'] = record['authors'] if record['authors'] else []
                            doc_info['main_affiliation'] = record['main_affiliation']
                        else:
                            doc_info['authors'] = []
                            doc_info['main_affiliation'] = None
                            
                except Exception as e:
                    print(f"Error getting authors for {doc_id}: {e}")
                    doc_info['authors'] = []
                    doc_info['main_affiliation'] = None
                
                results.append(doc_info)
        
        return results
    
    def display_results_with_authors(self, results, query=""):
        """FIXED: Display results with author information"""
        if not results:
            display(HTML("<h3>No results found</h3>"))
            return
        
        display(HTML(f"""
        <h3>Search Results for: "{query}"</h3>
        <p><strong>Found:</strong> {len(results)} documents</p>
        """))
        
        for i, doc in enumerate(results, 1):
            title = doc.get('title', 'No Title')
            if len(title) > 100:
                title = title[:100] + "..."
            
            abstract = doc.get('abstract', 'No abstract')
            if len(abstract) > 300:
                abstract = abstract[:300] + "..."
            
            similarity = doc.get('similarity_score', 0)
            year = doc.get('year', 'N/A')
            citations = doc.get('citations', 0)
            authors = doc.get('authors', [])
            affiliation = doc.get('main_affiliation', '')
            
            # Format authors
            if authors:
                author_str = ', '.join(authors[:3])
                if len(authors) > 3:
                    author_str += f" + {len(authors) - 3} more"
            else:
                author_str = "Authors not available"
            
            affiliation_str = f"<p><strong>Institution:</strong> {affiliation}</p>" if affiliation else ""
            
            display(HTML(f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <h4 style="margin: 0 0 10px 0;">{i}. {title}</h4>
                <p><strong>Authors:</strong> {author_str}</p>
                {affiliation_str}
                <p><strong>Year:</strong> {year} | <strong>Citations:</strong> {citations} | 
                   <strong>Similarity:</strong> {similarity:.3f}</p>
                <p><strong>Abstract:</strong> {abstract}</p>
            </div>
            """))
    
    # Convenience methods
    def build_document_embeddings(self):
        """Redirect to fixed version"""
        return self.build_document_embeddings_fixed()
    
    def semantic_search(self, query: str, top_k: int = 10):
        """Redirect to fixed version"""
        return self.semantic_search_with_authors(query, top_k)
    
    def display_results(self, results, query=""):
        """Redirect to fixed version"""
        return self.display_results_with_authors(results, query)
    
    def close(self):
        if self.driver:
            self.driver.close()

# ============================================================================
# INITIALIZE FIXED SYSTEM
# ============================================================================

print("Fixed RAG System Class ready!")

# Initialize your FIXED RAG system
rag = FixedAcademicRAGSystem()

# ============================================================================
# DIAGNOSTIC AND BUILD FUNCTIONS
# ============================================================================

def run_diagnosis_and_build():
    """Run diagnosis then build embeddings"""
    
    # Step 1: Diagnose database
    print("STEP 1: Diagnosing database...")
    rag.diagnose_database()
    
    # Step 2: Build embeddings with fixed method
    print(f"\nSTEP 2: Building embeddings...")
    rag.build_document_embeddings_fixed()
    
    print(f"\nFixed RAG system ready for testing!")

# ============================================================================
# FIXED SEARCH FUNCTION
# ============================================================================

def search_papers_fixed(query, top_k=5):
    """Fixed search function that shows authors"""
    print(f"Searching for: '{query}'")
    results = rag.semantic_search_with_authors(query, top_k)
    rag.display_results_with_authors(results, query)
    return results

print("Fixed search function ready!")

# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def test_cs_papers():
    """Test computer science paper retrieval"""
    cs_queries = [
        "machine learning algorithms",
        "computer science artificial intelligence", 
        "deep learning neural networks",
        "software engineering",
        "data mining"
    ]
    
    print("Testing Computer Science Paper Retrieval:")
    print("=" * 50)
    
    for query in cs_queries:
        print(f"\nQuery: '{query}'")
        results = rag.semantic_search_with_authors(query, 3)
        
        if results:
            print(f"Found {len(results)} results:")
            for i, doc in enumerate(results, 1):
                title = doc.get('title', 'No title')[:60] + "..."
                authors = doc.get('authors', [])
                similarity = doc.get('similarity_score', 0)
                print(f"  {i}. {title}")
                print(f"     Authors: {authors[:2] if authors else 'No authors'}")
                print(f"     Similarity: {similarity:.3f}")
        else:
            print("  No results found")
        print("-" * 30)

def test_author_information():
    """Test author information retrieval"""
    queries = [
        "researchers in AI at Birmingham",
        "machine learning healthcare authors",
        "computer vision Birmingham"
    ]
    
    print("Testing Author Information Retrieval:")
    print("=" * 50)
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = rag.semantic_search_with_authors(query, 5)
        
        authors_found = 0
        for doc in results:
            if doc.get('authors'):
                authors_found += 1
        
        print(f"Results with author info: {authors_found}/{len(results)}")
        
        if results:
            print("Sample results:")
            for i, doc in enumerate(results[:2], 1):
                title = doc.get('title', 'No title')[:50] + "..."
                authors = doc.get('authors', [])
                print(f"  {i}. {title}")
                print(f"     Authors: {', '.join(authors[:3]) if authors else 'No authors found'}")
        print("-" * 30)

def run_complete_test():
    """Run all tests"""
    print("RUNNING COMPLETE SYSTEM TEST")
    print("=" * 60)
    
    # Test 1: CS papers
    test_cs_papers()
    
    print(f"\n" + "=" * 60)
    
    # Test 2: Author information  
    test_author_information()
    
    print(f"\n" + "=" * 60)
    print("COMPLETE TEST FINISHED!")

# ============================================================================
# USAGE INSTRUCTIONS
# ============================================================================

print("""
USAGE INSTRUCTIONS:
==================

1. Run diagnosis and build embeddings:
   run_diagnosis_and_build()

2. Test the fixes:
   run_complete_test()

3. Use for searches:
   search_papers_fixed('your query', 5)

4. Check specific CS papers:
   test_cs_papers()

5. Check author information:
   test_author_information()

The fixed system should now:
- Include ALL papers (including CS papers)
- Show author information for each result
- Handle papers without abstracts
- Not bias towards highly-cited papers only
""")