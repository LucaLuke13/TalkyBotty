
import argparse
from src.talkybotty.main import talkyBotty
def print_help():
    print("Usage: python main.py [options]\n")
    print("Options:")
    print("  -h, --help      Show this help message and exit.")
    print("  -d, --debug     Enable debug logging.")
    print("\nExample:")
    print("  python main.py --debug\n")

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Telegram Voice Message Transcriber')
    
    
    #parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()


    # Initialize the Telegram client with the debug flag
    talkyBotty.run(args)
    #tg = Telegram(debug=args.debug)
