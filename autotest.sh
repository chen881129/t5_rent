#! /usr/bin/env bash

function wait_port()
{
    port=$1
    pid=$2
    while [[ 0 ]]
    do
        ps -p $pid
        if [[ $? -ne 0 ]];then
            return 1
        fi
        listen=`netstat -nalp | grep "\<$port\>"`
        if [[ $? -eq 0 ]];then
            return 0
        fi
    done
}

echo "start main server"
sudo python main.py 1010 &>test_log &
PID=$!
wait_port 1010 $PID
if [[ $? -ne 0 ]];then
    echo "start server failed"
    exit 1
fi

kill $PID
