# Instructions to install the DOCKER Repository.

####  This installation will configure the container to use correctly the nvidia drivers and install all the libraries used in this project

##  1. STEP ONE: Install nvidia drivers.
####    Open the *Show Aplications* window from your Ubuntu version and search the app *Software & Updates*.
####    Open the "Additional Drivers" window and select the next option:
    (Using NVIDIA driver metapackage from nvidia-driver-515 (proprietary))
####    After that you have to restart the computer.


##  2. STEP TWO: Install DOCKER.


```
sudo apt-get update
sudo apt-get install \
      ca-certificates \
      curl \
      gnupg \
      lsb-release
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg 
echo \ "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \ $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
sudo chgrp docker /lib/systemd/system/docker.socket
sudo chmod g+w /lib/systemd/system/docker.socket

sudo docker run hello-world
```

#### NOTES: The last command will print a hello-world container from docker, which shows you have already installed docker correctly. You can see this instrucions on their website: [Docker Install](https://docs.docker.com/engine/install/ubuntu/)

##  3. STEP THREE: Installation of nvidia docker2 drivers.



```
curl https://get.docker.com | sh \ && sudo systemctl --now enable docker

distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
sudo docker run --rm --runtime=nvidia --gpus all nvidia/cuda:11.6.2-base-ubuntu20.04 nvidia-smi
```
###  If you see the next table, the installation is complete:
![This is an image](https://github.com/DevasNAI/Electro-HorchatasPuzzleBot/blob/main/Docker/Screenshot%20from%202023-02-17%2013-18-16.png)

#### For the next part you will need a docker account, you can create it on the next page:
[Docker SignUp](https://hub.docker.com/signup)

#### Now login on your console
```
docker login
```

## 4. STEP FOUR: Download the dockerfile, makefile and nvidiaGPU.bash files from this folder:

####  Move the files to your desired folder and type the following commands:
####  Remember you have to be on the folder where you moved the downloaded files.

```
sudo apt install make
sudo make rosm.build

chmod +x nvidiaGPU.bash
sudo make rosm.nvidia
sudo make rosm.up
```

####  Note: Now you can open the shell inside the container with the next command:
```
sudo make rosm.shell
```

## Extra: To verify if the docker works correctly.

#### Open a terminal
```
sudo make rosm.shell

// This will open rviz.
rviz

// This will open gazebo.
gazebo

// This will open rqt_plot.
rqt_plot

// This will open rqt_graph.
rqt_graph

// This will open rqt.
rqt

sudo apt install mesa-utils
glxgears

// If the gears apppear in a window that means that the docker has access to your graphics card, if all is correct you can close the window. It takes a lot of time, don't worry this is normal.
```
#### Open other terminal
```
$  sudo apt install mesa-utils
$  glxgears
```

#### If everything works correctly, you have installed ros correctly, congrats :).







  
