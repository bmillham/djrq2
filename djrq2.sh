#! /bin/bash

function start ( )
{
    echo  "djrq2: starting service"
    # Edit this path to match the proper location
    cd /home/brian/djrq2-workingcopy/djrq2
    # Run in production mode: turns off debugging and starts fcgi
    ../bin/python -O -m web.app.djrq&
    echo $! > /tmp/djrq2.pid
     sleep  5
    echo  "PID is $(cat /tmp/djrq2.pid) "
}

function stop ( )
{
    echo  "djrq2: stopping Service (PID = $(cat /tmp/djrq2.pid))"
    kill $( cat  /tmp/djrq2.pid )
    rm  /tmp/djrq2.pid
 }

function status ( )
{
    ps  -ef  |  grep djrq2 |  grep  -v  grep
    echo  "PID indicate indication file $(cat /tmp/djrq2.pid 2>/dev/null) "
}

# Some Things That run always
touch  /var/lock/djrq2

# Management instructions of the service
case  "$1"  in
    start)
        start
        ;;
    stop)
        stop
        ;;
    reload)
        stop
        sleep  1
        start
        ;;
    status)
        status
        ;;
    * )
    echo  "Usage: $0 {start | stop | reload | status}"
    exit  1
    ;;
esac

exit  0
