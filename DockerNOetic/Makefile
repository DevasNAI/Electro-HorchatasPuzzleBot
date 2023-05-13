rosm.build:
	@docker build -t ros/ros:electroNoetic -f Dockerfile .
rosm.up:
	@xhost +
	@docker start electroNoetic 
rosm.down:
	@xhost +
	@docker stop electroNoetic
rosm.restart:
	@xhost +
	@docker restart electroNoetic
rosm.shell:
	@xhost +	
	@docker exec -it electroNoetic bash
rosm.nvidia:
	@./nvidiaGPU.bash
