HUBO_IK_CHAN='hubo-ik-chan'
HUBO_CTRL_CHAN='hubo-ctrl-chan'


MakeAch()
{
	ach -1 -C $HUBO_IK_CHAN 	-m 10 -n 3000 
	ach -1 -C $HUBO_CTRL_CHAN     	-m 10 -n 3000 
}

KillAch()
{
	sudo rm /dev/shm/achshm-$HUBO_IK_CHAN  
	sudo rm /dev/shm/achshm-$HUBO_CTRL_CHAN  
}

Start()
{
	sudo chmod 777 "$1"
	KillAch
	MakeAch
}

Kill()
{
	KillAch
}


case "$1" in
	'start' )
		Start $2
	;;

	'kill' )
		Kill
	;;

esac
exit 0
