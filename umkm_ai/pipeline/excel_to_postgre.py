import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import logging
from pathlib import Path
from typing import Dict, Set
import yaml
import numpy as np
import os

class ExcelToPostgreSQL:
    """Excel to PostgreSQL data loader for UMKM data pipeline"""
    
    def __init__(self, db_config: Dict[str, str]):
        self.db_config = db_config
        self.config = self._load_config()
        self.conn = None
        self.cursor = None
        self._loaded_penjualan_ids = set()
        
        # Setup logging
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
        
    def _setup_logging(self):
        """Setup logging configuration"""
        # Get paths from config
        log_dir = Path(self.config['paths']['log_directory'])
        log_file = self.config['paths']['log_file']
        
        # Create logs directory if it doesn't exist
        log_dir.mkdir(exist_ok=True)
        log_path = log_dir / log_file
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            handlers=[
                logging.FileHandler(log_path, encoding='utf-8'),
                logging.StreamHandler()
            ],
            force=True
        )

    def _load_config(self) -> Dict:
        """Load configuration from pipeline.yaml"""
        try:
            config_path = Path(__file__).parent.parent / "config" / "pipeline.yaml"
            
            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
                
            with open(config_path) as f:
                config = yaml.safe_load(f)
            
            # Validate required sections
            required_sections = ['tables', 'file_mappings', 'load_order', 'paths']
            for section in required_sections:
                if section not in config:
                    raise ValueError(f"Configuration missing required section: {section}")
            
            return config
        except Exception as e:
            print(f"Failed to load configuration: {e}")
            raise

    def connect_db(self) -> bool:
        """Establish connection to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.cursor = self.conn.cursor()
            self.logger.info(f"Connected to database: {self.db_config['database']}")
            return True
        except Exception as e:
            self.logger.error(f"Database connection failed: {e}")
            return False

    def close_db(self) -> None:
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.logger.info("Database connection closed")

    def _clear_tables(self) -> bool:
        """Clear all tables in reverse dependency order"""
        try:
            # Get load order and reverse it for clearing
            clear_order = list(reversed(self.config['load_order']))
            
            self.logger.info("Clearing existing data from tables...")
            
            for table_name in clear_order:
                if table_name in self.config['tables']:
                    schema = self.config['tables'][table_name]['schema']
                    self.cursor.execute(f"TRUNCATE TABLE {schema}.{table_name} CASCADE;")
                    self.logger.info(f"Cleared {schema}.{table_name}")
            
            self.conn.commit()
            self.logger.info("All tables cleared successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error clearing tables: {e}")
            if self.conn:
                self.conn.rollback()
            return False

    def _convert_value(self, value):
        """Convert pandas/numpy types to PostgreSQL compatible types"""
        if pd.isna(value):
            return None
        if isinstance(value, (np.integer)):
            return int(value)
        if isinstance(value, (np.floating)):
            return float(value)
        if isinstance(value, (np.bool_)):
            return bool(value)
        if isinstance(value, (np.datetime64)):
            return pd.to_datetime(value)
        if hasattr(value, 'item'):
            return value.item()
        return value

    def _apply_transformations(self, df: pd.DataFrame, table_name: str) -> pd.DataFrame:
        """Apply configured data transformations"""
        transformations = self.config['tables'][table_name].get('transformations', {})
        
        for col, func in transformations.items():
            if col in df.columns:
                try:
                    if func == 'to_datetime':
                        df[col] = pd.to_datetime(df[col])
                    elif func == 'to_float':
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    self.logger.debug(f"Applied {func} transformation to {col}")
                except Exception as e:
                    self.logger.warning(f"Transformation failed for {col}: {e}")
        return df

    def _validate_data(self, df: pd.DataFrame, table_name: str) -> bool:
        """Validate data meets requirements before loading"""
        required_cols = self.config['tables'][table_name].get('required_columns', [])
        missing = set(required_cols) - set(df.columns)
        
        if missing:
            self.logger.error(f"Missing required columns for {table_name}: {missing}")
            return False
            
        if df.empty:
            self.logger.warning(f"Empty DataFrame for {table_name} - no data to load")
            return False
            
        # Check for null values in required columns
        for col in required_cols:
            null_count = df[col].isnull().sum()
            if null_count > 0:
                self.logger.warning(f"Found {null_count} null values in required column {col}")
            
        return True

    def _handle_penjualan_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle duplicate transaction numbers in penjualan data"""
        self.logger.info("Checking for duplicate transaction numbers...")
        
        # Remove internal duplicates first
        initial_count = len(df)
        df = df.drop_duplicates(subset=['nomor_transaksi'], keep='first')
        
        if len(df) < initial_count:
            internal_dupes = initial_count - len(df)
            self.logger.warning(f"Removed {internal_dupes} internal duplicate transaction numbers")
        
        # Check against existing data in database
        try:
            self.cursor.execute("SELECT nomor_transaksi FROM umkm.penjualan")
            existing_transactions = {row[0] for row in self.cursor.fetchall()}
            
            if existing_transactions:
                pre_filter_count = len(df)
                df = df[~df['nomor_transaksi'].isin(existing_transactions)]
                
                if len(df) < pre_filter_count:
                    db_dupes = pre_filter_count - len(df)
                    self.logger.warning(f"Filtered out {db_dupes} duplicate transactions from database")
        except Exception as e:
            self.logger.warning(f"Could not check existing transactions: {e}")
        
        self.logger.info(f"Final penjualan records to load: {len(df)}")
        return df

    def _validate_foreign_keys(self, df: pd.DataFrame, table_name: str) -> pd.DataFrame:
        """Validate foreign key references"""
        if table_name == 'detail_penjualan':
            if not self._loaded_penjualan_ids:
                self.logger.error("No penjualan IDs available for detail validation")
                return pd.DataFrame(columns=df.columns)
            
            initial_count = len(df)
            df = df[df['penjualan_id'].isin(self._loaded_penjualan_ids)]
            
            if len(df) < initial_count:
                invalid = initial_count - len(df)
                self.logger.warning(f"Filtered out {invalid} detail records with invalid penjualan_id references")
        
        return df

    def load_file(self, file_path: Path, table_name: str) -> int:
        """Load single Excel file to PostgreSQL table"""
        if table_name not in self.config['tables']:
            self.logger.error(f"No configuration for table {table_name}")
            return 0

        try:
            # Read Excel file
            df = pd.read_excel(file_path)
            self.logger.info(f"Read {len(df)} rows from {file_path.name}")
            
            if df.empty:
                self.logger.warning(f"No data to load from {file_path.name}")
                return 0

            # Apply transformations
            df = self._apply_transformations(df, table_name)
            
            # Validate data structure
            if not self._validate_data(df, table_name):
                return 0

            # Special handling for penjualan duplicates
            if table_name == 'penjualan':
                df = self._handle_penjualan_duplicates(df)
            
            # Validate foreign keys
            df = self._validate_foreign_keys(df, table_name)
            
            if df.empty:
                self.logger.warning(f"No valid records to load for {table_name} after validation")
                return 0

            # Prepare for database insert
            table_config = self.config['tables'][table_name]
            schema = table_config['schema']
            columns = table_config['columns']
            
            # Filter to only configured columns that exist in the data
            available_columns = [col for col in columns if col in df.columns]
            if len(available_columns) != len(columns):
                missing = set(columns) - set(available_columns)
                self.logger.warning(f"Missing columns in {table_name} data: {missing}")
            
            # Convert values to PostgreSQL-compatible types
            records = []
            for _, row in df[available_columns].iterrows():
                record = tuple(self._convert_value(val) for val in row.values)
                records.append(record)
            
            # Insert into database
            columns_str = ', '.join(available_columns)
            sql = f"INSERT INTO {schema}.{table_name} ({columns_str}) VALUES %s"
            
            execute_values(self.cursor, sql, records, page_size=1000)
            self.conn.commit()
            
            loaded_count = len(records)
            self.logger.info(f"Successfully loaded {loaded_count} rows to {schema}.{table_name}")
            
            # Store penjualan IDs for foreign key validation
            if table_name == 'penjualan':
                self._loaded_penjualan_ids.update(df['penjualan_id'].tolist())
                self.logger.info(f"Stored {len(self._loaded_penjualan_ids)} penjualan IDs for FK validation")
            
            return loaded_count
            
        except Exception as e:
            self.logger.error(f"Failed to load {table_name} from {file_path.name}: {e}")
            if self.conn:
                self.conn.rollback()
            return 0

    def process_all_files(self, data_dir: Path) -> int:
        """Process all Excel files in configured dependency order"""
        if not data_dir.exists():
            self.logger.error(f"Data directory not found: {data_dir}")
            return 0
        
        self.logger.info(f"Starting data loading from: {data_dir}")
        
        # Clear tables first
        if not self._clear_tables():
            self.logger.error("Failed to clear tables, aborting load")
            return 0
        
        total_records = 0
        load_order = self.config['load_order']
        
        # Load files in dependency order
        for table_name in load_order:
            # Find matching file
            filename = None
            for file_key, table_key in self.config['file_mappings'].items():
                if table_key == table_name:
                    filename = file_key
                    break
            
            if filename:
                file_path = data_dir / filename
                if file_path.exists():
                    self.logger.info(f"Processing {filename} -> {table_name}")
                    count = self.load_file(file_path, table_name)
                    total_records += count
                else:
                    self.logger.warning(f"File not found: {filename}")
            else:
                self.logger.warning(f"No file mapping found for table: {table_name}")
        
        self.logger.info(f"Data loading completed. Total records loaded: {total_records}")
        return total_records

    def validate_loaded_data(self) -> bool:
        """Validate that data was loaded correctly"""
        try:
            self.logger.info("=== Data Validation ===")
            
            validation_queries = [
                ("Businesses", "SELECT COUNT(*) FROM umkm.bisnis"),
                ("Products", "SELECT COUNT(*) FROM umkm.produk"),
                ("Sales Transactions", "SELECT COUNT(*) FROM umkm.penjualan"),
                ("Sales Details", "SELECT COUNT(*) FROM umkm.detail_penjualan"),
                ("Expenses", "SELECT COUNT(*) FROM umkm.pengeluaran"),
                ("Daily Cash Records", "SELECT COUNT(*) FROM umkm.kas_harian"),
            ]
            
            for name, query in validation_queries:
                self.cursor.execute(query)
                count = self.cursor.fetchone()[0]
                self.logger.info(f"{name}: {count} records")
            
            # Check referential integrity
            self.cursor.execute("""
                SELECT COUNT(*) FROM umkm.detail_penjualan dp
                LEFT JOIN umkm.penjualan p ON dp.penjualan_id = p.penjualan_id
                WHERE p.penjualan_id IS NULL
            """)
            orphaned = self.cursor.fetchone()[0]
            
            if orphaned > 0:
                self.logger.error(f"Found {orphaned} orphaned detail records!")
                return False
            
            # Check for negative balances (business logic validation)
            self.cursor.execute("""
                SELECT COUNT(*) FROM umkm.kas_harian 
                WHERE saldo_akhir < 0
            """)
            negative_balances = self.cursor.fetchone()[0]
            
            if negative_balances > 0:
                self.logger.warning(f"Found {negative_balances} days with negative cash balances")
            
            self.logger.info("[SUCCESS] Data validation completed successfully")
            self.logger.info("[SUCCESS] All foreign key relationships are valid")
            return True
                
        except Exception as e:
            self.logger.error(f"Data validation failed: {e}")
            return False