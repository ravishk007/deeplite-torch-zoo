import os

import torch
from torchvision import datasets, transforms
from torch.utils.data.dataloader import default_collate


__all__ = ["get_imagenet", "get_imagenet10", "get_imagenet16"]


def get_imagenet10(data_root="", batch_size=128, num_workers=4, fp16=False, device="cuda", **kwargs):
    return get_imagenet(
            data_root=data_root,
            batch_size=batch_size,
            num_workers=num_workers,
            fp16=fp16,
            device=device
        )


def get_imagenet16(data_root="", batch_size=128, num_workers=4, fp16=False, device="cuda", **kwargs):
    return get_imagenet(
            data_root=data_root,
            batch_size=batch_size,
            num_workers=num_workers,
            fp16=fp16,
            device=device
        )


def get_imagenet(data_root="", batch_size=128, num_workers=4, fp16=False, device="cuda", **kwargs):

    if len(kwargs):
        import sys
        print(f"Warning, {sys._getframe().f_code.co_name}: extra arguments {list(kwargs.keys())}!")

    def half_precision(x):
        if fp16:
            x = [_x.half() if isinstance(_x, torch.FloatTensor) else _x for _x in x]
        return x

    def assign_device(x):
        if x[0].is_cuda ^ (device == "cuda"):
            return x
        return [v.to(device) for v in x]

    train_dataset = datasets.ImageFolder(
        os.path.join(data_root, "imagenet_training"),
        transforms.Compose(
            [
                transforms.RandomResizedCrop(224),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        ),
    )

    test_dataset = datasets.ImageFolder(
        os.path.join(data_root, "imagenet_val"),
        transforms.Compose(
            [
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        ),
    )

    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        pin_memory=True,
        num_workers=num_workers,
        collate_fn=lambda x: half_precision(assign_device(default_collate(x))),
    )

    test_loader = torch.utils.data.DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        pin_memory=True,
        num_workers=num_workers,
        collate_fn=lambda x: half_precision(assign_device(default_collate(x))),
    )

    return {"train": train_loader, "test": test_loader}
