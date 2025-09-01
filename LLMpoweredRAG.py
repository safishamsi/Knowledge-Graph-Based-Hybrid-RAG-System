# ============================================================================
# COMPLETE WORKING RESEARCH ASSISTANT - ONE CODE TO RULE THEM ALL
# ============================================================================

import os
import json
from typing import Dict, List, Any
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict

# ============================================================================
# STATE AND WORKFLOW
# ============================================================================

class ResearchState(TypedDict):
    query: str
    papers: str
    researchers: str  
    networks: str
    trends: str
    response: str

class SmartResearchAssistant:
    def __init__(self, rag_system, research_assistant, collab_analyzer):
        """Initialize with your existing components"""
        self.rag = rag_system
        self.research_assistant = research_assistant
        self.collab_analyzer = collab_analyzer
        
        # Initialize Claude
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            anthropic_api_key=os.environ.get('ANTHROPIC_API_KEY'),
            temperature=0.1,
            max_tokens=4000
        )
        
        # Build workflow
        self.workflow = self._build_workflow()
        self.app = self.workflow.compile()
        
    def _build_workflow(self):
        workflow = StateGraph(ResearchState)
        
        workflow.add_node("search_papers", self._search_papers)
        workflow.add_node("find_researchers", self._find_researchers)
        workflow.add_node("analyze_networks", self._analyze_networks)
        workflow.add_node("analyze_trends", self._analyze_trends)
        workflow.add_node("synthesize", self._synthesize)
        
        workflow.set_entry_point("search_papers")
        workflow.add_edge("search_papers", "find_researchers")
        workflow.add_edge("find_researchers", "analyze_networks") 
        workflow.add_edge("analyze_networks", "analyze_trends")
        workflow.add_edge("analyze_trends", "synthesize")
        workflow.add_edge("synthesize", END)
        
        return workflow
    
    def _search_papers(self, state: ResearchState) -> ResearchState:
        """Search for relevant papers"""
        query = state["query"]
        try:
            results = self.rag.semantic_search_with_authors(query, 8)
            
            papers = []
            for i, paper in enumerate(results[:5], 1):
                papers.append({
                    'rank': i,
                    'title': paper.get('title', '')[:100],
                    'authors': paper.get('authors', [])[:3],
                    'year': paper.get('year', 'N/A'),
                    'citations': paper.get('citations', 0),
                    'institution': paper.get('main_affiliation', ''),
                    'relevance': round(paper.get('similarity_score', 0), 3)
                })
            
            state["papers"] = json.dumps({'found': len(results), 'papers': papers}, indent=2)
        except Exception as e:
            state["papers"] = f"Error: {str(e)}"
        
        return state
    
    def _find_researchers(self, state: ResearchState) -> ResearchState:
        """Find Birmingham researchers"""
        query = state["query"]
        try:
            researchers = self.research_assistant.find_birmingham_researchers(query, 6)
            
            researcher_list = []
            for score, name, metrics in researchers[:5]:
                researcher_list.append({
                    'name': name,
                    'score': round(score, 2),
                    'papers': metrics['paper_count'],
                    'citations': metrics['total_citations'],
                    'recent_work': metrics['recent_papers'],
                    'department': metrics['main_affiliation'],
                    'expertise': metrics['papers'][0]['title'][:80] if metrics['papers'] else 'N/A'
                })
            
            state["researchers"] = json.dumps({'found': len(researchers), 'researchers': researcher_list}, indent=2)
        except Exception as e:
            state["researchers"] = f"Error: {str(e)}"
        
        return state
    
    def _analyze_networks(self, state: ResearchState) -> ResearchState:
        """Analyze collaboration networks"""
        query = state["query"]
        try:
            network_data = self.collab_analyzer.analyze_collaboration_network(query, min_papers=2)
            
            G = network_data['graph']
            centrality = network_data['centrality_metrics']
            communities = network_data['communities']
            
            key_researchers = []
            if centrality.get('degree'):
                for name, score in sorted(centrality['degree'].items(), key=lambda x: x[1], reverse=True)[:4]:
                    key_researchers.append({'name': name, 'centrality': round(score, 3)})
            
            network_summary = {
                'researchers': len(G.nodes),
                'collaborations': len(G.edges),
                'communities': len(communities),
                'key_researchers': key_researchers
            }
            
            state["networks"] = json.dumps(network_summary, indent=2)
        except Exception as e:
            state["networks"] = f"Error: {str(e)}"
        
        return state
    
    def _analyze_trends(self, state: ResearchState) -> ResearchState:
        """Analyze research trends"""
        query = state["query"]
        try:
            trends_data = self.collab_analyzer.analyze_research_trends(query, years_back=8)
            
            trend_analysis = trends_data['trend_analysis']
            emerging_keywords = trends_data['emerging_keywords']
            yearly_data = trends_data['yearly_data']
            
            recent_years = sorted(yearly_data.keys(), reverse=True)[:4]
            recent_activity = []
            for year in recent_years:
                if year in yearly_data:
                    data = yearly_data[year]
                    recent_activity.append({
                        'year': year,
                        'papers': data['papers'],
                        'citations': data['citations']
                    })
            
            trends_summary = {
                'total_papers': trend_analysis.get('total_papers', 0),
                'total_citations': trend_analysis.get('total_citations', 0),
                'trend': 'growing' if trend_analysis.get('paper_trend', 0) > 0.1 else 'stable',
                'recent_years': recent_activity,
                'emerging_topics': [kw for kw, _, _ in emerging_keywords[:5]]
            }
            
            state["trends"] = json.dumps(trends_summary, indent=2)
        except Exception as e:
            state["trends"] = f"Error: {str(e)}"
        
        return state
    
    def _synthesize(self, state: ResearchState) -> ResearchState:
        """Synthesize comprehensive response using Claude"""
        
        prompt = f"""
        You are an expert research assistant at University of Birmingham. Analyze this research query and provide comprehensive guidance.
        
        Query: "{state['query']}"
        
        Research Data:
        
        PAPERS FOUND:
        {state['papers']}
        
        RESEARCHERS IDENTIFIED:
        {state['researchers']}
        
        COLLABORATION NETWORKS:
        {state['networks']}
        
        RESEARCH TRENDS:
        {state['trends']}
        
        Provide a comprehensive response that:
        1. Directly answers the research question
        2. Highlights Birmingham's strengths in this area
        3. Identifies key researchers and their expertise
        4. Provides actionable next steps and recommendations
        5. Suggests collaboration opportunities
        
        Structure with clear headings and be practical and actionable.
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            state["response"] = response.content
        except Exception as e:
            state["response"] = f"Error in synthesis: {str(e)}"
        
        return state
    
    def query(self, research_query: str) -> str:
        """Process research query through complete workflow"""
        
        print(f"Processing: {research_query}")
        print("=" * 60)
        
        initial_state = {
            "query": research_query,
            "papers": "",
            "researchers": "",
            "networks": "",
            "trends": "",
            "response": ""
        }
        
        try:
            final_state = self.app.invoke(initial_state)
            return final_state["response"]
        except Exception as e:
            return f"Workflow error: {str(e)}"

# ============================================================================
# INITIALIZE AND USE
# ============================================================================

def create_smart_assistant():
    """Create the complete research assistant"""
    
    if not os.environ.get('ANTHROPIC_API_KEY'):
        print("Error: Set ANTHROPIC_API_KEY first")
        return None
    
    try:
        assistant = SmartResearchAssistant(rag, research_assistant, collab_trend_analyzer)
        print("✅ Smart Research Assistant created!")
        return assistant
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Create the assistant
smart_assistant = create_smart_assistant()

# ============================================================================
# INTERACTIVE FUNCTIONS
# ============================================================================

def interactive_research_assistant():
    """Interactive function for user queries"""
    
    if not smart_assistant:
        print("❌ Assistant not initialized. Check your API key and components.")
        return
    
    print("\n🔬 Birmingham Research Assistant")
    print("=" * 50)
    print("Ask me anything about research at University of Birmingham!")
    print("Examples:")
    print("- 'Find researchers working on machine learning for healthcare'")
    print("- 'I want to develop AI for medical diagnosis'") 
    print("- 'Show me trends in computer vision research'")
    print("- 'Who should I collaborate with for deep learning projects?'")
    print("\nType 'quit' or 'exit' to stop.")
    print("=" * 50)
    
    while True:
        try:
            # Get user input
            user_query = input("\n🔍 Your research question: ").strip()
            
            # Check for exit commands
            if user_query.lower() in ['quit', 'exit', 'stop', '']:
                print("\n👋 Thank you for using Birmingham Research Assistant!")
                break
            
            # Process the query
            print(f"\n🧠 Analyzing your query...")
            response = smart_assistant.query(user_query)
            
            # Display response
            print("\n📊 RESEARCH ANALYSIS RESULTS")
            print("=" * 60)
            print(response)
            print("=" * 60)
            
            # Ask if they want to continue
            continue_choice = input("\n❓ Ask another question? (y/n): ").strip().lower()
            if continue_choice in ['n', 'no']:
                print("\n👋 Thank you for using Birmingham Research Assistant!")
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again with a different question.")

def quick_query():
    """Quick single query function"""
    if not smart_assistant:
        print("❌ Assistant not initialized.")
        return
    
    user_query = input("\n🔍 Enter your research question: ").strip()
    if user_query:
        print(f"\n🧠 Processing: {user_query}")
        response = smart_assistant.query(user_query)
        print(f"\n📊 RESPONSE:\n{response}")
    else:
        print("No query entered.")

# ============================================================================
# READY TO USE
# ============================================================================

if smart_assistant:
    print("""
    READY! Usage:
    
    response = smart_assistant.query("I want to design a deep learning model for early detection of lung cancer from CT scans")
    print(response)
    
    Features:
    ✅ LangGraph workflow orchestration
    ✅ Claude-powered synthesis
    ✅ Graph + Semantic hybrid search
    ✅ Full research analysis pipeline
    """)

# Test function
def test_assistant():
    if smart_assistant:
        response = smart_assistant.query("machine learning healthcare Birmingham")
        print("\nTEST RESULT:")
        print("=" * 40)
        print(response)
        return response
    else:
        print("Assistant not initialized")

print("\nRun test_assistant() to test the system")