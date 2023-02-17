#Indication to install the DOCKER Repository.

##This installation configure the container to use correctly the nvidia drivers and install all the ibraries that we could use to this project.

##1. STEP ONE: Install nvidia drivers.
  ###Open the "Show Applications" window from your Ubuntu version and search the app "Software & Updates".
  Open the "Additional Drivers" window and select the next option:
    (Using NVIDIA driver metapackage from nvidia-driver-515 (proprietary))
  After that you have to restart the computer.
  
 2. STEP TWO: Install DOCKER.
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
  $ sudo docker run hello-world
  
NOTES: The last command will showa hello-world container from docker,that would the prouf you already have installed docker correctly. You can see

3 nvidia docker 2
4 los archivos
5 los comandos
  
  
