#
# Copyright (C) 2013 - 2022 Oracle and/or its affiliates. All rights reserved.
#

from jnius import autoclass
from pypgx._utils.error_handling import java_handler

_PgxResourcePermission = autoclass('oracle.pgx.common.auth.PgxResourcePermission')


class PgxResourcePermission:
    """Class representing a type of resource permission."""

    _java_class = 'oracle.pgx.common.auth.PgxResourcePermission'

    def __init__(self, java_resource_permission):
        self._resource_permission = java_resource_permission

    @staticmethod
    def get_strongest(a, b) -> "PgxResourcePermission":
        """Return the strongest permission of the two.

        :return: the strongest permission
        """
        permission = java_handler(_PgxResourcePermission.getStrongest,
                                  [a._resource_permission, b._resource_permission])
        return PgxResourcePermission(permission)

    def allows_inspect(self) -> bool:
        """Check if the resource can be inspected.

        :return: Boolean indicating if the resource can be inspected.
        """
        return java_handler(self._resource_permission.allowsInspect, [])

    def allows_read(self) -> bool:
        """Check if the resource can be read.

        :return: Boolean indicating if the resource can be read.
        """
        return java_handler(self._resource_permission.allowsRead, [])

    def allows_write(self) -> bool:
        """Check if the resource can be written.

        :return: Boolean indicating if the resource can be written.
        """
        return java_handler(self._resource_permission.allowsWrite, [])

    def allows_export(self) -> bool:
        """Check if the resource can be exported.

        :return: Boolean indicating if the resource can be exported.
        """
        return java_handler(self._resource_permission.allowsExport, [])

    def allows_manage(self) -> bool:
        """Check if the resource can be managed.

        :return: Boolean indicating if the resource can be managed.
        """
        return java_handler(self._resource_permission.allowsManage, [])

    def __str__(self) -> str:
        return java_handler(self._resource_permission.toString, [])

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._resource_permission.equals(other._resource_permission)

    def __hash__(self) -> int:
        return java_handler(self._resource_permission.hashCode, [])
