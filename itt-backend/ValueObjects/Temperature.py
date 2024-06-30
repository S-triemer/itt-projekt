import random
class Temperature:
    def __init__(self,desired_temp):
            self.value = random.uniform(18.0, 26.0)
            self.desired_temp = desired_temp

    def reach_outside_temp(self, outside_temp):
        if self.value < outside_temp:
            self.value += 0.1
        elif self.value > outside_temp:
            self.value -= 0.1
        return self.value
    
    def reach_desired_temp(self):
        if self.value < self.desired_temp:
            self.value += 0.1
        elif self.value > self.desired_temp:
            self.value -= 0.1
        return self.value
    
    def decrease(self, amount=0.1, min_temp=10.0):
        if self.value > min_temp:
            self.value -= amount
        return self.value
    
    def increase(self, amount=0.1, max_temp=26.0):
        if self.value < max_temp:
            self.value += amount
        return self.value