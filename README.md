## Project  Directory Structure
```
.CARLA_0.9.9            
├── WindowsNoEditor
│   │   ├── CarlaUE4
│   │   ├── Co-Simulation
│   │   ├── Engine
│   │   ├── HDMaps
│   │   ├── PythonAPI
│   │   │   ├── carla
│   │   │   ├── util
│   │   │   ├── examples
│   │   │   │ 	├── object_detection
│   │   │   │ 	│   ├── tensorflow_yolov3    
│   │   │   │ 	│     	├── traffic_light.py
│   │   │   │ 	│   	├── yolov3_object_detection.py            
```

## Setup
	-> Carla
		python3 -m venv .venv_carla
		
		. ./.venv_carla/bin/activate
		
		# Dependencies
		
		pip install -U pip 
		
		./ImportAssets.sh
		
		pip install -r ~/CARLA_0.9.9.3/PythonAPI/examples/requirements.txt
		
		python -m pip install pygame
	
	-> Yolov3 (python3.7)
		
		(Intall python3.7)
		
		https://phoenixnap.com/kb/how-to-install-python-3-ubuntu
		
		python3.7 -m venv .venv
		
		. ./.venv/bin/activate
		
		pip install -U pip
		
		pip install -r requirements.txt
			
## Running
	
	-> Carla Server:
	
		cd Projects/Latitude/Carla/CARLA_0.9.9.3/

		. ./.venv_carla/bin/activate

		./CarlaUE4.sh -windowed -ResX=800 -ResY=600 -carla-server -fps=20 -quality-level=Low

	-> Spanwn:
	
		cd ~/Projects/Latitude/Carla
		
		. ./.venv/bin/activate
		
		cd ~/Projects/Latitude/Carla/CARLA_0.9.9.3/PythonAPI/examples
		
		python3 spawn_npc.py 

	-> Traffic Light

		cd ~/Projects/Latitude/Carla
		
		. ./.venv/bin/activate
		
		cd ~/Projects/Latitude/Carla/CARLA_0.9.9.3/PythonAPI/examples
		
		export CARLA_ROOT=~/CARLA_0.9.9.3/
		
		export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.9-py3.7-linux-x86_64.egg
		
		python3 yolov3_object_detection.py -wi 1920 -he 1080
 		

