#!/usr/bin/env python3
"""
Birmingham Knowledge Graph - Clean Final Version
Robust processing with proper database handling
"""

import os
import json
import time
import logging
from datetime import datetime
from tqdm import tqdm
from collections import defaultdict
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, TransientError, NotALeader

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class BirminghamKG:
    def __init__(self, database="neo4j"):
        self.database = database
        self.driver = None
        self.connect()
        
        self.birmingham_institutions = [
            "University of Birmingham", "Birmingham Business School",
            "College of Social Sciences", "Birmingham Medical School"
        ]
        
        self.stats = {'documents': 0, 'authors': 0, 'affiliations': 0, 'publications': 0}
        
    def connect(self):
        """Connect to Neo4j with retry"""
        for attempt in range(3):
            try:
                self.driver = GraphDatabase.driver(
                    "neo4j://127.0.0.1:7687", 
                    auth=("neo4j", "12345678"),
                    max_connection_lifetime=300
                )
                
                with self.driver.session(database=self.database) as session:
                    session.run("RETURN 1").single()
                
                logger.info(f"✅ Connected to database '{self.database}'")
                return
                
            except Exception as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                if "nodatabaseaccess" in str(e).lower():
                    logger.error(f"Database '{self.database}' is offline. Connect to 'system' and run: START DATABASE {self.database}")
                    break
                time.sleep(5)
        
        raise Exception("Failed to connect to Neo4j")
    
    def get_session(self):
        return self.driver.session(database=self.database)
    
    def execute_query(self, query, params=None, session=None):
        """Execute query with retry logic"""
        for attempt in range(3):
            try:
                if session:
                    return session.run(query, params or {})
                else:
                    with self.get_session() as temp_session:
                        return temp_session.run(query, params or {})
            except (ServiceUnavailable, TransientError, NotALeader):
                if attempt < 2:
                    logger.warning(f"Retrying query (attempt {attempt + 2})")
                    time.sleep(5)
                else:
                    raise
    
    def clear_database(self):
        """Clear database safely"""
        logger.info("🗑️ Clearing database...")
        
        with self.get_session() as session:
            # Clear constraints and indexes
            try:
                constraints = session.run("SHOW CONSTRAINTS")
                for constraint in constraints:
                    name = constraint.get('name', '')
                    if name:
                        try:
                            session.run(f"DROP CONSTRAINT {name}")
                        except: pass
            except: pass
            
            # Delete nodes in batches
            batch_size = 1000
            deleted_total = 0
            
            while True:
                try:
                    result = self.execute_query(f"""
                        MATCH (n) WITH n LIMIT {batch_size}
                        DETACH DELETE n RETURN COUNT(n) as deleted
                    """, session=session)
                    
                    record = result.single()
                    if record and record['deleted'] > 0:
                        deleted_total += record['deleted']
                        logger.info(f"   Deleted {deleted_total:,} nodes")
                    else:
                        break
                except Exception as e:
                    if "Memory" in str(e):
                        batch_size = max(100, batch_size // 2)
                        logger.warning(f"Reduced batch size to {batch_size}")
                    else:
                        break
        
        logger.info(f"✅ Cleared {deleted_total:,} nodes")
    
    def create_schema(self):
        """Create schema"""
        logger.info("🏗️ Creating schema...")
        
        constraints = [
            "CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.document_id IS UNIQUE",
            "CREATE CONSTRAINT author_id IF NOT EXISTS FOR (a:Author) REQUIRE a.author_id IS UNIQUE",
            "CREATE CONSTRAINT publication_id IF NOT EXISTS FOR (p:Publication) REQUIRE p.publication_id IS UNIQUE",
            "CREATE CONSTRAINT affiliation_id IF NOT EXISTS FOR (af:Affiliation) REQUIRE af.affiliation_id IS UNIQUE"
        ]
        
        with self.get_session() as session:
            for constraint in constraints:
                try:
                    self.execute_query(constraint, session=session)
                except: pass
        
        logger.info("✅ Schema created")
    
    def extract_papers(self, data):
        """Extract papers from Scopus response"""
        papers = []
        
        if isinstance(data, dict):
            if 'search-results' in data and 'entry' in data['search-results']:
                papers = data['search-results']['entry']
            elif 'entry' in data:
                papers = data['entry']
            elif any(key.startswith('result_') for key in data.keys()):
                for key, value in data.items():
                    if key.startswith('result_') and isinstance(value, dict) and 'entry' in value:
                        papers.extend(value['entry'])
        elif isinstance(data, list):
            papers = data
        
        return papers
    
    def is_birmingham_affiliated(self, paper):
        """Check if paper has Birmingham affiliation"""
        if 'affiliation' not in paper:
            return False
        
        affil_list = paper['affiliation'] if isinstance(paper['affiliation'], list) else [paper['affiliation']]
        
        for affil in affil_list:
            if isinstance(affil, dict):
                affil_name = affil.get('affilname', '').lower()
                if any(inst.lower() in affil_name for inst in self.birmingham_institutions):
                    return True
        return False
    
    def extract_document_data(self, paper):
        """Extract document data"""
        doi = paper.get('prism:doi', '')
        scopus_id = paper.get('dc:identifier', '').replace('SCOPUS_ID:', '')
        document_id = doi if doi else scopus_id
        
        if not document_id:
            return None
        
        # Extract year
        year = None
        date_str = paper.get('prism:coverDate', '')
        if date_str and '-' in str(date_str):
            try:
                year = int(str(date_str).split('-')[0])
            except: pass
        
        return {
            'document_id': document_id,
            'title': paper.get('dc:title', ''),
            'abstract': paper.get('dc:description', ''),
            'year': year,
            'citation_count': int(paper.get('citedby-count', 0)),
            'doi': doi,
            'scopus_id': scopus_id
        }
    
    def extract_authors_data(self, paper):
        """Extract authors data"""
        authors = []
        
        if 'author' in paper:
            author_list = paper['author'] if isinstance(paper['author'], list) else [paper['author']]
            
            for author in author_list:
                if isinstance(author, dict):
                    author_id = author.get('authid', author.get('@auid', ''))
                    if not author_id:
                        continue
                    
                    full_name = author.get('authname', author.get('ce:indexed-name', ''))
                    
                    authors.append({
                        'author_id': author_id,
                        'full_name': full_name,
                        'orcid': author.get('orcid', ''),
                        'sequence': author.get('@seq', '')
                    })
        
        return authors
    
    def extract_affiliations_data(self, paper):
        """Extract affiliations data"""
        affiliations = []
        
        if 'affiliation' in paper:
            affil_list = paper['affiliation'] if isinstance(paper['affiliation'], list) else [paper['affiliation']]
            
            for affil in affil_list:
                if isinstance(affil, dict):
                    affil_id = affil.get('afid', '')
                    name = affil.get('affilname', '')
                    
                    if affil_id:
                        affiliations.append({
                            'affiliation_id': affil_id,
                            'name': name,
                            'city': affil.get('affiliation-city', ''),
                            'country': affil.get('affiliation-country', '')
                        })
        
        return affiliations
    
    def extract_publication_data(self, paper):
        """Extract publication data"""
        pub_name = paper.get('prism:publicationName', '')
        if not pub_name:
            return None
        
        issn = paper.get('prism:issn', '')
        pub_id = issn if issn else f"name_{pub_name.lower().replace(' ', '_')}"
        
        return {
            'publication_id': pub_id,
            'name': pub_name,
            'issn': issn,
            'publisher': paper.get('dc:publisher', '')
        }
    
    def load_data(self, json_files):
        """Load data from JSON files"""
        all_papers = []
        
        if isinstance(json_files, str):
            json_files = [json_files]
        
        for file_path in json_files:
            logger.info(f"📁 Loading {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                papers = self.extract_papers(data)
                all_papers.extend(papers)
        
        logger.info(f"📊 Loaded {len(all_papers)} papers")
        return all_papers
    
    def process_papers(self, raw_papers):
        """Process papers into knowledge graph"""
        logger.info("🏛️ Processing Birmingham papers...")
        
        # Filter Birmingham papers
        birmingham_papers = [paper for paper in raw_papers if self.is_birmingham_affiliated(paper)]
        logger.info(f"🎯 Found {len(birmingham_papers)} Birmingham papers")
        
        if not birmingham_papers:
            return 0
        
        # Pre-process data
        logger.info("🔄 Pre-processing data...")
        all_documents = []
        all_authors = {}
        all_affiliations = {}
        all_publications = {}
        all_relationships = {'author_of': [], 'affiliated_with': [], 'published_in': [], 'co_author': []}
        
        for paper in tqdm(birmingham_papers):
            try:
                doc_data = self.extract_document_data(paper)
                if not doc_data:
                    continue
                
                authors_data = self.extract_authors_data(paper)
                affiliations_data = self.extract_affiliations_data(paper)
                pub_data = self.extract_publication_data(paper)
                
                # Store data
                all_documents.append(doc_data)
                
                for author in authors_data:
                    all_authors[author['author_id']] = author
                
                for affil in affiliations_data:
                    all_affiliations[affil['affiliation_id']] = affil
                
                if pub_data:
                    all_publications[pub_data['publication_id']] = pub_data
                
                # Store relationships
                doc_id = doc_data['document_id']
                
                for author in authors_data:
                    all_relationships['author_of'].append({
                        'author_id': author['author_id'],
                        'doc_id': doc_id
                    })
                    
                    for affil in affiliations_data:
                        all_relationships['affiliated_with'].append({
                            'author_id': author['author_id'],
                            'affil_id': affil['affiliation_id']
                        })
                
                if pub_data:
                    all_relationships['published_in'].append({
                        'doc_id': doc_id,
                        'pub_id': pub_data['publication_id']
                    })
                
                # Co-author relationships
                if len(authors_data) > 1:
                    for i, author1 in enumerate(authors_data):
                        for author2 in authors_data[i+1:]:
                            all_relationships['co_author'].append({
                                'author1_id': author1['author_id'],
                                'author2_id': author2['author_id'],
                                'doc_id': doc_id
                            })
            
            except Exception as e:
                logger.error(f"Error processing paper: {e}")
                continue
        
        # Create nodes in batches
        logger.info("🚀 Creating nodes in Neo4j...")
        batch_size = 1000
        
        # Documents
        logger.info("📄 Creating documents...")
        for i in range(0, len(all_documents), batch_size):
            batch = all_documents[i:i + batch_size]
            with self.get_session() as session:
                self.execute_query("""
                    UNWIND $documents as doc
                    MERGE (d:Document {document_id: doc.document_id})
                    SET d.title = doc.title, d.abstract = doc.abstract,
                        d.year = doc.year, d.citation_count = doc.citation_count,
                        d.doi = doc.doi, d.scopus_id = doc.scopus_id
                """, {'documents': batch}, session)
        
        # Authors
        logger.info("👥 Creating authors...")
        author_list = list(all_authors.values())
        for i in range(0, len(author_list), batch_size):
            batch = author_list[i:i + batch_size]
            with self.get_session() as session:
                self.execute_query("""
                    UNWIND $authors as author
                    MERGE (a:Author {author_id: author.author_id})
                    SET a.full_name = author.full_name, a.orcid = author.orcid
                """, {'authors': batch}, session)
        
        # Affiliations
        logger.info("🏛️ Creating affiliations...")
        affil_list = list(all_affiliations.values())
        for i in range(0, len(affil_list), batch_size):
            batch = affil_list[i:i + batch_size]
            with self.get_session() as session:
                self.execute_query("""
                    UNWIND $affiliations as affil
                    MERGE (af:Affiliation {affiliation_id: affil.affiliation_id})
                    SET af.name = affil.name, af.city = affil.city, af.country = affil.country
                """, {'affiliations': batch}, session)
        
        # Publications
        if all_publications:
            logger.info("📚 Creating publications...")
            pub_list = list(all_publications.values())
            for i in range(0, len(pub_list), batch_size):
                batch = pub_list[i:i + batch_size]
                with self.get_session() as session:
                    self.execute_query("""
                        UNWIND $publications as pub
                        MERGE (p:Publication {publication_id: pub.publication_id})
                        SET p.name = pub.name, p.issn = pub.issn, p.publisher = pub.publisher
                    """, {'publications': batch}, session)
        
        # Create relationships
        logger.info("🔗 Creating relationships...")
        
        # Author-Document relationships
        for i in range(0, len(all_relationships['author_of']), batch_size):
            batch = all_relationships['author_of'][i:i + batch_size]
            with self.get_session() as session:
                self.execute_query("""
                    UNWIND $rels as rel
                    MATCH (a:Author {author_id: rel.author_id})
                    MATCH (d:Document {document_id: rel.doc_id})
                    MERGE (a)-[:AUTHOR_OF]->(d)
                """, {'rels': batch}, session)
        
        # Author-Affiliation relationships (deduplicated)
        unique_affiliations = list({(rel['author_id'], rel['affil_id']): rel 
                                   for rel in all_relationships['affiliated_with']}.values())
        for i in range(0, len(unique_affiliations), batch_size):
            batch = unique_affiliations[i:i + batch_size]
            with self.get_session() as session:
                self.execute_query("""
                    UNWIND $rels as rel
                    MATCH (a:Author {author_id: rel.author_id})
                    MATCH (af:Affiliation {affiliation_id: rel.affil_id})
                    MERGE (a)-[:AFFILIATED_WITH]->(af)
                """, {'rels': batch}, session)
        
        # Document-Publication relationships
        if all_relationships['published_in']:
            for i in range(0, len(all_relationships['published_in']), batch_size):
                batch = all_relationships['published_in'][i:i + batch_size]
                with self.get_session() as session:
                    self.execute_query("""
                        UNWIND $rels as rel
                        MATCH (d:Document {document_id: rel.doc_id})
                        MATCH (p:Publication {publication_id: rel.pub_id})
                        MERGE (d)-[:PUBLISHED_IN]->(p)
                    """, {'rels': batch}, session)
        
        # Co-author relationships (with counting)
        logger.info("🤝 Creating co-author relationships...")
        co_author_count = defaultdict(int)
        for rel in all_relationships['co_author']:
            key = tuple(sorted([rel['author1_id'], rel['author2_id']]))
            co_author_count[key] += 1
        
        co_author_final = [{'author1_id': key[0], 'author2_id': key[1], 'count': count} 
                          for key, count in co_author_count.items()]
        
        # Process in smaller batches for co-author relationships
        small_batch = 500
        for i in range(0, len(co_author_final), small_batch):
            batch = co_author_final[i:i + small_batch]
            with self.get_session() as session:
                self.execute_query("""
                    UNWIND $rels as rel
                    MATCH (a1:Author {author_id: rel.author1_id})
                    MATCH (a2:Author {author_id: rel.author2_id})
                    MERGE (a1)-[co:CO_AUTHOR]-(a2)
                    SET co.collaboration_count = rel.count
                """, {'rels': batch}, session)
            
            if i % 5000 == 0:
                logger.info(f"   Created {i:,} co-author relationships")
                time.sleep(0.5)  # Brief pause
        
        # Update stats
        self.stats['documents'] = len(all_documents)
        self.stats['authors'] = len(all_authors)
        self.stats['affiliations'] = len(all_affiliations)
        self.stats['publications'] = len(all_publications)
        
        logger.info(f"✅ Created knowledge graph with {len(all_documents)} documents")
        return len(all_documents)
    
    def get_statistics(self):
        """Get database statistics"""
        stats = {}
        with self.get_session() as session:
            for label in ['Document', 'Author', 'Publication', 'Affiliation']:
                try:
                    result = self.execute_query(f"MATCH (n:{label}) RETURN COUNT(n) as count", session=session)
                    stats[f'{label.lower()}_nodes'] = result.single()['count']
                except:
                    stats[f'{label.lower()}_nodes'] = 0
            
            try:
                result = self.execute_query("MATCH (n) RETURN COUNT(n) as count", session=session)
                stats['total_nodes'] = result.single()['count']
            except:
                stats['total_nodes'] = 0
        
        return stats
    
    def show_insights(self):
        """Show Birmingham insights"""
        logger.info(f"\n🏛️ BIRMINGHAM INSIGHTS (Database: {self.database}):")
        
        with self.get_session() as session:
            # Top authors
            try:
                result = self.execute_query("""
                    MATCH (a:Author)-[:AFFILIATED_WITH]->(af:Affiliation)
                    WHERE toLower(af.name) CONTAINS 'birmingham'
                    OPTIONAL MATCH (a)-[:AUTHOR_OF]->(d:Document)
                    RETURN a.full_name, COUNT(d) as papers, SUM(d.citation_count) as citations
                    ORDER BY papers DESC LIMIT 10
                """, session=session)
                
                logger.info("\n👥 TOP AUTHORS:")
                for record in result:
                    logger.info(f"   {record['a.full_name']} - {record['papers']} papers, {record['citations']} citations")
            except Exception as e:
                logger.warning(f"Error getting authors: {e}")
            
            # Research by year
            try:
                result = self.execute_query("""
                    MATCH (a:Author)-[:AFFILIATED_WITH]->(af:Affiliation)
                    WHERE toLower(af.name) CONTAINS 'birmingham'
                    MATCH (a)-[:AUTHOR_OF]->(d:Document)
                    WHERE d.year >= 2020
                    RETURN d.year, COUNT(d) as papers
                    ORDER BY d.year DESC
                """, session=session)
                
                logger.info("\n📈 PAPERS BY YEAR:")
                for record in result:
                    logger.info(f"   {record['d.year']}: {record['papers']} papers")
            except Exception as e:
                logger.warning(f"Error getting yearly data: {e}")
    
    def close(self):
        if self.driver:
            self.driver.close()

def main():
    logger.info("🚀 Birmingham Knowledge Graph - Final Version")
    
    # Get JSON files
    json_files = []
    while True:
        file_path = input("\nEnter JSON file path (or 'done'): ").strip()
        if file_path.lower() == 'done':
            break
        if os.path.exists(file_path):
            json_files.append(file_path)
            logger.info(f"✅ Added: {file_path}")
        else:
            logger.info("❌ File not found")
    
    if not json_files:
        logger.info("No files provided. Exiting.")
        return
    
    # Database options
    choice = input("""
🎯 Options:
1. Clear 'neo4j' database and process
2. Add to existing 'neo4j' database
3. Check database status first

Choose (1/2/3): """).strip()
    
    try:
        if choice == "3":
            # Check status first
            kg_system = BirminghamKG(database="system")
            with kg_system.get_session() as session:
                result = session.run("SHOW DATABASES")
                logger.info("\n📊 Databases:")
                for record in result:
                    logger.info(f"   {record['name']}: {record['status']}")
                
                # Start neo4j if offline
                db_status = session.run("SHOW DATABASE neo4j").single()
                if db_status['status'] == 'offline':
                    logger.info("🔄 Starting neo4j database...")
                    session.run("START DATABASE neo4j")
                    time.sleep(3)
            kg_system.close()
        
        # Main processing
        kg = BirminghamKG(database="neo4j")
        
        if choice == "1":
            kg.clear_database()
        
        kg.create_schema()
        papers = kg.load_data(json_files)
        
        start_time = datetime.now()
        processed = kg.process_papers(papers)
        duration = datetime.now() - start_time
        
        if processed > 0:
            logger.info(f"\n⏱️ Processing time: {duration}")
            
            stats = kg.get_statistics()
            logger.info(f"\n📊 Final Statistics:")
            for key, value in stats.items():
                logger.info(f"   {key.replace('_', ' ').title()}: {value:,}")
            
            kg.show_insights()
            
            logger.info(f"\n🎯 Success! Neo4j Browser: http://localhost:7474")
            logger.info(f"Database: {kg.database}")
        
        kg.close()
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        logger.info("💡 Try option 3 to check database status")

if __name__ == "__main__":
    main()