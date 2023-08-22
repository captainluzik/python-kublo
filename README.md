
# Python-kublo


### Resquirements:

    - docker
    - docker-compose

### Docker Engine installation:

#### Set up the repository 

#1. Update the ```apt``` package index and install packages to allow ```apt``` to use a repository over HTTPS:

```
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
```

#2 Add Docker's official GPG key:

```
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

#3 Use the following command to set up the repository:

```
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

#4 Update the ```apt``` package index:

```
sudo apt-get update
```


#### Install-docker-engine

#1 Install Docker Engine, containerd, and Docker Compose.

```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#2 Verify that the Docker Engine installation is successful by running the ```hello-world``` image.

```
sudo docker run hello-world
```


## Congratulations! You have just installed docker engine and docker-compose!


# Run docker containers

#1 cd to ```python-kublo``` directory  (```~/python-kublo$```)

#2 create ```.env``` file or just rename ```.env.example``` to ```.env```

#3 Run ```docker-compose.yaml``` file:

##3.1 With aborting containers building on tests failure:

```
sudo docker-compose up --build --abort-on-container-exit
```

##3.2 Without aborting containers building on tests failure:

```
sudo docker-compose up -d --build 
```

###4 Now, open your browser and go to ```http://0.0.0.0:80/swagger/```



# Congratulations! You have just successfully ran your containers!