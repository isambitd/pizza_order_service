## Cleaning Docker images
function clean_images {
    docker image prune --force
    docker image prune -a --force
    image_id=`docker images -q pizza_app_api`
    if [ ! -z "$image_id" ]
    then 
        docker rmi $image_id
    fi
}
function clean_containers {
    docker container prune --force
    stop_and_clean_movies_app_cont
}

function stop_and_clean_movies_app_cont {
    running_container_id=`docker ps -q --filter ancestor=pizza_app_api`
    if [ ! -z "$running_container_id" ]
    then 
        docker stop $running_container_id 
        docker rm $running_container_id
    fi
    container_id=`docker ps -aq --filter ancestor=pizza_app_api`
    if [ ! -z "$container_id" ]
    then 
        docker rm $container_id
    fi
}

function stop {
    docker-compose down
    clean_containers
    clean_images
}

stop

echo "Stopped the server and cleaned containers with images."

echo "Thank you :)"