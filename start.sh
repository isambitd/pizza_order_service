## Cleaning Docker images
function clean_images {
    docker image prune --force
    image_id=`docker images -q pizza_app_api`
    if [ ! -z "$image_id" ]
    then 
        docker rmi $image_id
    fi
}
function clean_containers {
    docker container prune --force
    stop_and_clean_pizza_app_cont
}

function stop_and_clean_pizza_app_cont {
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

function build_and_run {
    docker-compose run api python app/manage.py migrate --noinput
    docker-compose run api python app/manage.py test app -v 2
    docker-compose up -d --build
    
}

function clean_and_start {
    clean_containers
    clean_images
    build_and_run
}

function start {
    docker-compose down
    stop_and_clean_pizza_app_cont
    build_and_run
}

# clean_and_start
start

echo "You can view the apis at localhost:8000"

echo "Thank you :)"