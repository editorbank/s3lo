# Copyright (c) 2014 Amazon.com, Inc. or its affiliates.
# All Rights Reserved
#
#
from boto.regioninfo import get_regions
from boto.regioninfo import connect


def regions():
    """
    Get all available regions for the CloudWatch Logs service.

    :rtype: list
    :return: A list of :class:`boto.regioninfo.RegionInfo`
    """
    from boto.logs.layer1 import CloudWatchLogsConnection
    return get_regions('logs', connection_cls=CloudWatchLogsConnection)


def connect_to_region(region_name, **kw_params):
    from boto.logs.layer1 import CloudWatchLogsConnection
    return connect('logs', region_name,
                   connection_cls=CloudWatchLogsConnection, **kw_params)
