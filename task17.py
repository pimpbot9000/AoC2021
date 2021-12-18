
class Probe:
    def __init__(self, vx, vy, target):
        """
        :param target ((int,int), (int,int)
        """
        self.x = 0
        self.y = 0
        self.max_y = 0
        self.vx = vx
        self.vy = vy
        self.target_x, self.target_y = target
    
    def step(self):
        self.x += self.vx
        self.y += self.vy
        self.max_y = max(self.max_y, self.y)
        if self.vx > 0:
            self.vx -= 1
        elif self.vx < 0:
            self.vx += 1
        
        self.vy -= 1

    def is_missed(self):
        # Missile has moved below the target area
        return self.y < self.target_y[0]

    def is_hit(self):
        # Probe is inside the target area
        return self.target_x[0] <= self.x <= self.target_x[1] and self.target_y[0] <= self.y <= self.target_y[1]
    
    def simulate(self):        
        
        while not self.is_missed():
            self.step()
            if self.is_hit():
                return self.max_y, True
        return self.max_y, False
    
    def max_horizonal_position(self):
        previous_x = 0
        while True:
            self.step()
            if previous_x == self.x:
                return self.x
            previous_x = self.x

target_area = ((14, 50), (-267, -225))


        

