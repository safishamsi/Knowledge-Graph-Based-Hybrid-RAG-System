# ============================================================================
# ADVANCED RESEARCH ASSISTANT - RESEARCHER RECOMMENDATIONS & ENHANCED QUERIES
# ============================================================================

import re
from collections import defaultdict, Counter
from datetime import datetime
import json

class AdvancedResearchAssistant:
    def __init__(self, rag_system):
        self.rag = rag_system
        
        # Domain mapping for better query understanding
        self.domain_keywords = {
            'machine_learning': ['machine learning', 'deep learning', 'neural network', 'artificial intelligence', 'AI'],
            'medical': ['medical', 'healthcare', 'clinical', 'disease', 'cancer', 'diagnosis', 'treatment'],
            'computer_vision': ['computer vision', 'image processing', 'CT scan', 'medical imaging'],
            'nlp': ['natural language processing', 'NLP', 'text mining', 'language model'],
            'robotics': ['robotics', 'autonomous', 'robot', 'automation'],
            'energy': ['energy', 'smart grid', 'renewable', 'solar', 'wind'],
            'genetics': ['genetic', 'genomics', 'biomarker', 'gene expression', 'DNA'],
            'blockchain': ['blockchain', 'cryptocurrency', 'distributed ledger'],
            'climate': ['climate', 'weather', 'environmental', 'satellite'],
            'neuroscience': ['brain', 'neural', 'cognitive', 'neuroscience', 'BCI', 'brain-computer']
        }
        
        # Method keywords
        self.method_keywords = {
            'deep_learning': ['deep learning', 'convolutional', 'CNN', 'RNN', 'transformer'],
            'reinforcement_learning': ['reinforcement learning', 'RL', 'Q-learning', 'policy gradient'],
            'graph_neural_networks': ['graph neural network', 'GNN', 'graph convolution'],
            'interpretability': ['interpretable', 'explainable', 'interpretability', 'XAI'],
            'privacy': ['privacy', 'differential privacy', 'federated learning', 'secure']
        }
        
    def extract_research_components(self, query):
        """Extract methodology, domain, and constraints from research query"""
        query_lower = query.lower()
        
        # Extract domains
        domains = []
        for domain, keywords in self.domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                domains.append(domain)
        
        # Extract methods
        methods = []
        for method, keywords in self.method_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                methods.append(method)
        
        # Extract constraints/requirements
        constraints = []
        constraint_patterns = [
            'interpretability', 'interpretable', 'explainable',
            'false positive', 'accuracy', 'precision',
            'privacy-preserving', 'real-time', 'scalable'
        ]
        
        for pattern in constraint_patterns:
            if pattern in query_lower:
                constraints.append(pattern)
        
        return {
            'domains': domains,
            'methods': methods,
            'constraints': constraints,
            'original_query': query
        }
    
    def find_birmingham_researchers(self, research_area, top_k=10):
        """Find Birmingham researchers specializing in a research area"""
        
        print(f"Finding Birmingham researchers for: {research_area}")
        print("=" * 60)
        
        # Step 1: Find relevant papers
        papers = self.rag.semantic_search_with_authors(research_area, top_k=50)
        
        # Step 2: Extract Birmingham authors and their metrics
        author_metrics = defaultdict(lambda: {
            'name': '',
            'papers': [],
            'total_citations': 0,
            'paper_count': 0,
            'recent_papers': 0,
            'avg_citations': 0,
            'main_affiliation': '',
            'collaboration_count': 0
        })
        
        birmingham_affiliations = [
            'university of birmingham', 'birmingham business school',
            'college of social sciences', 'birmingham medical school'
        ]
        
        for paper in papers:
            authors = paper.get('authors', [])
            affiliation = paper.get('main_affiliation', '').lower()
            
            # Check if this is a Birmingham paper
            is_birmingham = any(bham in affiliation for bham in birmingham_affiliations)
            
            if is_birmingham and authors:
                year = paper.get('year', 0)
                citations = paper.get('citations', 0)
                
                for author_name in authors:
                    if author_name:  # Skip empty names
                        metrics = author_metrics[author_name]
                        metrics['name'] = author_name
                        metrics['papers'].append({
                            'title': paper.get('title', ''),
                            'year': year,
                            'citations': citations,
                            'similarity': paper.get('similarity_score', 0)
                        })
                        metrics['total_citations'] += citations
                        metrics['paper_count'] += 1
                        metrics['main_affiliation'] = paper.get('main_affiliation', '')
                        
                        # Count recent papers (last 5 years)
                        if year and year >= 2019:
                            metrics['recent_papers'] += 1
        
        # Step 3: Calculate final scores and rank
        researcher_scores = []
        
        for author_name, metrics in author_metrics.items():
            if metrics['paper_count'] > 0:
                metrics['avg_citations'] = metrics['total_citations'] / metrics['paper_count']
                
                # Calculate composite score
                score = (
                    metrics['paper_count'] * 0.3 +           # Productivity
                    metrics['avg_citations'] * 0.001 +       # Impact (scaled)
                    metrics['recent_papers'] * 0.4 +         # Recent activity
                    min(len(set([p['title'][:50] for p in metrics['papers']])), 10) * 0.3  # Diversity (capped)
                )
                
                researcher_scores.append((score, author_name, metrics))
        
        # Sort by score
        researcher_scores.sort(reverse=True, key=lambda x: x[0])
        
        return researcher_scores[:top_k]
    
    def display_researcher_recommendations(self, researchers, research_area):
        """Display researcher recommendations with rich information"""
        
        if not researchers:
            display(HTML("<h3>No Birmingham researchers found for this area</h3>"))
            return
        
        display(HTML(f"""
        <h3>Birmingham Researchers for: "{research_area}"</h3>
        <p><strong>Found:</strong> {len(researchers)} researchers</p>
        """))
        
        for i, (score, name, metrics) in enumerate(researchers, 1):
            # Get top papers for this researcher
            top_papers = sorted(metrics['papers'], 
                              key=lambda p: (p['similarity'] * 0.7 + p['citations'] * 0.0001), 
                              reverse=True)[:3]
            
            papers_html = ""
            for j, paper in enumerate(top_papers, 1):
                title = paper['title'][:80] + "..." if len(paper['title']) > 80 else paper['title']
                papers_html += f"""
                <li><strong>{paper['year']}</strong>: {title} 
                    <em>({paper['citations']} citations, similarity: {paper['similarity']:.3f})</em></li>
                """
            
            display(HTML(f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin: 15px 0; border-radius: 8px; background-color: #f9f9f9;">
                <h4 style="margin: 0 0 10px 0; color: #2c5aa0;">{i}. {name}</h4>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <div><strong>Papers:</strong> {metrics['paper_count']}</div>
                    <div><strong>Total Citations:</strong> {metrics['total_citations']:,}</div>
                    <div><strong>Recent Papers (2019+):</strong> {metrics['recent_papers']}</div>
                    <div><strong>Score:</strong> {score:.2f}</div>
                </div>
                <p><strong>Affiliation:</strong> {metrics['main_affiliation']}</p>
                <p><strong>Representative Papers:</strong></p>
                <ul style="margin-left: 20px;">
                    {papers_html}
                </ul>
            </div>
            """))
    
    def enhanced_research_query(self, query, include_researchers=True, top_papers=10, top_researchers=8):
        """Enhanced research query that includes both papers and researchers"""
        
        # Extract research components
        components = self.extract_research_components(query)
        
        display(HTML(f"""
        <h2>Research Query Analysis</h2>
        <div style="background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
            <p><strong>Query:</strong> {query}</p>
            <p><strong>Detected Domains:</strong> {', '.join(components['domains']) if components['domains'] else 'General'}</p>
            <p><strong>Detected Methods:</strong> {', '.join(components['methods']) if components['methods'] else 'Not specified'}</p>
            <p><strong>Constraints/Requirements:</strong> {', '.join(components['constraints']) if components['constraints'] else 'None specified'}</p>
        </div>
        """))
        
        # Find relevant papers
        print("Finding relevant papers...")
        papers = self.rag.semantic_search_with_authors(query, top_papers)
        
        # Display papers
        display(HTML("<h3>Relevant Research Papers</h3>"))
        self.rag.display_results_with_authors(papers, query)
        
        # Find researchers if requested
        if include_researchers:
            print(f"\nFinding Birmingham researchers...")
            researchers = self.find_birmingham_researchers(query, top_researchers)
            self.display_researcher_recommendations(researchers, query)
        
        return {
            'components': components,
            'papers': papers,
            'researchers': researchers if include_researchers else []
        }
    
    def collaboration_analysis(self, author_name):
        """Analyze collaboration patterns for a given author"""
        
        query = f"""
        MATCH (a:Author {{full_name: $author_name}})-[:CO_AUTHOR]-(collaborator:Author)
        OPTIONAL MATCH (a)-[:AUTHOR_OF]->(paper:Document)
        RETURN collaborator.full_name as collaborator_name,
               count(DISTINCT paper) as shared_papers,
               collect(DISTINCT paper.title)[0..3] as sample_papers
        ORDER BY shared_papers DESC
        LIMIT 10
        """
        
        with self.rag.get_session() as session:
            result = session.run(query, author_name=author_name)
            collaborators = []
            
            for record in result:
                collaborators.append({
                    'name': record['collaborator_name'],
                    'shared_papers': record['shared_papers'],
                    'sample_papers': record['sample_papers']
                })
        
        return collaborators

# ============================================================================
# INITIALIZE ADVANCED SYSTEM
# ============================================================================

# Initialize the advanced research assistant
research_assistant = AdvancedResearchAssistant(rag)

print("Advanced Research Assistant initialized!")

# ============================================================================
# TESTING FUNCTIONS
# ============================================================================

def test_researcher_recommendations():
    """Test the researcher recommendation system"""
    test_queries = [
        "machine learning medical imaging lung cancer",
        "natural language processing automated grading",
        "reinforcement learning energy smart grid",
        "genetic biomarkers Alzheimer's disease",
        "brain computer interface rehabilitation",
        "graph neural networks materials science"
    ]
    
    print("Testing Researcher Recommendations:")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\nTesting: {query}")
        researchers = research_assistant.find_birmingham_researchers(query, 3)
        
        if researchers:
            print(f"Found {len(researchers)} researchers:")
            for score, name, metrics in researchers:
                print(f"  - {name}: {metrics['paper_count']} papers, {metrics['total_citations']} citations")
        else:
            print("  No researchers found")
        print("-" * 30)

def run_enhanced_query(query):
    """Run an enhanced research query"""
    return research_assistant.enhanced_research_query(
        query, 
        include_researchers=True, 
        top_papers=8, 
        top_researchers=6
    )

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

print("""
USAGE INSTRUCTIONS:
==================

1. Test researcher recommendations:
   test_researcher_recommendations()

2. Run enhanced research queries:
   run_enhanced_query("your research question here")

3. Find researchers for specific area:
   researchers = research_assistant.find_birmingham_researchers("machine learning healthcare", 10)
   research_assistant.display_researcher_recommendations(researchers, "machine learning healthcare")

4. Analyze collaborations:
   collaborators = research_assistant.collaboration_analysis("Author Name")

READY TO USE!
""")

# Example test - uncomment to run
# test_researcher_recommendations()