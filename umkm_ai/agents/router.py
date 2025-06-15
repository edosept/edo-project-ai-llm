import logging
from typing import Literal
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class Router:
    """Router for UMKM chatbot classification"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            max_tokens=20,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # SQL patterns
        self.sql_keywords = [
            # Sales and revenue terms (Indonesian & English)
            'penjualan', 'omzet', 'pendapatan', 'untung', 'keuntungan', 'laba', 'hasil',
            'sales', 'revenue', 'profit', 'income', 'earnings', 'turnover',
            
            # Transaction terms
            'transaksi', 'jual', 'beli', 'transaction', 'sold', 'purchase', 'buy',
            
            # Product and inventory (Indonesian & English)
            'produk', 'barang', 'item', 'laris', 'terjual', 'stok', 'menu', 'dagangan',
            'product', 'goods', 'selling', 'stock', 'inventory', 'merchandise',
            
            # Business entities (Indonesian & English)
            'warung kopi', 'warung sayur', 'warung sembako', 'kopi gembira', 'sayur sehat', 'sembako berkah',
            'coffee shop', 'vegetable store', 'grocery store', 'all businesses', 'each business',
            'semua warung', 'setiap warung', 'ketiga warung', 'masing-masing warung',
            'breakdown', 'gembira', 'sehat', 'berkah', 'bisnis', 'business', 'usaha',
            
            # Time periods and analysis (Indonesian & English)
            'bulan', 'hari', 'tahun', 'minggu', 'tanggal', 'waktu', 'periode', 'masa',
            'month', 'day', 'year', 'week', 'date', 'time', 'period', 'when', 'during',
            'analisis', 'data', 'laporan', 'statistik', 'performa', 'kinerja',
            'analysis', 'report', 'statistics', 'performance', 'metrics',
            
            # Payment and financial terms (Indonesian & English)
            'pembayaran', 'bayar', 'tunai', 'qris', 'digital', 'transfer', 'kartu',
            'payment', 'pay', 'cash', 'method', 'metode', 'preferensi', 'preference',
            'pengeluaran', 'biaya', 'ongkos', 'expense', 'cost', 'spending', 'expenditure',
            
            # Customer and sales patterns (Indonesian & English)
            'pelanggan', 'konsumen', 'pembeli', 'customer', 'buyer', 'client',
            'pola', 'pattern', 'tren', 'trend', 'perilaku', 'behavior', 'habits',
            
            # Quantities and comparisons (Indonesian & English)
            'berapa', 'jumlah', 'total', 'banyak', 'sedikit',
            'how much', 'how many', 'amount', 'quantity', 'number',
            'tertinggi', 'terendah', 'terbanyak', 'tersedikit', 'paling',
            'highest', 'lowest', 'most', 'least', 'maximum', 'minimum',
            'rata-rata', 'average', 'mean', 'maksimal', 'minimal',
            
            # Question words that typically need data (Indonesian & English)
            'kapan', 'dimana', 'siapa', 'apa', 'mana', 'kenapa', 'mengapa', 'bagaimana',
            'what', 'which', 'who', 'where', 'why', 'how', 'when',
            
            # Categories and classifications (Indonesian & English)
            'kategori', 'jenis', 'tipe', 'macam', 'golongan',
            'category', 'type', 'kind', 'classification', 'segment', 'group',
            
            # Performance indicators (Indonesian & English)
            'naik', 'turun', 'meningkat', 'menurun', 'stabil',
            'increase', 'decrease', 'rise', 'fall', 'stable', 'growth', 'decline',
            
            # Comparison terms (Indonesian & English)
            'dibanding', 'versus', 'vs', 'compare', 'bandingkan', 'banding',
            'lebih', 'kurang', 'sama', 'more', 'less', 'equal', 'than',
            
            # Time-specific terms (Indonesian & English)
            'kemarin', 'hari ini', 'besok', 'minggu lalu', 'bulan lalu',
            'yesterday', 'today', 'tomorrow', 'last week', 'last month',
            '2024', '2023', 'tahun ini', 'tahun lalu', 'this year', 'last year'
        ]
        
        # RAG patterns
        self.rag_keywords = [
            # Advice terms (Indonesian & English)
            'tips', 'saran', 'nasihat', 'advice', 'suggest', 'recommend',
            'strategi', 'strategy', 'cara', 'way', 'method', 'bagaimana cara',
            'rekomendasi', 'recommendation', 'sebaiknya', 'should',
            
            # Improvement terms (Indonesian & English)
            'cara meningkatkan', 'how to improve', 'bagaimana agar', 'how to',
            'meningkatkan', 'improve', 'memperbaiki', 'fix', 'enhance',
            'optimasi', 'optimize', 'maksimalkan', 'maximize',
            
            # General business concepts (Indonesian & English)
            'manajemen', 'management', 'kepemimpinan', 'leadership',
            'pemasaran', 'marketing', 'promosi', 'promotion', 'iklan', 'advertising',
            'pelayanan', 'service', 'customer service', 'layanan pelanggan'
        ]
        
        logger.info("Router initialized successfully")
    
    def _get_sql_score(self, question: str) -> int:
        """Calculate SQL score based on comprehensive keyword matching"""
        question_lower = question.lower()
        score = 0
        
        for keyword in self.sql_keywords:
            if keyword in question_lower:
                score += 1
                # Give extra weight to business-specific terms
                if keyword in ['warung', 'gembira', 'sehat', 'berkah', 'penjualan', 'sales']:
                    score += 1
        
        return score
    
    def _get_rag_score(self, question: str) -> int:
        """Calculate RAG score based on advice/strategy keywords"""
        question_lower = question.lower()
        score = 0
        
        for keyword in self.rag_keywords:
            if keyword in question_lower:
                score += 1
                # Give extra weight to clear advice terms
                if keyword in ['tips', 'saran', 'advice', 'cara meningkatkan', 'how to improve']:
                    score += 2
        
        return score
    
    def classify(self, question: str) -> Literal["SQL", "RAG"]:
        """Classification with better bilingual support"""
        try:
            logger.info(f"Classifying question: {question[:50]}...")
            
            sql_score = self._get_sql_score(question)
            rag_score = self._get_rag_score(question)
            
            logger.info(f"Scores - SQL: {sql_score}, RAG: {rag_score}")
            
            # Clear SQL indicators - prioritize data queries
            if sql_score >= 2:  # Need at least 2 matching keywords for confidence
                logger.info(f"Classification: SQL (score: {sql_score})")
                return "SQL"
            elif rag_score >= 1:  # RAG needs fewer matches since advice keywords are more specific
                logger.info(f"Classification: RAG (score: {rag_score})")
                return "RAG"
            elif sql_score > 0:  # Any SQL keyword without RAG keywords
                logger.info(f"Classification: SQL (score: {sql_score})")
                return "SQL"
            else:
                # Use LLM for unclear cases
                logger.info("No clear patterns, using LLM")
                return self._llm_classify(question)
                
        except Exception as e:
            logger.error(f"Error in classification: {str(e)}")
            return "RAG"
    
    def _llm_classify(self, question: str) -> Literal["SQL", "RAG"]:
        """LLM classification with better context"""
        try:
            prompt = f"""Classify this question as "SQL" or "RAG":

SQL = Questions that need specific business data from database:
- Sales numbers, revenue, profit data
- Product performance, inventory levels
- Transaction counts, payment methods
- Specific business performance metrics
- Time-based data analysis (monthly, yearly trends)
- Comparisons between businesses/products

RAG = Questions about general business advice:
- Tips for improving business
- General strategies and recommendations
- How-to guidance without needing specific data
- General business concepts and best practices

Examples:
SQL: "Berapa penjualan warung kopi bulan ini?" (needs sales data)
SQL: "What are my top selling products?" (needs product data)
RAG: "Tips untuk meningkatkan penjualan" (general advice)
RAG: "How to improve customer service?" (general strategy)

Question: {question}

Answer only "SQL" or "RAG":"""

            response = self.llm.invoke(prompt)
            classification = response.content.strip().upper()
            
            if classification not in ["SQL", "RAG"]:
                classification = "RAG"  # Default fallback
            
            logger.info(f"LLM classification: {classification}")
            return classification
            
        except Exception as e:
            logger.error(f"LLM classification error: {str(e)}")
            return "RAG"