import argparse
import logging
import sys
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def run_gradio():
    """Run Gradio interface"""
    try:
        from interfaces.gradioapp import GradioApp
        
        logger.info("Starting Gradio interface...")
        app = GradioApp()
        app.launch()
        
    except ImportError as e:
        logger.error(f"Failed to import Gradio interface: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error starting Gradio interface: {str(e)}")
        sys.exit(1)

def main():
    """Main application runner"""
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Mas Warung - AI UMKM Assistant")
    parser.add_argument(
        "--gradio", "-g",
        action="store_true",
        help="Run Gradio web interface"
    )
    
    args = parser.parse_args()
    
    # Check if no arguments provided, default to gradio
    if not args.gradio:
        print("Mas Warung - AI UMKM Assistant")
        print("Usage:")
        print("  python main.py --gradio or  python main.py -g    (Run Gradio web interface)")
        run_gradio()
    else:
        run_gradio()

if __name__ == "__main__":
    main()