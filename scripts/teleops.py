from inputs import get_gamepad
import time

ps4_code = {
    "left_x": "ABS_X",
    "left_y": "ABS_Y",
    "right_x": "ABS_RX",
    "right_y": "ABS_RY",
    "left_trigger": "ABS_Z",
    "right_trigger": "ABS_RZ",
    "left_bumper": "BTN_TL",
    "right_bumper": "BTN_TR",
}

class Controller:
    def __init__(self):
        self.default()

    def get_value(self, count):
        return self.waist, self.shoulder, self.elbow, self.wrist_angle, self.wrist_rotate, self.gripper
    
    def default(self):
        self.waist = 0
        self.shoulder = 0
        self.elbow = 0
        self.wrist_angle = 0
        self.wrist_rotate = 0
        self.gripper = 0

class Teleops:
    def __init__(self):
        self.left_x = 0
        self.left_y = 0

        self.right_x = 0
        self.right_y = 0

        self.left_trigger = 0
        self.right_trigger = 0
        
        self.left_bumper = 0
        self.right_bumper = 0
    
    def update(self):
        events = get_gamepad()
        for event in events:
            if event.code == ps4_code['left_x']:
                self.left_x = self.joy_parse(event.state)
            if event.code == ps4_code['left_y']:
                self.left_y = self.joy_parse(event.state)
            if event.code == ps4_code['right_x']:
                self.right_x = self.joy_parse(event.state)
            if event.code == ps4_code['right_y']:
                self.right_y = self.joy_parse(event.state)
            if event.code == ps4_code['left_trigger']:
                self.left_trigger = self.trigger_parse(event.state)
            if event.code == ps4_code['right_trigger']:
                self.right_trigger = self.trigger_parse(event.state)
            if event.code == ps4_code['left_bumper']:
                self.left_bumper = event.state
            if event.code == ps4_code['right_bumper']:
                self.right_bumper = event.state
            
    def joy_parse(self, state):
        # cap value within the superscribed square
        state -= 128
        if state > 90:
            state = 90
        if state < -90:
            state = -90
        # normalize to between -1 and 1     
        return state / 90

    def trigger_parse(self, state):
        return state / 255

class Pincher_teleops(Teleops, Controller): 
    def __init__(self, pwm_max = 500, gripper_multiplier = 5):
        Teleops.__init__(self)
        Controller.__init__(self)
        self.pwm_max = pwm_max
        self.gripper_multiplier = gripper_multiplier

    def get_value(self, count):
        Teleops.update(self)
        self.waist = int(self.left_x * self.pwm_max)
        self.shoulder = int(self.left_y * self.pwm_max)
        self.elbow = int((self.right_trigger - self.left_trigger) * self.pwm_max)
        self.wrist_angle = int(self.right_y * self.pwm_max)
        self.wrist_rotate = int(self.right_x * self.pwm_max)
        self.get_gripper_pwm()
        return Controller.get_value(self, count)

    def get_gripper_pwm(self):
        if self.left_bumper == 1 and self.right_bumper == 1:
            self.gripper = 0
        elif self.left_bumper == 1 and self.gripper > -self.pwm_max + self.gripper_multiplier:
            self.gripper -= self.gripper_multiplier
        elif self.right_bumper == 1 and self.gripper < self.pwm_max - self.gripper_multiplier:
            self.gripper += self.gripper_multiplier