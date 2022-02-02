# Copyright (C) 2020-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0


class Registry:
    """ Generic registry implentation taken from
    https://github.com/openvinotoolkit/openvino/blob/master/tools/pot/openvino/tools/pot/utils/registry.py """

    def __init__(self, name):
        self._name = name
        self._registry_dict = dict()

    def register(self, name=None):
        def _register(obj_name, obj):
            if obj_name in self._registry_dict:
                raise KeyError('{} is already registered in {}'.format(name, self._name))
            self._registry_dict[obj_name] = obj

        def wrap(obj):
            cls_name = name
            if cls_name is None:
                cls_name = obj.__name__
            _register(cls_name, obj)
            return obj

        return wrap

    def get(self, name):
        if name not in self._registry_dict:
            raise KeyError('{} was not found in the {} '.format(name, self._name))
        return self._registry_dict[name]

    @property
    def registry_dict(self):
        return self._registry_dict

    @property
    def name(self):
        return self._name


class TupleKeyRegistry(Registry):
    """
    Registry class with key as a tuple of 2 items
    """

    def register(self, key1, key2=None):
        def wrap(func):
            model_key = (key1, key2)
            if model_key in self._registry_dict:
                raise KeyError('Key {} is already registered in {}'.format(model_key, self._name))
            self._registry_dict[model_key] = func
            return func

        return wrap
