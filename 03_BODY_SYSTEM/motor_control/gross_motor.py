# motor_control/gross_motor.py

class GrossMotor:
    """
    Walking, reaching, lifting.
    """

    def execute(self, command: str):
        return {"gross_motor": command}
