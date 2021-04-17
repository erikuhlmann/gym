import os
import numpy as np

from gym import utils
from gym.envs.robotics import fetch_env


# Ensure we get the path separator correct on windows
MODEL_XML_PATH = os.path.join('fetch', 'slide.xml')


class FetchSlideEnv(fetch_env.FetchEnv, utils.EzPickle):
    def __init__(self, reward_type='sparse'):
        initial_qpos = {
            'robot0:slide0': 0.05,
            'robot0:slide1': 0.48,
            'robot0:slide2': 0.0,
            'object0:joint': [1.7, 1.1, 0.41, 1., 0., 0., 0.],
        }
        fetch_env.FetchEnv.__init__(
            self, MODEL_XML_PATH, has_object=True, block_gripper=True, n_substeps=20,
            gripper_extra_height=-0.02, target_in_the_air=False, target_offset=np.array([0.4, 0.0, 0.0]),
            obj_range=0.1, target_range=0.3, distance_threshold=0.05,
            initial_qpos=initial_qpos, reward_type=reward_type)
        utils.EzPickle.__init__(self)

    # bypass the mocap object and set joint angles directly
    def _set_action(self, action):
        qpos = {
            'robot0:shoulder_pan_joint': action[0],
            'robot0:shoulder_lift_joint': action[1],
            'robot0:upperarm_roll_joint': action[2],
            'robot0:elbow_flex_joint': action[3],
            'robot0:wrist_flex_joint': action[4],
            'robot0:wrist_roll_joint': action[5]
        }
        for name, value in qpos.items():
            self.sim.data.set_joint_qpos(name, value)
