rosm.build:
	@docker build -t ros/ros:electro-horchatas -f Dockerfile .
rosm.up:
	@xhost +
	@docker start electro-horchatas 
rosm.down:
	@xhost +
	@docker stop electro-horchatas 
rosm.restart:
	@xhost +
	@docker restart electro-horchatas 
rosm.shell:
	@xhost +	
	@docker exec -it electro-horchatas bash
rosm.nvidia:
	@./nvidiaGPU.bash