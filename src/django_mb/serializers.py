# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from rest_framework import serializers

logger = logging.getLogger(__name__)

registry = {}


class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = None


def serializer_factory(model, base=GeneralSerializer,
                       fields=None, exclude=None, **kwargs):
    meta_attrs = {"model": model, "exclude": [], "auto": True}
    if fields is not None:
        meta_attrs["fields"] = fields
        meta_attrs["exclude"] = None
    elif exclude is not None:
        meta_attrs["fields"] = None
        meta_attrs["exclude"] = exclude

    parent = (object,)
    if hasattr(base, "Meta"):
        parent = (base.Meta, object)
    Meta = type(str("Meta"), parent, meta_attrs)

    class_name = model.__name__ + "Serializer"
    attrs = {"Meta": Meta}
    attrs.update(**kwargs)
    return type(base)(class_name, (base,), attrs)


def serialize(obj):
    if obj.__class__ not in registry:
        registry[obj.__class__] = serializer_factory(obj.__class__)

    serializer_class = registry[obj.__class__]
    serializer = serializer_class(obj)

    meta = obj._meta

    return {
        "key": obj.pk,
        "version": 1,
        "model": "{0.app_label}.{0.model_name}".format(meta),
        "database_table": meta.db_table,
        "payload": {
            "version": getattr(serializer, "VERSION", 1),
            "data": serializer.data
        }
    }
