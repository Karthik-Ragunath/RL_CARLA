import parl
import torch
import torch.nn as nn
import torch.nn.functional as F

# clamp bounds for Std of action_log
LOG_SIG_MAX = 2.0
LOG_SIG_MIN = -20.0

__all__ = ['TorchModel']

# class TorchModel(parl.Model):
#     def __init__(self, obs_dim, action_dim):
#         super(TorchModel, self).__init__()
#         self.actor_model = Actor(obs_dim, action_dim)
#         self.critic_model = Critic(obs_dim, action_dim)
#
#     def policy(self, obs):
#         return self.actor_model(obs)
#
#     def value(self, obs, action):
#         return self.critic_model(obs, action)
#
#
# class Actor(parl.Model):
#     def __init__(self, obs_dim=512, action_dim=2):
#         super(Actor, self).__init__()
#
#         # Original Image - CNN Arch
#         self.cnn_layer_1_1 = nn.Conv2d(3, 24, (5, 5), stride=4)  # (input_channels, output_channels, kernel_size, stride
#         self.cnn_layer_1_2 = nn.Conv2d(24, 36, (5, 5), stride=4)
#         self.cnn_layer_1_3 = nn.Conv2d(36, 48, (5, 5), stride=4)
#         self.cnn_layer_1_4 = nn.Conv2d(48, 64, (3, 3), stride=1)
#         self.cnn_layer_1_5 = nn.Conv2d(64, 64, (3, 3), stride=1)
#         self.fully_connected_layer_1_1 = nn.Linear(64, 128)
#         self.fully_connected_layer_1_2 = nn.Linear(128, 256)
#         self.fully_connected_layer_1_3 = nn.Linear(256, obs_dim)
#
#         # Image With Bounding Box
#         self.cnn_layer_2_1 = nn.Conv2d(3, 24, (5, 5), stride=4)
#         self.cnn_layer_2_2 = nn.Conv2d(24, 36, (5, 5), stride=4)
#         self.cnn_layer_2_3 = nn.Conv2d(36, 48, (5, 5), stride=4)
#         self.cnn_layer_2_4 = nn.Conv2d(48, 64, (3, 3), stride=1)
#         self.cnn_layer_2_5 = nn.Conv2d(64, 64, (3, 3), stride=1)
#         self.fully_connected_layer_2_1 = nn.Linear(64, 128)
#         self.fully_connected_layer_2_2 = nn.Linear(128, 256)
#         self.fully_connected_layer_2_3 = nn.Linear(256, obs_dim)
#
#         self.fusion_fully_connected_layer_1 = nn.Linear(obs_dim * 2, 768)
#         self.fusion_fully_connected_layer_2 = nn.Linear(768, obs_dim)
#
#         self.l1 = nn.Linear(obs_dim, 256)
#         self.l2 = nn.Linear(256, 256)
#         self.l3 = nn.Linear(256, 256)
#
#         self.mean_linear1 = nn.Linear(256, 256)
#         self.mean_linear2 = nn.Linear(256, 256)
#         self.mean_linear = nn.Linear(256, action_dim)
#
#         self.std_linear1 = nn.Linear(256, 256)
#         self.std_linear2 = nn.Linear(256, 256)
#         self.std_linear = nn.Linear(256, action_dim)
#
#     def forward(self, orig_image, bounding_box_image):
#
#         # Original Image - CNN
#         x_cnn_orig = F.relu(self.cnn_layer_1_1(orig_image))
#         x_cnn_orig = F.relu(self.cnn_layer_1_2(x_cnn_orig))
#         x_cnn_orig = F.relu(self.cnn_layer_1_3(x_cnn_orig))
#         x_cnn_orig = F.relu(self.cnn_layer_1_4(x_cnn_orig))
#         x_cnn_orig = F.relu(self.cnn_layer_1_5(x_cnn_orig))
#
#         # Bounding Box Image - CNN
#         x_faster_rcnn = F.relu(self.cnn_layer_2_1(bounding_box_image))
#         x_faster_rcnn = F.relu(self.cnn_layer_2_2(x_faster_rcnn))
#         x_faster_rcnn = F.relu(self.cnn_layer_2_3(x_faster_rcnn))
#         x_faster_rcnn = F.relu(self.cnn_layer_2_4(x_faster_rcnn))
#         x_faster_rcnn = F.relu(self.cnn_layer_2_5(x_faster_rcnn))
#
#         fusion = torch.concat((x_cnn_orig, x_faster_rcnn), 0)
#         fusion = F.relu(self.fusion_fully_connected_layer_1(fusion))
#         fusion = F.relu(self.fusion_fully_connected_layer_2(fusion))
#
#         x = F.relu(self.l1(fusion))
#         x = F.relu(self.l2(x))
#         x = F.relu(self.l3(x))
#
#         act_mean = F.relu(self.mean_linear1(x))
#         act_mean = F.relu(self.mean_linear2(act_mean))
#         act_mean = self.mean_linear(act_mean)
#
#         act_std = F.relu(self.std_linear1(x))
#         act_std = F.relu(self.std_linear2(act_std))
#         act_std = self.std_linear(act_std)
#         act_log_std = torch.clamp(act_std, min=LOG_SIG_MIN, max=LOG_SIG_MAX)
#         return act_mean, act_log_std
#
#
# class Critic(parl.Model):
#     def __init__(self, obs_dim, action_dim):
#         super(Critic, self).__init__()
#
#         # Original Image - CNN Arch
#         self.cnn_layer_1_1 = nn.Conv2d(3, 24, (5, 5), stride=4)  # (input_channels, output_channels, kernel_size, stride
#         self.cnn_layer_1_2 = nn.Conv2d(24, 36, (5, 5), stride=4)
#         self.cnn_layer_1_3 = nn.Conv2d(36, 48, (5, 5), stride=4)
#         self.cnn_layer_1_4 = nn.Conv2d(48, 64, (3, 3), stride=1)
#         self.cnn_layer_1_5 = nn.Conv2d(64, 64, (3, 3), stride=1)
#         self.fully_connected_layer_1_1 = nn.Linear(64, 128)
#         self.fully_connected_layer_1_2 = nn.Linear(128, 256)
#         self.fully_connected_layer_1_3 = nn.Linear(256, obs_dim)
#
#         # Image With Bounding Box
#         self.cnn_layer_2_1 = nn.Conv2d(3, 24, (5, 5), stride=4)
#         self.cnn_layer_2_2 = nn.Conv2d(24, 36, (5, 5), stride=4)
#         self.cnn_layer_2_3 = nn.Conv2d(36, 48, (5, 5), stride=4)
#         self.cnn_layer_2_4 = nn.Conv2d(48, 64, (3, 3), stride=1)
#         self.cnn_layer_2_5 = nn.Conv2d(64, 64, (3, 3), stride=1)
#         self.fully_connected_layer_2_1 = nn.Linear(64, 128)
#         self.fully_connected_layer_2_2 = nn.Linear(128, 256)
#         self.fully_connected_layer_2_3 = nn.Linear(256, obs_dim)
#
#         self.fusion_fully_connected_layer_1 = nn.Linear(obs_dim * 2, 768)
#         self.fusion_fully_connected_layer_2 = nn.Linear(768, obs_dim)
#
#         # Q1 network
#         self.l1 = nn.Linear(obs_dim + action_dim, 256)
#         self.l2 = nn.Linear(256, 256)
#         self.l3 = nn.Linear(256, 256)
#         self.l4 = nn.Linear(256, 256)
#         self.l5 = nn.Linear(256, 1)
#
#         # Q2 network
#         self.l6 = nn.Linear(obs_dim + action_dim, 256)
#         self.l7 = nn.Linear(256, 256)
#         self.l8 = nn.Linear(256, 256)
#         self.l9 = nn.Linear(256, 256)
#         self.l10 = nn.Linear(256, 1)
#
#     def forward(self, orig_image, bounding_box_image, action):
#         # Original Image - CNN
#         x_cnn_orig = F.relu(self.cnn_layer_1_1(orig_image))
#         x_cnn_orig = F.relu(self.cnn_layer_1_2(x_cnn_orig))
#         x_cnn_orig = F.relu(self.cnn_layer_1_3(x_cnn_orig))
#         x_cnn_orig = F.relu(self.cnn_layer_1_4(x_cnn_orig))
#         x_cnn_orig = F.relu(self.cnn_layer_1_5(x_cnn_orig))
#
#         # Bounding Box Image - CNN
#         x_faster_rcnn = F.relu(self.cnn_layer_2_1(bounding_box_image))
#         x_faster_rcnn = F.relu(self.cnn_layer_2_2(x_faster_rcnn))
#         x_faster_rcnn = F.relu(self.cnn_layer_2_3(x_faster_rcnn))
#         x_faster_rcnn = F.relu(self.cnn_layer_2_4(x_faster_rcnn))
#         x_faster_rcnn = F.relu(self.cnn_layer_2_5(x_faster_rcnn))
#
#         fusion = torch.concat((x_cnn_orig, x_faster_rcnn), 0)
#         fusion = F.relu(self.fusion_fully_connected_layer_1(fusion))
#         fusion = F.relu(self.fusion_fully_connected_layer_2(fusion))
#
#         x = torch.cat([fusion, action], 1)
#
#         # Q1
#         q1 = F.relu(self.l1(x))
#         q1 = F.relu(self.l2(q1))
#         q1 = F.relu(self.l3(q1))
#         q1 = F.relu(self.l4(q1))
#         q1 = self.l5(q1)
#
#         # Q2
#         q2 = F.relu(self.l6(x))
#         q2 = F.relu(self.l7(q2))
#         q2 = F.relu(self.l8(q2))
#         q2 = F.relu(self.l9(q2))
#         q2 = self.l10(q2)
#         return q1, q2

