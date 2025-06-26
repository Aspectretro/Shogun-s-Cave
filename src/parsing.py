# Helper functions for parsing user input

def parse_int(arg: str):
    """Parse a string into an int, returning None if it fails"""

    try:
        return int(arg)
    except:
        return None
