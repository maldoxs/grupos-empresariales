#
# Copyright (C) 2013 - 2022 Oracle and/or its affiliates. All rights reserved.
#

from pypgx._utils.error_handling import java_handler

from pypgx.api._pgx_graph import PgxGraph
from pypgx.api._pgx_entity import PgxVertex
from pypgx.api.mllib._gnn_explainer import GnnExplainer
from pypgx.api.mllib._gnn_explanation import GnnExplanation
from pypgx._utils import conversion

from typing import Union


class UnsupervisedGnnExplainer(GnnExplainer):
    """UnsupervisedGnnExplainer used to request explanations from unsupervised model predictions."""

    _java_class = "oracle.pgx.api.mllib.UnsupervisedGnnExplainer"

    def infer_and_explain(
        self, graph: PgxGraph, vertex: Union[PgxVertex, int, str]
    ) -> GnnExplanation:
        """Perform inference on the specified vertex and generate an explanation that contains
        scores of how important each property and each vertex in the computation graph is for the
        embeddings position relative to embeddings of other vertices in the graph.

        :param graph: the graph
        :param vertex: the vertex
        :return: explanation containing feature importance and vertex importance.
        """
        java_vertex = conversion.to_java_vertex(graph, vertex)
        return GnnExplanation(
            java_handler(
                self._explainer.inferAndExplain, [graph._graph, java_vertex]
            )
        )

    @property
    def num_clusters(self) -> int:
        """Get number of clusters.

        :return: number of clusters
        :rtype: int
        """
        return java_handler(self._explainer.numClusters, [])

    @num_clusters.setter
    def num_clusters(self, clusters: int):
        java_handler(self._explainer.numClusters, [clusters])

    @property
    def num_samples(self) -> int:
        """Get number of samples.

        :return: number of samples
        :rtype: int
        """
        return java_handler(self._explainer.numSamples, [])

    @num_samples.setter
    def num_samples(self, samples: int):
        java_handler(self._explainer.numSamples, [samples])
