import sys
def main(value):
    print(f"Received value: {value}")  # Process the value
if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])