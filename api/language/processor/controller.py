import os
import language.processor.etc as etc
import logging


def processor(mapping, user):
    for mapping_child in mapping:
        etc.main(mapping=mapping_child, user=user)
