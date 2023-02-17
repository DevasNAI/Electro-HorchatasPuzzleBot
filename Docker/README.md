# Indications to install the DOCKER Repository.

####  This installation configure the container to use correctly the nvidia drivers and install all the libraries that we could use to this project

##  1. STEP ONE: Install nvidia drivers.
####    Open the *Show Aplications* window from your Ubuntu version and search the app *Software & Updates*.
####    Open the "Additional Drivers" window and select the next option:
    (Using NVIDIA driver metapackage from nvidia-driver-515 (proprietary))
####    After that you have to restar the computer.


##  2. STEP TWO: Install DOCKER.


```
$ sudo apt-get update
$ sudo apt-get install \
      ca-certificates \
      curl \
      gnupg \
      lsb-release
$ sudo mkdir -m 0755 -p /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg 
  $ echo \ "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \ $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
 
$ sudo apt-get update
$ sudo chmod a+r /etc/apt/keyrings/docker.gpg
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
$ newgrp docker
$ sudo chgrp docker /lib/systemd/system/docker.socket
$ sudo chmod g+w /lib/systemd/system/docker.socket
$ sudo docker run hello-world
```

#### NOTES: The last command will show a hello-world container from docker, that would the prouf you already have installed docker correctly. You can see this instrucions on there website: [Docker Install](https://docs.docker.com/engine/install/ubuntu/)

##  3. STEP THREE: Installation nvidia docker2 drivers.



```
$  curl https://get.docker.com | sh \ && sudo systemctl --now enable docker
$  distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
$  distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/experimental/$distribution/libnvidia-container.list | \
         sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
         sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
$  sudo apt-get update
$  sudo apt-get install -y nvidia-container-toolkit
$  sudo nvidia-ctk runtime configure --runtime=docker
$  sudo systemctl restart docker
$  sudo docker run --rm --runtime=nvidia --gpus all nvidia/cuda:11.6.2-base-ubuntu20.04 nvidia-smi
```
###  If you see the next table, the installation is right:
![This is an image](https://github.com/DevasNAI/Electro-HorchatasPuzzleBot/blob/main/Docker/Screenshot%20from%202023-02-17%2013-18-16.png)

#### You need a docker account, you can do it on the next page:
[Docker SignUp](https://hub.docker.com/signup)

#### Now login on your console
```
$ docker login
```

## 4. STEP FOUR: Download the docker achieves from this folder:

####  Open in a terminal the location of the files.
####  Now you are gonna introduce the next commands:

```
$  sudo apt install make
$  sudo make rosm.build
$  ls
$  chmod +x nvidiaGPU.bash
$  sudo make rosm.nvidia
$  sudo make rosm.up
```

####  Note: Now you can open the ros terminal with the next command:
```
$  sudo make rosm.shell
```
####  Remember you have to be on the folder with the downloaded files.

## Extra: Now we are gonna look all are fine.

#### Open other terminal
```
$  sudo make rosm.shell
$  rviz
// This show the rviz simulator, open it in big window, if all is right close it and continue.
$  gazibo
// This show the gazibo simulator, open it in big window, if all is right close it and continue.
$  rqt_plot
// This show the plot simulator, open it in big window, if all is right close it and continue.
$  rqt_graph
// This show the graph simulator, open it in big window, if all is right close it and continue.
$  rqt
// This show the rqt simulator, open it in big window, if all is right close it and continue.
$  sudo apt install mesa-utils
$  glxgears
// This show the proof that the docker recognize your grafic card, if all is correct you can close the window. If it takes a lot of time, don't worry this is normal.
```
#### Open other terminal
```
$  sudo apt install mesa-utils
$  glxgears
// This show the proof that the docker recognize your grafic card, if all is correct you can close the window. If it takes a lot of time, don't worry this is normal.
```

#### If you have all of this correct, now you can work, good luck







  
