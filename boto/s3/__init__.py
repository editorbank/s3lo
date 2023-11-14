# Copyright (c) 2006-2012 Mitch Garnaat http://garnaat.org/
# Copyright (c) 2010, Eucalyptus Systems, Inc.
# Copyright (c) 2014, Steven Richards <sbrichards@mit.edu>
# All rights reserved.
#
#

from boto.regioninfo import RegionInfo, get_regions
from boto.regioninfo import connect


class S3RegionInfo(RegionInfo):

    def connect(self, **kw_params):
        """
        Connect to this Region's endpoint. Returns an connection
        object pointing to the endpoint associated with this region.
        You may pass any of the arguments accepted by the connection
        class's constructor as keyword arguments and they will be
        passed along to the connection object.

        :rtype: Connection object
        :return: The connection to this regions endpoint
        """
        if self.connection_cls:
            return self.connection_cls(host=self.endpoint, **kw_params)


def regions():
    """
    Get all available regions for the Amazon S3 service.

    :rtype: list
    :return: A list of :class:`boto.regioninfo.RegionInfo`
    """
    from boto.s3.connection import S3Connection
    return get_regions(
        's3',
        region_cls=S3RegionInfo,
        connection_cls=S3Connection
    )


def connect_to_region(region_name, **kw_params):
    from boto.s3.connection import S3Connection
    if 'host' in kw_params:
        host = kw_params.pop('host')
        if host not in ['', None]:
            region = S3RegionInfo(
                name='custom',
                endpoint=host,
                connection_cls=S3Connection
            )
            return region.connect(**kw_params)

    return connect('s3', region_name, region_cls=S3RegionInfo,
                   connection_cls=S3Connection, **kw_params)
