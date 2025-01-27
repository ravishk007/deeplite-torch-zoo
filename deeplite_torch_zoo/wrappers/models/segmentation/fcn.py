from torch.hub import load_state_dict_from_url

from torchfcn.models import FCN32s as FCN
from deeplite_torch_zoo.wrappers.registries import MODEL_WRAPPER_REGISTRY


__all__ = ["fcn32_voc_20"]


model_urls = {
    "fcn32_voc_20": "http://download.deeplite.ai/zoo/models/fcn32-voc-20_713-b745bd7e373e31d1.pth",
}


def fcn32(
    net="fcn32",
    dataset="voc_20",
    num_classes=21,
    pretrained=False,
    progress=True,
    device="cuda",
):
    model = FCN(n_class=num_classes)
    if pretrained:
        state_dict = load_state_dict_from_url(
            model_urls[f"{net}_{dataset}"], progress=progress, check_hash=True, map_location=device
        )
        model.load_state_dict(state_dict)
    return model.to(device)


@MODEL_WRAPPER_REGISTRY.register(model_name='fcn32', dataset_name='voc_20', task_type='semantic_segmentation')
def fcn32_voc_20(pretrained=True, progress=False, device='cuda'):
    return fcn32(
        net="fcn32",
        dataset="voc_20",
        num_classes=21,
        pretrained=pretrained,
        progress=progress,
        device=device,
    )
