[ ! -f "s3lo.pyz" ] && sh $(dirname $0)make_pyz.sh
#call %~dp0settings.cmd

echo Make exe v2 ...

[ ! -f "s3lo.pyz" ] && ( 1>&2 echo Error: No found "s3lo.pyz"! ; exit 1 )
rm -f s3lo.spec
rm -rf exe2.tmp
unzip "s3lo.pyz" -d exe2.tmp
[ -z VIRNUAL_ENV -a -d .venv ] && source .venv/bin/activate || true
pip install pyinstaller && pyinstaller exe2.tmp/__main__.py --contents-directory s3lo.files --name s3lo && (
  rm -f s3lo.spec
  rm -rf exe2.tmp
) && echo OK || ( 1>&2 echo FAIL & exit 1 )
