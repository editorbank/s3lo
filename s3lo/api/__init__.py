#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pathlib import Path
from urllib.parse import quote_plus

import boto
import boto.s3.connection

__version__ = 1.0


class S3Config:
    default_env_prefix = "S3_"
    prams_list = ("protocol", "access_key", "secret_key", "host", "port", "bucket")

    def __init__(self) -> None:
        self.protocol = "https"
        self.access_key = ""
        self.secret_key = ""
        self.host = ""
        self.port = ""
        self.bucket = ""

    def init_from_environments_variables(self, prefix: str = ""):
        if not prefix:
            prefix = self.default_env_prefix
        for name in self.prams_list:
            env_name = (prefix + name).upper()
            env_value = os.environ.get(env_name, None)
            if env_value:
                self.__setattr__(name, env_value)

    def init_from_other_object(self, obj: object):
        if not obj:
            return
        for name in self.prams_list:
            value = obj.__getattribute__(name)
            if value:
                self.__setattr__(name, value)

    def __str__(self) -> str:
        ret = ""
        if self.access_key:
            ret = ret + quote_plus(self.access_key)
        if self.secret_key:
            ret = ret + ":" + quote_plus(self.secret_key)
        if ret:
            ret = ret + "@"
        ret = ("https" if self.protocol == "https" else "http") + "://" + ret
        if self.host:
            ret = ret + self.host
        if self.port.isdigit():
            ret = ret + ":" + self.port
        if self.bucket:
            ret = ret + "/" + self.bucket
        return ret
        # return f'{quote_plus(self.access_key)}:{quote_plus(self.secret_key)}@{self.host}/{self.bucket}'


def _cut_prefix(name, prefix):
    return name[len(prefix) :] if name.startswith(prefix) else name


class S3API:
    def __init__(self, config: S3Config) -> None:
        is_secure = True if config.protocol == "https" else False
        port = int(config.port) if config.port.isdigit() else 443 if is_secure else 80
        self.conn = boto.connect_s3(
            aws_access_key_id=config.access_key,
            aws_secret_access_key=config.secret_key,
            host=config.host,
            port=port,
            is_secure=is_secure,  # using ssl
            validate_certs=False,
            calling_format=boto.s3.connection.OrdinaryCallingFormat(),
        )
        self.bucket = self.conn.get_bucket(config.bucket)
        self._cat_encoding = "utf-8"
        self._expired_thous_secconds = 36000
        self.silent = True
        self.save_empty_dir = False

    def list(self, *args, **kwargs):
        return [key.__dict__ for key in self.bucket.list(*args, **kwargs)]

    def keys_list(self, *args, **kwargs):
        return [i["name"] for i in self.list(*args, **kwargs)]

    def delete(self, key_prefix):
        for _key in self.keys_list(prefix=key_prefix):
            if not self.silent:
                print(f' Delete key "{_key}" ...')
            self.bucket.delete_key(_key)

    def set(self, key: str, value: str = ""):
        _key_object = self.bucket.new_key(key)
        _key_object.set_contents_from_string(value)

    def url(self, key):
        _key_object = self.bucket.get_key(key)
        return _key_object.generate_url(self._expired_thous_secconds)

    def exists(self, key) -> bool:
        _key_object = self.bucket.get_key(key)
        return True if _key_object and _key_object.exists() else False

    def as_dir(self, name: str = "") -> str:
        if not name:
            name = ""
        if name != "" and not name.endswith("/"):
            name = name + "/"
        return name

    def is_dir(self, name: str = "") -> bool:
        if not name:
            name = ""
        return name in ("", ".", "..") or name.endswith("/")

    def download(self, key_prefix, add_file_path: str = "", cut_key_prefix: str = ""):
        if not add_file_path:
            add_file_path = ""
        if not cut_key_prefix:
            cut_key_prefix = ""
        for _key in self.keys_list(prefix=key_prefix):
            _filename = add_file_path + _cut_prefix(_key, cut_key_prefix)
            if not self.is_dir(_key):
                if not self.silent:
                    print(f' Download key "{_key}" to "{_filename}" ...')
                Path(_filename).parent.mkdir(parents=True, exist_ok=True)
                self.bucket.get_key(_key).get_contents_to_filename(_filename)
            else:
                if self.save_empty_dir:
                    if not self.silent:
                        print(f' Download key "{_key}" as empty dir "{_filename}" ...')
                    Path(_filename).mkdir(parents=True, exist_ok=True)

    def get(self, filename, default=""):
        key = self.bucket.get_key(filename)
        return (
            key.get_contents_as_string().decode(encoding=self._cat_encoding)
            if key
            else default
        )

    def fs_list(self, root_dir: str = ""):
        ret = []
        if self.is_dir(root_dir):
            root_dir = self.as_dir(root_dir)
        while root_dir.startswith("./"):
            root_dir = root_dir[2:]
        while root_dir.endswith("/./"):
            root_dir = root_dir[:-2]
        if root_dir == "./":
            root_dir = ""
        if not self.is_dir(root_dir):
            ret.append(root_dir)
        else:
            for path in os.scandir(root_dir if root_dir != "" else "."):
                if path.is_file():
                    file_name = self.as_dir(root_dir) + path.name
                    ret.append(file_name)
                if path.is_dir():
                    dir_name = self.as_dir(self.as_dir(root_dir) + path.name)
                    # print(dir_name)
                    ret.extend(self.fs_list(dir_name))
        return ret

    def upload(self, filename, add_key_prefix: str = "", cut_file_path: str = ""):
        if not add_key_prefix:
            add_key_prefix = ""
        if not cut_file_path:
            cut_file_path = ""
        for i in self.fs_list(filename):
            _key = add_key_prefix + _cut_prefix(i, cut_file_path)
            if not self.is_dir(i):
                if not self.silent:
                    print(f'Upload key "{_key}" from "{i}" ...')
                self.bucket.new_key(_key).set_contents_from_filename(i)
            else:
                if self.save_empty_dir:
                    if not self.silent:
                        print(f'Upload key "{_key}" as empty ...')
                    self.set(_key)


# if __name__ == "__main__":
#   s3c = S3Config()
#   s3c.init_from_environments_variables()
#   s3 = S3API(s3c)
#   s3.silent = False
#   for k in s3.keys_list(): print(k)
