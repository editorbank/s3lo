# Copyright 2012 Google Inc.
# Copyright (c) 2006,2007 Mitch Garnaat http://garnaat.org/
#

def versioned_bucket_lister(bucket, prefix='', delimiter='',
                            marker='', generation_marker='', headers=None):
    """
    A generator function for listing versioned objects.
    """
    more_results = True
    k = None
    while more_results:
        rs = bucket.get_all_versions(prefix=prefix, marker=marker,
                                     generation_marker=generation_marker,
                                     delimiter=delimiter, headers=headers,
                                     max_keys=999)
        for k in rs:
            yield k
        marker = rs.next_marker
        generation_marker = rs.next_generation_marker
        more_results= rs.is_truncated

class VersionedBucketListResultSet(object):
    """
    A resultset for listing versions within a bucket.  Uses the bucket_lister
    generator function and implements the iterator interface.  This
    transparently handles the results paging from GCS so even if you have
    many thousands of keys within the bucket you can iterate over all
    keys in a reasonably efficient manner.
    """

    def __init__(self, bucket=None, prefix='', delimiter='', marker='',
                 generation_marker='', headers=None):
        self.bucket = bucket
        self.prefix = prefix
        self.delimiter = delimiter
        self.marker = marker
        self.generation_marker = generation_marker
        self.headers = headers

    def __iter__(self):
        return versioned_bucket_lister(self.bucket, prefix=self.prefix,
                                       delimiter=self.delimiter,
                                       marker=self.marker,
                                       generation_marker=self.generation_marker,
                                       headers=self.headers)
