# Containers



1. Create a Docker image specification **Dockerfile** that runs the Playwrigt script `test_home.py` towards your locally deployed (without docker) backend and frontend.


1. Send a pull request with the Dockerfile and, if it apply, the additional files you had to create to make run the test_home.py script run inside of a docker container.


The commands to build and run the image locally should be just:

```
docker build . -t test_pw

docker run --rm [add to network] test_pw
```


Hints:

Useful documentation:  https://playwright.dev/python/docs/docker

Command to check local IP in windows:  `ipconfig`

export an environment variable `export APP_FRONT_URL=http://???`


# i build an own network so i dont colide with infra network for the oter labs. 

#  rm - take away container as soon you run the container 

# --network infrahannes_default name of the network infra folder wuth compose file 

# -e (export) env variabel and value is app-frontend beacuse service name is that in the compose file 

# test_pw the image to run the container from 


docker run --rm  --network infrahannes_default   -e APP_FRONT_URL=http://-app-frontend/   test_pw