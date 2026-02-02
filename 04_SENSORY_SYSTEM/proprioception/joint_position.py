# proprioception/joint_position.py

class JointPositionSense:
    """
    Reports joint angles.
    """

    def sense(self, joint_angles):
        return {"joint_positions": joint_angles}
