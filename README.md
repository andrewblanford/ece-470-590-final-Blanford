# ece-470-590-final-Blanford

Video: https://youtu.be/STn7e4Z30rw

In the video, it looks like one leg is solved reasonably, but the other does some strange IK solution. 

To Run (in separate terminals):
* hubo-ach sim openhubo physics drc
* source ./channels.sh start
* python final_filter.py
* python ik_ctrl.py
* python final_ctrl.py
