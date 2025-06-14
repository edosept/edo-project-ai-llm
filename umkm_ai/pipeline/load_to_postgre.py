#!/usr/bin/env python3
"""
Main script for UMKM Excel to PostgreSQL data loading pipeline
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Add the pipeline directory to Python path
sys.path.append(str(Path(__file__).parent))

from excel_to_postgre import ExcelToPostgreSQL

def setup_logging():
    """Setup logging for the main script"""
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "excel_ingestion.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ],
        force=True
    )
    
    return logging.getLogger(__name__)

def load_db_config() -> dict:
    """Load database configuration from environment variables"""
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    # Validate required configuration
    required_keys = ['database', 'user', 'password']
    missing = [key for key in required_keys if not config[key]]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(f'DB_{key.upper()}' for key in missing)}")
    
    return config

def validate_prerequisites(data_dir: Path, config_path: Path) -> bool:
    """Validate that all required files and directories exist"""
    logger = logging.getLogger(__name__)
    
    # Check data directory
    if not data_dir.exists():
        logger.error(f"Data directory not found: {data_dir}")
        logger.info("Please ensure your Excel files are generated in the data directory")
        return False
    
    # Check config file
    if not config_path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        logger.info("Please ensure pipeline.yaml exists in the config directory")
        return False
    
    # Check for Excel files
    excel_files = list(data_dir.glob("*.xlsx"))
    if not excel_files:
        logger.error("No Excel files found in data directory")
        logger.info("Please run your data generation script first")
        return False
    
    logger.info(f"Found {len(excel_files)} Excel files:")
    for file in sorted(excel_files):
        file_size = file.stat().st_size
        logger.info(f"  - {file.name} ({file_size:,} bytes)")
    
    return True

def display_summary(total_loaded: int, validation_passed: bool, logger):
    """Display pipeline execution summary"""
    logger.info("=" * 50)
    logger.info("PIPELINE EXECUTION SUMMARY")
    logger.info("=" * 50)
    
    if total_loaded > 0:
        logger.info(f"[SUCCESS] Total records loaded: {total_loaded:,}")
        
        if validation_passed:
            logger.info("[SUCCESS] Data validation: PASSED")
            logger.info("[SUCCESS] Pipeline status: SUCCESS")
            logger.info("")
            logger.info("Your UMKM data has been successfully loaded to PostgreSQL!")
            logger.info("You can now run queries and analysis on your data.")
        else:
            logger.error("[FAILED] Data validation: FAILED")
            logger.error("[FAILED] Pipeline status: FAILED")
            logger.info("Please check the logs for validation errors.")
    else:
        logger.error("[FAILED] No data was loaded")
        logger.error("[FAILED] Pipeline status: FAILED")
        logger.info("Please check the logs for loading errors.")
    
    logger.info("=" * 50)

def main() -> int:
    """Main execution function"""
    loader = None
    logger = None
    
    try:
        # Setup logging first
        logger = setup_logging()
        logger.info("=" * 60)
        logger.info("UMKM DATA LOADING PIPELINE STARTING")
        logger.info("=" * 60)
        
        # Load environment variables
        load_dotenv()
        logger.info("Environment variables loaded")
        
        # Setup paths
        current_dir = Path(__file__).parent
        project_root = current_dir.parent
        data_dir = project_root / "data"
        config_path = project_root / "config" / "pipeline.yaml"
        
        logger.info(f"Project root: {project_root}")
        logger.info(f"Data directory: {data_dir}")
        logger.info(f"Config file: {config_path}")
        
        # Load database configuration
        try:
            db_config = load_db_config()
            logger.info(f"Database configuration loaded for: {db_config['database']}")
        except ValueError as e:
            logger.error(f"Database configuration error: {e}")
            logger.info("Please check your .env file contains all required database settings")
            return 1
        
        # Validate prerequisites
        if not validate_prerequisites(data_dir, config_path):
            logger.error("Prerequisites validation failed")
            return 1
        
        logger.info("All prerequisites validated successfully")
        
        # Initialize data loader
        try:
            loader = ExcelToPostgreSQL(db_config)
            logger.info("Data loader initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize data loader: {e}")
            return 1
        
        # Connect to database
        if not loader.connect_db():
            logger.error("Failed to connect to database")
            logger.info("Please check your database is running and credentials are correct")
            return 1
        
        # Process all files
        logger.info("Starting file processing...")
        total_loaded = loader.process_all_files(data_dir)
        
        if total_loaded > 0:
            logger.info(f"File processing completed - {total_loaded:,} records loaded")
            
            # Validate loaded data
            logger.info("Starting data validation...")
            validation_passed = loader.validate_loaded_data()
            
            # Display summary
            display_summary(total_loaded, validation_passed, logger)
            
            return 0 if validation_passed else 1
        else:
            logger.error("No data was loaded - pipeline failed")
            display_summary(0, False, logger)
            return 1
        
    except KeyboardInterrupt:
        if logger:
            logger.info("Pipeline interrupted by user")
        return 1
    except Exception as e:
        if logger:
            logger.error(f"Pipeline failed with unexpected error: {e}")
            logger.exception("Full error details:")
        else:
            print(f"Critical error before logging setup: {e}")
        return 1
    finally:
        # Cleanup database connection
        if loader:
            try:
                loader.close_db()
            except Exception as e:
                if logger:
                    logger.warning(f"Error closing database connection: {e}")

if __name__ == "__main__":
    """Entry point for the script"""
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"Critical startup error: {e}")
        sys.exit(1)