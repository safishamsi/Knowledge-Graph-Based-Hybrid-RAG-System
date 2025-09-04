# Knowledge Graph-Based Hybrid RAG System

Academic search system combining knowledge graphs with retrieval-augmented generation to eliminate citation bias and hallucinations in research discovery.

## 🚀 Key Features
- **50% better search relevance** (NDCG@10: 0.814) than traditional systems
- **57.5% reduction** in temporal citation bias
- **67% fewer hallucinations** through document grounding
- Sub-500ms query response times
- Automatic collaboration discovery via community detection

## 🛠️ Tech Stack
- **Knowledge Graph**: Neo4j (61,945 papers, 189,972 authors)
- **Embeddings**: SBERT + FAISS indexing
- **RAG Pipeline**: LangChain/LangGraph + Claude-3.5-Sonnet
- **Data Source**: Scopus API integration
- **Language**: Python

## 📊 Results
- 82% researcher preference over Google Scholar
- 64% reduction in literature review time
- 96% cost reduction vs GPT-4 ($1.02 vs $24/1000 queries)

## 📁 Project Structure
├── Neo4jKG/           # Knowledge graph construction notebooks
├── RAG/               # Retrieval-augmented generation implementation
├── embeddings/        # SBERT embedding pipeline
├── scopusscraping/    # Scopus data collection scripts
├── Dissertation/      # Thesis documentation
├── Data/              # UoB affiliates and datasets
└── LLMpoweredRAG.py   # Main system implementation

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- Neo4j Database
- Anthropic API key for Claude-3.5

### Installation
```bash
git clone https://github.com/safishamsi/Knowledge-Graph-Based-Hybrid-RAG-System.git
cd Knowledge-Graph-Based-Hybrid-RAG-System

# Install dependencies
pip install neo4j sentence-transformers faiss-cpu langchain langchain-anthropic langgraph

# Set environment variables
export ANTHROPIC_API_KEY="your-api-key"

Research Context
Master's thesis project, University of Birmingham (2025)
Supervised by Prof. Dr. Paolo Missier
License
MIT License - see LICENSE file
Contact
For questions or collaboration: safishamsi98@gmail.com


