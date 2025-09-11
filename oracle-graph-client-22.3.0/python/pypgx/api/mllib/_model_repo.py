#
# Copyright (C) 2013 - 2022 Oracle and/or its affiliates. All rights reserved.
#
from typing import List

from pypgx._utils.error_handling import java_handler


class ModelRepository:
    """
    ModelRepository object that exposes crud operations on
    - model stores and
    - the models within these model stores.
    """

    _java_class = 'oracle.pgx.api.mllib.ModelRepository'

    def __init__(self, java_generic_model_repository):
        """
        Initialize model repository.

        :param java_generic_model_repository: reference to java object
        """
        self._java_specific_model_repository = java_generic_model_repository

    def create(self, model_store_name: str) -> None:
        """
        Create a new model store.

        :param model_store_name: the name of the model store
        :return: None
        """
        java_handler(self._java_specific_model_repository.create, [model_store_name])

    def delete_model_store(self, model_store_name: str) -> None:
        """
        Delete a model store.

        :param model_store_name: the name of the model store
        :return: None
        """
        java_handler(
            self._java_specific_model_repository.deleteModelStore,
            [model_store_name]
        )

    def list_model_stores_names(self) -> List[str]:
        """
        List the names of all model stores in the model repository.

        :return: List of names.
        """
        return java_handler(self._java_specific_model_repository.listModelStoresNames, [])

    def list_model_stores_names_matching(self, regex: str) -> List[str]:
        """
        List the names of all model stores in the model repository that match the regex.

        :param regex: a regex in form of a string.
        :return: List of matching names.
        """
        return java_handler(
            self._java_specific_model_repository.listModelStoresNamesMatching,
            [regex]
        )

    def list_models(self, model_store_name: str) -> List[str]:
        """
        List the models present in the model store with the given name.

        :param model_store_name: the name of the model store (non-prefixed)
        :return: List of model names.
        """
        return java_handler(
            self._java_specific_model_repository.listModels,
            [model_store_name]
        )

    def get_model_description(self, model_store_name: str, model_name: str) -> str:
        """
        Retrieve the description of the model in the specified model store, with the given model
        name.

        :param model_store_name: the name of the model store
        :param model_name: the name under which the model was stored
        :return: A string containing the description that was stored with the model
        """
        return java_handler(
            self._java_specific_model_repository.getModelDescription,
            [model_store_name, model_name]
        )

    def delete_model(self, model_store_name: str, model_name: str) -> None:
        """
        Delete the model in the specified model store with the given model
        name.

        :param model_store_name: the name of the model store
        :param model_name: the name under which the model was stored
        :return: None
        """
        java_handler(
            self._java_specific_model_repository.deleteModel,
            [model_store_name, model_name]
        )
