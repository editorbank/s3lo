import argparse
import os
from s3api import S3Config


def get_args(prog, version) -> None:
  description = f"{prog} - Утилита загрузки и выгрузки файлов из S3 подобного хранилища. Версия {version}"
  s3c = S3Config()
  s3c.init_from_environments_variables()
  
  parser = argparse.ArgumentParser(add_help=False, prog=prog, description=description)
  msessages = parser.add_argument_group("Параметры отображения сообщений")
  msessages.add_argument("-h","--help", help = "Вывести это  собщение и завершить работу", action="help")
  msessages.add_argument("--silent", help = "Не отображать собщений результатов работы", action="store_true")

  s3storage = parser.add_argument_group("Параметры S3-хранилища", description = f"Все параметры в этом разделе можно установить через переменные окружения с префиксом \"{s3c.default_env_prefix}\", например параметр HOST устанавливается переменной окружения \"{s3c.default_env_prefix}HOST\".")
  # s3storage.add_argument("-e", dest="env_prefix", help = "Префикс для считывания параметров из переменных окружения (по умолчанию: \"%(default)s\")", default=s3c.default_env_prefix)
  s3storage.add_argument("--protocol", dest="protocol", help = "Протокол (http или https) для работы с S3-хранилищем (по умолчанию: \"%(default)s\")", default=s3c.protocol)
  s3storage.add_argument("--access_key", dest="access_key", help = "Ключ доступа", default=s3c.access_key, required=not s3c.access_key)
  s3storage.add_argument("--secret_key", dest="secret_key", help = "Сектретный ключ", default=s3c.secret_key, required=not s3c.secret_key)
  s3storage.add_argument("--host", help = "Имя хоста или IP-адрес", default=s3c.host, required=not s3c.host)
  s3storage.add_argument("--port", type=str, help = "Порт S3-хранилища (по умолчанию устанавливается в зависимости от протокола", default=s3c.port, required=False)
  s3storage.add_argument("--bucket", type=str, help = "Имя бакета", default=s3c.bucket, required=not s3c.bucket)

  other = parser.add_argument_group("Дополнительные параметры")
  other.add_argument("--save_empty_dir", action="store_true", help = "Хранить пустые директории", default=False)

  cmd:argparse._SubParsersAction[argparse.ArgumentParser] = parser.add_subparsers(title="Комманды", required=True, dest='command',
    description="""
    Для дополнительной справки по параметрам команд используйте опции \"-h\" или \"--help\" после команды.
    """)
  
  _="Список ключей в хранилище"
  ls:argparse.ArgumentParser=cmd.add_parser("list", help=_, description=_ )
  ls.add_argument("-k","--key_prefix", dest="key_prefix", help="Не обязательный префикс для отображения объектов хранилища",required=False)
  
  _="Отправка файла или директории в хранилище."
  up:argparse.ArgumentParser=cmd.add_parser("upload", help=_, description=_, epilog="""
    В качестве ключа используются имя в файловой системе. В конец имени диретори добавляется слэш, чтоб отличать её от файла.
    Примеры:
    1) опции "-f hello.txt" - загрузят файл "hello.txt" из рабочей директории в ключ хранилища с названием "hello.txt";
    2) опции "-f /tmp/hello.txt -с /tmp/" - загрузят файл "hello.txt" из директории "/tmp/" в ключ "hello.txt";
    3) опции "-f /tmp/hello.txt -с /tmp/ -a xxx/" - загрузят файл "hello.txt" из директории "/tmp/" в ключ "xxx/hello.txt";
    """)
  up.add_argument("-f","--file", help="Имя директории или файла для отравки в храничище (относительно рабочей директории)",required=True)
  up.add_argument("-a","--add_key_prefix", help="Не обязательный добовляемый к ключам префикс")
  up.add_argument("-c","--cut_file_path", help="Не обязательный вырезаемый из файлового пути префикс")
  
  _="Загрузка ключей из хранилища в файлы или директории"
  dn:argparse.ArgumentParser=cmd.add_parser("download", help=_, description=_ )
  dn.add_argument("-k","--key_prefix", help="Объект для загрузки из хранилища",required=True)
  dn.add_argument("-a","--add_file_path",help="Добавляемый путь в локальной файловой системе к имени ключа")
  dn.add_argument("-c","--cut_key_prefix", help="Вырезаемый из ключей префикс для формирования имени файла")
  
  _="Удаление ключей"
  rm:argparse.ArgumentParser=cmd.add_parser("delete", help=_, description=_ , )
  rm.add_argument("-k","--key_prefix", dest="key_prefix", help="Префикс для удаления объектов в хранилище",required=True)
  
  _="Чтение содержимого файла из хранилища"
  rd:argparse.ArgumentParser=cmd.add_parser("get", help=_, description=_ )
  rd.add_argument("-k","--key",help="Ключ в хранилище",required=True)
  
  _="Установка значения ключа в хранилище"
  wr:argparse.ArgumentParser=cmd.add_parser("set", help=_, description=_ )
  wr.add_argument("-k","--key",help="Ключ в хранилище",required=True)
  wr.add_argument("-v","--value",help="Новое значение ключа (по умолчанию пусто)")
  
  return parser.parse_args()


if __name__ == "__main__":
  args = get_args( version = "'0.0.1-test", prog = os.path.basename(__file__) )
  print(args.host)
