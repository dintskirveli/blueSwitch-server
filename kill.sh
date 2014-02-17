for i in $(ps aux | grep blueServ | grep -v grep | awk '{print $2}'); do sudo kill -9 $i; done;
