BASEDIR=$(dirname "$0")
COMMAND=$1
NUM_OF_TEMP_TABLES=$2

help() {
    echo "Usage: init-db COMMAND [ARGS]"
    echo "COMMAND:"
    echo "  drop, d    -   drop the entire db"
    echo "  create, c  -   create db and schema if exists"
    echo "                 ARGS: number of temp tables (should be equal to number of instances) "
    echo "  help, h    -   output this help"
}
drop() {
    sudo -u postgres psql -f $BASEDIR/drop-db.sql
}
create() {
    sudo -u postgres psql -f $BASEDIR/create-db.sql
    sudo -u postgres psql -d terminal -f $BASEDIR/create-schema.sql
    create_temp_schema
}
create_temp_schema() {
    CREATE_SCHEMA_TEMP_SQL=$BASEDIR/create-temp-schema.sql
    TEMP__CREATE_TEMP_SCHEMA_SQL=$BASEDIR/_create-temp-schema.sql

    for i in `seq 0 $((NUM_OF_TEMP_TABLES - 1))`
    do
        cp $CREATE_SCHEMA_TEMP_SQL $TEMP__CREATE_TEMP_SCHEMA_SQL
        sed -i "s/_ID/_$i/g" $TEMP__CREATE_TEMP_SCHEMA_SQL
        sudo -u postgres psql -d terminal -f $TEMP__CREATE_TEMP_SCHEMA_SQL
        rm $TEMP__CREATE_TEMP_SCHEMA_SQL
    done
}


case $COMMAND in
    "h"|"help") help;;
    "d"|"drop") drop;;
    "c"|"create") create;;
    *) help;;
esac
