
set -e

[ -f .venv/bin/activate ] && source .venv/bin/activate

if [ -f .env ] ; then
    echo "Read .env ..."
    IFS="="
    while read -r key value
    do
        echo $key="$value"
        export $key="$value"
    done < .env
    unset IFS
fi
project_name=$(cat pyproject.toml|grep -E "^[[][^]]+[]]|^\s*[a-z0-9]+\s*=\s*\"" | git config -f - project.name)  
call_app="python -m $project_name"
[ -f $project_name.pyz ] && call_app="python $project_name.pyz"
echo Call $call_app $* ...
$call_app $*
