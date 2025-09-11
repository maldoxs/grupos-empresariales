#
# Copyright (C) 2013 - 2022 Oracle and/or its affiliates. All rights reserved.
#

from typing import Any, List, Mapping, Optional, Union, Collection

from jnius import autoclass

from pypgx._utils.error_handling import java_handler
from pypgx._utils.error_messages import INVALID_OPTION
from pypgx._utils import conversion
from pypgx._utils.pgx_types import (
    aggregates,
    graph_property_config_fields,
    property_types,
    string_pooling_strategies,
    graph_property_config
)


class GraphPropertyConfig:
    """A class for representing graph property configurations."""

    _java_class = 'oracle.pgx.config.GraphPropertyConfig'

    def __init__(self, name: str, property_type: str,
                 dimension: Optional[int] = None, formats: Optional[List[str]] = None,
                 default: Optional[Any] = None, column: Optional[Union[int, str]] = None,
                 stores: Optional[List[Mapping[str, str]]] = None,
                 max_distinct_strings_per_pool: Optional[int] = None,
                 string_pooling_strategy: Optional[str] = None, aggregate: Optional[str] = None,
                 field: Optional[str] = None, group_key: Optional[str] = None,
                 drop_after_loading: Optional[bool] = None) -> None:

        config_builder = autoclass('oracle.pgx.config.GraphPropertyConfigBuilder')()
        java_handler(config_builder.setName, [name])
        if property_type not in property_types:
            raise ValueError(INVALID_OPTION.format(var='type', opts=list(property_types)))
        java_type = property_types[property_type]
        java_handler(config_builder.setType, [java_type])

        if dimension is not None:
            java_handler(config_builder.setDimension, [dimension])
        if formats is not None:
            java_handler(config_builder.setFormat, [*formats])
        if default is not None:
            java_default = conversion.property_to_java(default, property_type)
            java_handler(config_builder.setDefault, [java_default])
        if column is not None:
            java_handler(config_builder.setColumn, [column])
        if stores is not None:
            java_handler(
                config_builder.setStores,
                [conversion.to_java_map(s) for s in stores]
            )
        if max_distinct_strings_per_pool is not None:
            java_handler(config_builder.setMaxDistinctStringsPerPool,
                         [max_distinct_strings_per_pool])
        if string_pooling_strategy is not None:
            if string_pooling_strategy in string_pooling_strategies:
                java_string_pooling_strategy = string_pooling_strategies[string_pooling_strategy]
            else:
                raise ValueError(
                    INVALID_OPTION.format(
                        var='string_pooling_strategy',
                        opts=list(string_pooling_strategies)
                    )
                )
            java_handler(config_builder.setStringPoolingStrategy, [java_string_pooling_strategy])
        if aggregate is not None:
            if aggregate in aggregates:
                java_aggregate = aggregates[aggregate]
            else:
                raise ValueError(
                    INVALID_OPTION.format(
                        var='aggregate',
                        opts=list(aggregates)
                    )
                )
            java_handler(config_builder.setAggregate, [java_aggregate])
        if field is not None:
            java_handler(config_builder.setField, [field])
        if group_key is not None:
            java_handler(config_builder.setGroupKey, [group_key])
        if drop_after_loading is not None:
            java_handler(config_builder.setDropAfterLoading, [drop_after_loading])

        self._graph_property_config = java_handler(config_builder.build, [])

    @classmethod
    def _from_java_config(cls, java_config: graph_property_config) -> "GraphPropertyConfig":
        """Instantiate GraphPropertyConfig from java instance

        :return: GraphPropertyConfig wrapping the java instance
        """
        self = cls.__new__(cls)
        self._graph_property_config = java_config
        return self

    @staticmethod
    def get_config_fields() -> Collection[str]:
        """Return the config fields

        :return: list of config fields
        """
        return graph_property_config_fields.keys()

    def is_empty(self) -> bool:
        """Check if it's empty.

        :return: True, if the Map 'values' is empty.
        """
        return java_handler(self._graph_property_config.isEmpty, [])

    def has_default_value(self, field: str) -> bool:
        """Check if field has a default value.

        :param field: the field
        :return: True, if value for given field is the default value
        """
        if field in graph_property_config_fields:
            java_field = graph_property_config_fields[field]
        else:
            raise ValueError(
                INVALID_OPTION.format(var='type', opts=list(graph_property_config_fields))
            )
        return java_handler(self._graph_property_config.hasDefaultValue, [java_field])

    def get_name(self) -> str:
        """Get name of property

        :return: name of property
        """
        return java_handler(self._graph_property_config.getName, [])

    def get_dimension(self) -> int:
        """Get dimension of property

        :return: dimension of property
        """
        return java_handler(self._graph_property_config.getDimension, [])

    def get_format(self) -> List[str]:
        """Get list of formats of property

        :return: list of formats of property
        """
        java_list = java_handler(self._graph_property_config.getFormat, [])
        return conversion.collection_to_python_list(java_list)

    def get_type(self) -> str:
        """Get type of property

        :return: type of property
        """
        java_property_type = java_handler(self._graph_property_config.getType, [])
        if java_property_type is None:
            property_type = None
        else:
            property_type = next(k for k, v in property_types.items() if v == java_property_type)
        return property_type

    def get_default(self) -> Any:
        """Get default value to be assigned to this property if datasource does not provide it.
        In case of date type: string is expected to be formatted with yyyy-MM-dd HH:mm:ss.
        If no default is present, non-existent properties will contain default Java types
        (primitives) or empty string or 01.01.1970 00:00.

        :return: default of property
        """
        java_default = java_handler(self._graph_property_config.getDefault, [])
        default = conversion.anything_to_python(java_default)
        return default

    def get_column(self) -> Optional[Union[int, str]]:
        """Get name or index (starting from 1) of the column holding the property data.
        If it is not specified, the loader will try to use the property name as column name
        (for CSV format only)

        :return: column of property
        """
        java_column = java_handler(self._graph_property_config.getColumn, [])
        column = conversion.anything_to_python(java_column)
        return column

    def get_stores(self) -> List[Mapping[str, str]]:
        """Get list of storage identifiers that indicate where this property resides.

        :return: list of storage identifiers
        """
        java_map = java_handler(self._graph_property_config.getStores, [])
        stores = conversion.collection_to_python_list(java_map)
        return stores

    def get_max_distinct_strings_per_pool(self) -> Optional[int]:
        """Get amount of distinct strings per property after which to stop pooling.
        If the limit is reached an exception is thrown. If set to null, the default
        value from the global PGX configuration will be used.

        :return: amount of distinct strings per property after which to stop pooling
        """
        return java_handler(self._graph_property_config.getMaxDistinctStringsPerPool, [])

    def get_string_pooling_strategy(self) -> Optional[str]:
        """Get which string pooling strategy to use. If set to null, the default value from
        the global PGX configuration will be used.

        :return: string pooling strategy to use
        """
        java_strategy = java_handler(self._graph_property_config.getStringPoolingStrategy, [])
        if java_strategy is None:
            strategy = None
        else:
            strategy = next(k for k, v in string_pooling_strategies.items() if v == java_strategy)
        return strategy

    def get_aggregate(self) -> Optional[str]:
        """Which aggregation function to use, aggregation always happens by vertex key

        :return: aggregation function to use
        """
        java_aggregate = java_handler(self._graph_property_config.getAggregate, [])
        if java_aggregate is None:
            aggregate = None
        else:
            aggregate = next(k for k, v in aggregates.items() if v == java_aggregate)
        return aggregate

    def get_field(self) -> Optional[str]:
        """Get name of the JSON field holding the property data.
        Nesting is denoted by dot - separation. Field names containing dots are possible, in this
        case the dots need to be escaped using backslashes to resolve ambiguities. Only the exactly
        specified object are loaded, if they are non existent, the default value is used

        :return: name of the JSON field
        """
        return java_handler(self._graph_property_config.getField, [])

    def get_group_key(self) -> Optional[str]:
        """Can only be used if the property / key is part of the grouping expression

        :return: group key
        """
        return java_handler(self._graph_property_config.getGroupKey, [])

    def is_drop_after_loading(self) -> bool:
        """Whether helper properties are only used for aggregation, which are dropped after
        loading

        :return: True, if helper properties are dropped after loading
        """
        return bool(java_handler(self._graph_property_config.isDropAfterLoading, []))

    def get_parsed_default_value(self) -> Any:
        """Get the parsed default value guaranteed to match the property type (with the exception
        of type node/edge). In case a default is not specified, the *default* default value is
        returned.

        :return: the parsed default value
        """
        java_default = java_handler(self._graph_property_config.getParsedDefaultValue, [])
        return conversion.anything_to_python(java_default)

    def get_source_column(self) -> Optional[Union[int, str]]:
        """Return column if indicated, otherwise return the property name

        :return: the source column
        """
        java_source_column = java_handler(self._graph_property_config.getSourceColumn, [])
        source_column = conversion.anything_to_python(java_source_column)
        return source_column

    @staticmethod
    def get_value_from_environment(key: str) -> Optional[str]:
        """Look up a value by a key from java properties and the system environment.
        Looks up the provided key first in the java system properties prefixed with
        SYSTEM_PROPERTY_PREFIX and returns the value if present.
        If it is not present, looks it up in the system environment prefixed with
        ENV_VARIABLE_PREFIX and returns this one if present.
        Returns None if the key is neither found in the properties nor in the environment.

        :param key: the key to look up
        :return: the found value or None if the key is not available
        """
        return java_handler(autoclass(GraphPropertyConfig._java_class).getValueFromEnvironment,
                            [key])

    def is_external(self) -> bool:
        """Whether the property is external

        :return: True if the property is external, False otherwise
        """
        return java_handler(self._graph_property_config.isExternal, [])

    def is_in_memory(self) -> bool:
        """Whether the property is in memory

        :return: True if the property is in memory, False otherwise
        """
        return java_handler(self._graph_property_config.isInMemory, [])

    def is_string_pool_enabled(self) -> bool:
        """Whether the string pool is enabled

        :return: True if the the string pool is enabled, False otherwise
        """
        return java_handler(self._graph_property_config.isStringPoolEnabled, [])

    def set_serializable(self, serializable: bool) -> None:
        """Set this config to be serializable

        :param serializable: True if serializable, False otherwise
        :return:
        """
        java_handler(self._graph_property_config.setSerializable, [serializable])

    def __repr__(self) -> str:
        return str(self._graph_property_config.toString())

    def __str__(self) -> str:
        return repr(self)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._graph_property_config.equals(other._graph_property_config)
