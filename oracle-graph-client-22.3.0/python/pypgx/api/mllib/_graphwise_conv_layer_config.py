#
# Copyright (C) 2013 - 2022 Oracle and/or its affiliates. All rights reserved.
#

from pypgx._utils.error_handling import java_handler


class GraphWiseConvLayerConfig:
    """GraphWise conv layer configuration."""

    _java_class = "oracle.pgx.config.mllib.GraphWiseConvLayerConfig"

    def __init__(self, java_config, params) -> None:
        self._config = java_config
        self.num_sampled_neighbors = java_handler(java_config.getNumSampledNeighbors, [])
        self.neighbor_weight_property_name = java_handler(
            java_config.getNeighborWeightPropertyName, []
        )
        self.activation_fn = java_handler(java_config.getActivationFunction, [])
        self.weight_init_scheme = java_handler(java_config.getWeightInitScheme, [])
        self.vertex_to_edge_connection = java_handler(java_config.getVertexToEdgeConnection, [])
        self.vertex_to_vertex_connection = java_handler(java_config.getVertexToVertexConnection, [])
        self.edge_to_vertex_connection = java_handler(java_config.getEdgeToVertexConnection, [])
        self.edge_to_edge_connection = java_handler(java_config.getEdgeToEdgeConnection, [])
        self.params = params

    def __repr__(self) -> str:
        attributes = []
        for param in self.params:
            if param != "self":
                attributes.append("%s: %s" % (param, self.params[param]))
        return "%s(%s)" % (self.__class__.__name__, ", ".join(attributes))

    def __str__(self) -> str:
        return repr(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._config.equals(other._config)
