
from torchvision import models
from torch.hub import load_state_dict_from_url
from deeplite_torch_zoo.wrappers.registries import MODEL_WRAPPER_REGISTRY


__all__ = ["mobilenet_v2_tinyimagenet"]


model_urls = {
    "mobilenet_v2": "http://download.deeplite.ai/zoo/models/mobilenet_v2_tinyimagenet_0-6803-4ec21929b72f0b4d.pt",
}


@MODEL_WRAPPER_REGISTRY.register(model_name='mobilenet_v2', dataset_name='tinyimagenet', task_type='classification')
def mobilenet_v2_tinyimagenet(pretrained=False, progress=True, device="cuda"):
    model = models.mobilenet_v2(num_classes=100)
    if pretrained:
        state_dict = load_state_dict_from_url(
            model_urls["mobilenet_v2"], progress=progress, check_hash=True, map_location=device
        )
        model.load_state_dict(state_dict)
    return model.to(device)
