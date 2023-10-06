#!/usr/bin/env python
#-*- coding: utf-8 -*-
from api import S3API, S3Config
from ui import get_args

def main(prog,version):
  args = get_args(prog=prog,version=version)
  s3c = S3Config()
  s3c.init_from_other_object(args)
  s3 = S3API(s3c)
  s3.silent = args.silent
  s3.save_empty_dir = args.save_empty_dir

  if 'list'==args.command:
    line_format = "{last_modified!s} {size: >15} {name}"
    line_delimiter = "\n"
    print( line_delimiter.join([ line_format.format(**i) for i in s3.list(args.key_prefix) ]) )

  elif 'upload'==args.command:
    s3.upload(filename=args.file, add_key_prefix=args.add_key_prefix, cut_file_path=args.cut_file_path)

  elif 'download'==args.command:
    s3.download(key_prefix=args.key_prefix, add_file_path=args.add_file_path, cut_key_prefix=args.cut_key_prefix)

  elif 'delete'==args.command:
    s3.delete(key_prefix=args.key_prefix)

  elif 'get'==args.command:
    print(s3.get(filename=args.key))

  elif 'set'==args.command:
    s3.set(_key=args.key, value=args.value)

if __name__ == "__main__":  main()


