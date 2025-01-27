from torch.hub import load_state_dict_from_url
from deeplite_torch_zoo.src.classification.mobilenets.mobilenetv1 import MobileNetV1
from deeplite_torch_zoo.wrappers.registries import MODEL_WRAPPER_REGISTRY


__all__ = ["mobilenet_v1_vww"]

model_urls = {
    "mobilenetv1": "http://download.deeplite.ai/zoo/models/mobilenetv1-vww-84f65dc4bc649cd6.pth",
}


def _mobilenetv1_vww(arch, pretrained=False, progress=True, device='cuda'):
    model = MobileNetV1()

    if pretrained:
        state_dict = load_state_dict_from_url(
            model_urls[arch], progress=progress, check_hash=True
        )
        model.load_state_dict(state_dict)
    return model.to(device)


@MODEL_WRAPPER_REGISTRY.register(model_name='mobilenet_v1', dataset_name='vww', task_type='classification')
def mobilenet_v1_vww(pretrained=False, progress=True, device='cuda'):
    return _mobilenetv1_vww("mobilenetv1", pretrained=pretrained, progress=progress, device=device)
