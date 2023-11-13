[ ! -f .whl/s3lo-1.0.0-py3-none-any.whl ] && sh make_whl.sh || true
[ ! -f .whl/s3lo-1.0.0-py3-none-any.whl ] && ( echo Error: not found .whl/s3lo-1.0.0-py3-none-any.whl ; exit 1 ) || true

[ -z VIRNUAL_ENV -a -d .venv ] && source .venv/bin/activate || true
echo Make pyz ...
pip install --no-index -f .whl -t pyz.tmp --upgrade .whl/s3lo-1.0.0-py3-none-any.whl

python -c "import zipapp" || pip install zipapps
find ./pyz.tmp  -name *.pyc -delete
find ./pyz.tmp  -name __pycache__ -delete
rm -rf ./pyz.tmp/bin
rm -f ./pyz.tmp/s3lo/direct_url.json
python -m zipapp pyz.tmp -o s3lo.pyz -m s3lo.__main__:main -p interpreter -c

