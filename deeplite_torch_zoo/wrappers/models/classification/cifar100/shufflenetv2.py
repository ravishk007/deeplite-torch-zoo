"""shufflenetv2 in pytorch

[1] Ningning Ma, Xiangyu Zhang, Hai-Tao Zheng, Jian Sun
    ShuffleNet V2: Practical Guidelines for Efficient CNN Architecture Design
    https://arxiv.org/abs/1807.11164
[2] Implementation
    https://github.com/weiaicunzai/pytorch-cifar100

"""


from torch.hub import load_state_dict_from_url
from deeplite_torch_zoo.src.classification.cifar_models.shufflenetv2 import ShuffleNetV2
from deeplite_torch_zoo.wrappers.registries import MODEL_WRAPPER_REGISTRY


__all__ = ["shufflenet_v2_1_0_cifar100"]


model_urls = {
    "shufflenet_v2": "http://download.deeplite.ai/zoo/models/shufflenet_v2_l.0-cifar100-16ae6f50f5adecad.pth",
}


def _shufflenetv2(arch, net_size=1, pretrained=False, progress=True, device='cuda'):
    model = ShuffleNetV2(net_size)
    if pretrained:
        state_dict = load_state_dict_from_url(
            model_urls[arch], progress=progress, check_hash=True
        )
        model.load_state_dict(state_dict)
    return model.to(device)


@MODEL_WRAPPER_REGISTRY.register(model_name='shufflenet_v2_1_0', dataset_name='cifar100', task_type='classification')
def shufflenet_v2_1_0_cifar100(pretrained=False, progress=True, device='cuda'):
    return _shufflenetv2(
        "shufflenet_v2", net_size=1, pretrained=pretrained, progress=progress, device=device
    )
