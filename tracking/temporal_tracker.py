import time


class TemporalTracker:
    def __init__(self, min_duration=2.0):
        """
        min_duration: seconds a face must persist
        """
        self.min_duration = min_duration
        self.first_seen = {}
        self.marked = set()

    def update(self, name):
        """
        Called every frame with the recognized name.
        Returns True if attendance should be marked now.
        """
        current_time = time.time()

        # Ignore unknowns
        if name == "Unknown":
            return False

        # Already marked
        if name in self.marked:
            return False

        # First time seeing this name
        if name not in self.first_seen:
            self.first_seen[name] = current_time
            return False

        # Check persistence
        elapsed = current_time - self.first_seen[name]
        if elapsed >= self.min_duration:
            self.marked.add(name)
            return True

        return False