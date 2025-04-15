_progress = 0

def reset_progress():
    global _progress
    _progress = 0

def update_progress(increment: int):
    global _progress
    _progress += increment

def get_progress():
    return _progress
