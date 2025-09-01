# ============================================================================
# COLLABORATION NETWORK AND RESEARCH TREND ANALYSIS
# ============================================================================

import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
import pandas as pd
from datetime import datetime
import numpy as np
from scipy import stats
import seaborn as sns

class CollaborationTrendAnalyzer:
    def __init__(self, rag_system):
        self.rag = rag_system
        
    def analyze_collaboration_network(self, research_area, min_papers=2, top_k=50):
        """Analyze collaboration networks for a research area"""
        
        print(f"Analyzing collaboration network for: {research_area}")
        print("=" * 60)
        
        # Step 1: Get relevant papers
        papers = self.rag.semantic_search_with_authors(research_area, top_k=top_k)
        
        # Step 2: Build collaboration graph
        collaboration_graph = defaultdict(lambda: defaultdict(int))
        author_paper_count = defaultdict(int)
        author_info = {}
        
        birmingham_affiliations = [
            'university of birmingham', 'birmingham business school',
            'college of social sciences', 'birmingham medical school',
            'university of birmingham dubai'
        ]
        
        for paper in papers:
            authors = paper.get('authors', [])
            affiliation = paper.get('main_affiliation', '').lower()
            year = paper.get('year', 0)
            
            # Filter for Birmingham papers
            is_birmingham = any(bham in affiliation for bham in birmingham_affiliations)
            
            if is_birmingham and len(authors) > 1:
                # Count papers per author
                for author in authors:
                    if author:
                        author_paper_count[author] += 1
                        if author not in author_info:
                            author_info[author] = {
                                'affiliation': paper.get('main_affiliation', ''),
                                'years': [],
                                'total_citations': 0
                            }
                        author_info[author]['years'].append(year)
                        author_info[author]['total_citations'] += paper.get('citations', 0)
                
                # Build collaboration edges
                for i, author1 in enumerate(authors):
                    for author2 in authors[i+1:]:
                        if author1 and author2:
                            collaboration_graph[author1][author2] += 1
                            collaboration_graph[author2][author1] += 1
        
        # Step 3: Filter authors with minimum papers
        active_authors = {author for author, count in author_paper_count.items() 
                         if count >= min_papers}
        
        # Step 4: Create NetworkX graph
        G = nx.Graph()
        
        for author1 in active_authors:
            G.add_node(author1, papers=author_paper_count[author1])
            
            for author2, weight in collaboration_graph[author1].items():
                if author2 in active_authors and weight > 0:
                    G.add_edge(author1, author2, weight=weight)
        
        # Step 5: Calculate network metrics
        if len(G.nodes) > 0:
            centrality_metrics = {
                'degree': nx.degree_centrality(G),
                'betweenness': nx.betweenness_centrality(G),
                'closeness': nx.closeness_centrality(G),
                'eigenvector': nx.eigenvector_centrality(G) if nx.is_connected(G) or len(G.nodes) == 1 else {}
            }
            
            # Find communities
            try:
                communities = list(nx.community.greedy_modularity_communities(G))
            except:
                communities = []
        else:
            centrality_metrics = {}
            communities = []
        
        return {
            'graph': G,
            'centrality_metrics': centrality_metrics,
            'communities': communities,
            'author_info': author_info,
            'author_paper_count': author_paper_count
        }
    
    def display_collaboration_network(self, network_data, research_area, top_n=10):
        """Display collaboration network analysis results"""
        
        G = network_data['graph']
        centrality_metrics = network_data['centrality_metrics']
        communities = network_data['communities']
        author_info = network_data['author_info']
        
        if len(G.nodes) == 0:
            display(HTML("<h3>No collaboration network found for this research area</h3>"))
            return
        
        # Network Statistics
        density = nx.density(G)
        num_components = nx.number_connected_components(G)
        
        display(HTML(f"""
        <h3>Collaboration Network Analysis: {research_area}</h3>
        <div style="background-color: #f0f8ff; padding: 15px; border-radius: 5px; margin: 15px 0;">
            <h4>Network Statistics</h4>
            <ul>
                <li><strong>Total Researchers:</strong> {len(G.nodes)}</li>
                <li><strong>Collaboration Edges:</strong> {len(G.edges)}</li>
                <li><strong>Network Density:</strong> {density:.3f}</li>
                <li><strong>Connected Components:</strong> {num_components}</li>
                <li><strong>Research Communities:</strong> {len(communities)}</li>
            </ul>
        </div>
        """))
        
        # Top Researchers by Different Metrics
        if centrality_metrics:
            metrics_html = ""
            for metric_name, metric_values in centrality_metrics.items():
                if metric_values:
                    top_researchers = sorted(metric_values.items(), 
                                           key=lambda x: x[1], reverse=True)[:5]
                    
                    researchers_list = ""
                    for author, score in top_researchers:
                        papers = network_data['author_paper_count'].get(author, 0)
                        researchers_list += f"<li>{author} (Score: {score:.3f}, Papers: {papers})</li>"
                    
                    metrics_html += f"""
                    <div style="margin: 10px 0;">
                        <h5>{metric_name.title()} Centrality Leaders</h5>
                        <ul>{researchers_list}</ul>
                    </div>
                    """
            
            display(HTML(f"""
            <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <h4>Key Researchers by Network Position</h4>
                {metrics_html}
            </div>
            """))
        
        # Research Communities
        if communities:
            communities_html = ""
            for i, community in enumerate(communities[:3], 1):
                community_list = list(community)[:5]  # Show top 5 members
                members_str = ", ".join(community_list)
                if len(community) > 5:
                    members_str += f" + {len(community) - 5} more"
                
                communities_html += f"""
                <li><strong>Community {i}:</strong> {len(community)} researchers<br>
                    <em>Members:</em> {members_str}</li>
                """
            
            display(HTML(f"""
            <div style="background-color: #fff5f5; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <h4>Research Communities Detected</h4>
                <ul>{communities_html}</ul>
            </div>
            """))
    
    def analyze_research_trends(self, research_area, years_back=10):
        """Analyze research trends over time"""
        
        print(f"Analyzing research trends for: {research_area}")
        print("=" * 60)
        
        current_year = datetime.now().year
        start_year = current_year - years_back
        
        # Get papers with broader search
        papers = self.rag.semantic_search_with_authors(research_area, top_k=100)
        
        # Analyze trends by year
        yearly_data = defaultdict(lambda: {
            'papers': 0,
            'citations': 0,
            'authors': set(),
            'keywords': [],
            'avg_citations': 0
        })
        
        keyword_trends = defaultdict(lambda: defaultdict(int))
        
        birmingham_affiliations = [
            'university of birmingham', 'birmingham business school',
            'college of social sciences', 'birmingham medical school',
            'university of birmingham dubai'
        ]
        
        for paper in papers:
            year = paper.get('year')
            affiliation = paper.get('main_affiliation', '').lower()
            
            # Filter for Birmingham and valid years
            is_birmingham = any(bham in affiliation for bham in birmingham_affiliations)
            
            if is_birmingham and year and year >= start_year:
                citations = paper.get('citations', 0)
                authors = paper.get('authors', [])
                title = paper.get('title', '').lower()
                
                # Update yearly statistics
                yearly_data[year]['papers'] += 1
                yearly_data[year]['citations'] += citations
                yearly_data[year]['authors'].update(authors)
                
                # Extract keywords from titles (simple approach)
                keywords = self.extract_trend_keywords(title)
                yearly_data[year]['keywords'].extend(keywords)
                
                # Track keyword trends over time
                for keyword in keywords:
                    keyword_trends[keyword][year] += 1
        
        # Calculate averages and growth rates
        trend_analysis = {}
        years = sorted([y for y in yearly_data.keys() if y >= start_year])
        
        if len(years) > 1:
            papers_by_year = [yearly_data[year]['papers'] for year in years]
            citations_by_year = [yearly_data[year]['citations'] for year in years]
            
            # Calculate trends
            if len(papers_by_year) > 2:
                paper_trend = np.polyfit(range(len(papers_by_year)), papers_by_year, 1)[0]
                citation_trend = np.polyfit(range(len(citations_by_year)), citations_by_year, 1)[0]
            else:
                paper_trend = 0
                citation_trend = 0
            
            trend_analysis = {
                'years': years,
                'papers_by_year': papers_by_year,
                'citations_by_year': citations_by_year,
                'paper_trend': paper_trend,
                'citation_trend': citation_trend,
                'total_papers': sum(papers_by_year),
                'total_citations': sum(citations_by_year)
            }
        
        # Find emerging keywords
        emerging_keywords = []
        if len(years) >= 3:
            recent_years = years[-3:]
            earlier_years = years[:-3] if len(years) > 3 else []
            
            for keyword, year_counts in keyword_trends.items():
                recent_count = sum(year_counts[y] for y in recent_years)
                earlier_count = sum(year_counts[y] for y in earlier_years) if earlier_years else 1
                
                if recent_count >= 2 and recent_count > earlier_count:
                    growth_rate = (recent_count - earlier_count) / max(earlier_count, 1)
                    emerging_keywords.append((keyword, recent_count, growth_rate))
        
        emerging_keywords.sort(key=lambda x: x[2], reverse=True)
        
        return {
            'yearly_data': yearly_data,
            'trend_analysis': trend_analysis,
            'keyword_trends': keyword_trends,
            'emerging_keywords': emerging_keywords[:10]
        }
    
    def extract_trend_keywords(self, title):
        """Extract meaningful keywords from paper titles"""
        
        # Common research keywords to track
        research_keywords = [
            'deep learning', 'machine learning', 'neural network', 'artificial intelligence',
            'computer vision', 'natural language processing', 'reinforcement learning',
            'transformer', 'attention', 'convolutional', 'lstm', 'gru',
            'classification', 'segmentation', 'detection', 'prediction',
            'medical imaging', 'healthcare', 'clinical', 'diagnosis',
            'covid', 'cancer', 'tumor', 'disease',
            'interpretable', 'explainable', 'federated', 'privacy',
            'robust', 'adversarial', 'uncertainty', 'ensemble'
        ]
        
        found_keywords = []
        title_lower = title.lower()
        
        for keyword in research_keywords:
            if keyword in title_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def display_research_trends(self, trends_data, research_area):
        """Display research trends analysis"""
        
        yearly_data = trends_data['yearly_data']
        trend_analysis = trends_data['trend_analysis']
        emerging_keywords = trends_data['emerging_keywords']
        
        if not yearly_data:
            display(HTML("<h3>No trend data found for this research area</h3>"))
            return
        
        # Overall trends summary
        total_papers = trend_analysis.get('total_papers', 0)
        total_citations = trend_analysis.get('total_citations', 0)
        paper_trend = trend_analysis.get('paper_trend', 0)
        
        trend_direction = "increasing" if paper_trend > 0.1 else "decreasing" if paper_trend < -0.1 else "stable"
        
        display(HTML(f"""
        <h3>Research Trends Analysis: {research_area}</h3>
        <div style="background-color: #f0f8ff; padding: 15px; border-radius: 5px; margin: 15px 0;">
            <h4>Overall Trends</h4>
            <ul>
                <li><strong>Total Papers (Birmingham):</strong> {total_papers}</li>
                <li><strong>Total Citations:</strong> {total_citations:,}</li>
                <li><strong>Research Activity:</strong> {trend_direction.title()}</li>
                <li><strong>Annual Growth Rate:</strong> {paper_trend:+.2f} papers/year</li>
            </ul>
        </div>
        """))
        
        # Year by year breakdown
        years_html = ""
        for year in sorted(yearly_data.keys(), reverse=True)[:5]:
            data = yearly_data[year]
            avg_cit = data['citations'] / max(data['papers'], 1)
            unique_authors = len(data['authors'])
            
            years_html += f"""
            <li><strong>{year}:</strong> {data['papers']} papers, 
                {data['citations']} citations (avg: {avg_cit:.1f}), 
                {unique_authors} unique authors</li>
            """
        
        display(HTML(f"""
        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin: 15px 0;">
            <h4>Recent Years Breakdown</h4>
            <ul>{years_html}</ul>
        </div>
        """))
        
        # Emerging keywords
        if emerging_keywords:
            keywords_html = ""
            for keyword, count, growth in emerging_keywords[:8]:
                keywords_html += f"""
                <li><strong>{keyword.title()}:</strong> {count} recent papers 
                    (Growth: {growth:+.1f}x)</li>
                """
            
            display(HTML(f"""
            <div style="background-color: #fff5f5; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <h4>Emerging Research Topics</h4>
                <ul>{keywords_html}</ul>
            </div>
            """))
    
    def comprehensive_research_analysis(self, research_area, min_papers=2):
        """Run both collaboration and trend analysis"""
        
        display(HTML(f"""
        <h2>Comprehensive Research Analysis: {research_area}</h2>
        <hr style="margin: 20px 0;">
        """))
        
        # Collaboration Network Analysis
        network_data = self.analyze_collaboration_network(research_area, min_papers)
        self.display_collaboration_network(network_data, research_area)
        
        print("\n" + "="*60 + "\n")
        
        # Research Trends Analysis
        trends_data = self.analyze_research_trends(research_area)
        self.display_research_trends(trends_data, research_area)
        
        return {
            'collaboration_network': network_data,
            'research_trends': trends_data
        }

