[ -d .whl ] && exit 0
echo Make wheel ...
[ -z VIRNUAL_ENV -a -d .venv ] && source .venv/bin/activate || true
pip wheel -w .whl .
