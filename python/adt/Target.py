class Target:
    def __init__(self, confidence, x=-1, y=-1, centroid=(-1, -1)):
        self.x = x
        self.y = y
        self.confidence = confidence
        self.centroid = centroid