# ============================================================================
# INITIALIZE THE ANALYZER
# ============================================================================

# Initialize the collaboration and trend analyzer
collab_trend_analyzer = CollaborationTrendAnalyzer(rag)

print("Collaboration and Trend Analyzer initialized!")

# ============================================================================
# TESTING AND USAGE FUNCTIONS
# ============================================================================

def analyze_research_landscape(research_area, min_papers=2):
    """Analyze the complete research landscape for an area"""
    return collab_trend_analyzer.comprehensive_research_analysis(research_area, min_papers)

def analyze_collaborations_only(research_area, min_papers=2):
    """Analyze just the collaboration network"""
    network_data = collab_trend_analyzer.analyze_collaboration_network(research_area, min_papers)
    collab_trend_analyzer.display_collaboration_network(network_data, research_area)
    return network_data

def analyze_trends_only(research_area, years_back=10):
    """Analyze just the research trends"""
    trends_data = collab_trend_analyzer.analyze_research_trends(research_area, years_back)
    collab_trend_analyzer.display_research_trends(trends_data, research_area)
    return trends_data

# ============================================================================
# USAGE INSTRUCTIONS
# ============================================================================

print("""
COLLABORATION & TREND ANALYSIS READY!
=====================================

Functions available:

1. Complete analysis:
   analyze_research_landscape("machine learning medical imaging")

2. Collaboration network only:
   analyze_collaborations_only("deep learning healthcare")

3. Research trends only:
   analyze_trends_only("artificial intelligence", years_back=8)

4. For specific researchers:
   network_data = analyze_collaborations_only("lung cancer detection")
   # Then examine network_data['centrality_metrics'] for detailed metrics

Examples:
- analyze_research_landscape("deep learning lung cancer")
- analyze_collaborations_only("machine learning healthcare", min_papers=3)
- analyze_trends_only("computer vision medical", years_back=5)
""")