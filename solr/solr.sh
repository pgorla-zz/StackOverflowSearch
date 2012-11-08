#!/bin/sh -e

# Starts, stops, and restarts solr


cd "$( dirname "$0" )"

SOLR_ROOT=`pwd`
SOLR_DIR="${SOLR_ROOT}/apache-solr-4.0-trunk/example"
JAVA_OPTIONS="-Xmx1024m -DSTOP.PORT=8079 -DSTOP.KEY=stopkey -jar start.jar"
SOLR_OPTIONS="-Dsolr.solr.home=${SOLR_ROOT}/cores/"
LOG_FILE="${SOLR_DIR}/../../solr.log"
JAVA="/usr/bin/java"

case $1 in
    run)
        echo "Running Solr"
        cd $SOLR_DIR
        $JAVA $SOLR_OPTIONS $JAVA_OPTIONS
        ;;
    start)
        echo "Starting Solr"
        cd $SOLR_DIR
        $JAVA $SOLR_OPTIONS $JAVA_OPTIONS 2> $LOG_FILE &
        ;;
    stop)
        echo "Stopping Solr"
        cd $SOLR_DIR
        $JAVA $JAVA_OPTIONS --stop
        ;;
    restart)
        $0 stop
        sleep 1
        $0 start
        ;;
    *)
        echo "Usage: $0 {run|start|stop|restart}" >&2
        exit 1
        ;;
esac

cd -
