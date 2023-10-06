import sys,os
sys.path.append(os.path.dirname(__file__)) # use all modules from current dir
sys.path.extend([i.path for i in os.scandir('./.whl') if i.is_file() and i.name.endswith('.whl')]) # use all packages from dir './.whl'
print("\n".join(sys.path))

from s3lo.api import S3API,S3Config

conf = S3Config()
conf.init_from_environments_variables()
print(conf)
s3 = S3API(conf)
print(s3.keys_list())