class TorchModel(parl.Model):
    def __init__(self, obs_dim, action_dim):
        super(TorchModel, self).__init__()
        # print("Torch Model Called")
        self.actor_model = Actor(obs_dim, action_dim)
        self.critic_model = Critic(obs_dim, action_dim)

    def policy(self, obs):
        return self.actor_model(obs)

    def value(self, obs, action):
        return self.critic_model(obs, action)


class Actor(parl.Model):
    def __init__(self, obs_dim, action_dim):
        super(Actor, self).__init__()

        self.l1 = nn.Linear(obs_dim, 256)
        self.l2 = nn.Linear(256, 256)
        self.l3 = nn.Linear(256, 256)

        self.mean_linear1 = nn.Linear(256, 256)
        self.mean_linear2 = nn.Linear(256, 256)
        self.mean_linear = nn.Linear(256, action_dim)

        self.std_linear1 = nn.Linear(256, 256)
        self.std_linear2 = nn.Linear(256, 256)
        self.std_linear = nn.Linear(256, action_dim)

    def forward(self, obs):
        x = F.relu(self.l1(obs))
        x = F.relu(self.l2(x))
        x = F.relu(self.l3(x))

        act_mean = F.relu(self.mean_linear1(x))
        act_mean = F.relu(self.mean_linear2(act_mean))
        act_mean = self.mean_linear(act_mean)

        act_std = F.relu(self.std_linear1(x))
        act_std = F.relu(self.std_linear2(act_std))
        act_std = self.std_linear(act_std)
        act_log_std = torch.clamp(act_std, min=LOG_SIG_MIN, max=LOG_SIG_MAX)
        return act_mean, act_log_std


class Critic(parl.Model):
    def __init__(self, obs_dim, action_dim):
        super(Critic, self).__init__()

        # Q1 network
        self.l1 = nn.Linear(obs_dim + action_dim, 256)
        self.l2 = nn.Linear(256, 256)
        self.l3 = nn.Linear(256, 256)
        self.l4 = nn.Linear(256, 256)
        self.l5 = nn.Linear(256, 1)

        # Q2 network
        self.l6 = nn.Linear(obs_dim + action_dim, 256)
        self.l7 = nn.Linear(256, 256)
        self.l8 = nn.Linear(256, 256)
        self.l9 = nn.Linear(256, 256)
        self.l10 = nn.Linear(256, 1)

    def forward(self, obs, action):
        x = torch.cat([obs, action], 1)

        # Q1
        q1 = F.relu(self.l1(x))
        q1 = F.relu(self.l2(q1))
        q1 = F.relu(self.l3(q1))
        q1 = F.relu(self.l4(q1))
        q1 = self.l5(q1)

        # Q2
        q2 = F.relu(self.l6(x))
        q2 = F.relu(self.l7(q2))
        q2 = F.relu(self.l8(q2))
        q2 = F.relu(self.l9(q2))
        q2 = self.l10(q2)
        return q1, q2
