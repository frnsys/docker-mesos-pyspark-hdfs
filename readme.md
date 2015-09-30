These scripts allow you to simulate a multi-node Mesos cluster for running Spark using Docker containers (except for Hadoop, which is currently configured only as a single node).

With a little modification of IP addresses this can easily be adapted to an actual multi-node deployment.

The basic arrangement is this:

- a Docker host machine, which also acts as the Spark _client_ (where Spark tasks are submitted from). This is what you are building images and running containers on.
- a Docker container running a Zookeeper process for coordinating Mesos leaders
- Docker container(s) running a Mesos master process to act as a leader
- Docker container(s) running a Mesos slave process to act as a follower
- a Docker container running Hadoop to host files with HDFS

Almost everything is handled via the `run` script.

Note that you can have multiple Zookeepers as well but the `run` script doesn't handle gathering those IPs properly yet.

### Client setup

If you don't have `docker` and `docker-compose`, run:

    ./run install_docker

This also pulls the `ubuntu:14.04` image which is used as the base for the other images.

The client also needs an installation of Mesos and Spark to properly submit jobs to the cluster.

These can be setup by running:

    ./run install_mesos
    ./run install_spark

### Building the images

Then you can build the Docker images:

    ./run build_images

This builds a base Mesos image, which is then used to build the leader and follower images. A Zookeeper image and a Hadoop image are also created.

### Running the containers

First, start a Zookeeper container:

    ./run zookeeper

Then start a Hadoop container:

    ./run hadoop

Then start a Mesos leader container:

    ./run leader

Finally, start a Mesos follower container:

    ./run follower

### Running the example

First, setup a text file to work with in the HDFS.

Open a shell in the Hadoop container:

    sudo docker exec -it hadoop bash

Download a text file:

    wget http://www.gutenberg.org/cache/epub/4300/pg4300.txt

Then copy it to the HDFS:

    hadoop fs -put pg4300.txt /sample.txt

Now it will be available to Spark and the example can be run from the client machine:

    ./run pyspark example.py

### Running any PySpark script

    ./run pyspark <my script>

Just note that any PySpark script needs to know the Zookeeper IP(s) and the Hadoop IP. If you use this `run pyspark` command to run your script, then the Zookeeper IP(s) and the Hadoop IP are passed in as first and second arguments, respectively, so they can be accessed like so:

    import sys
    leader_ip = sys.argv[1]
    hadoop_ip = sys.argv[2]

Refer to the `example.py` script.

### Other tools

The `run` script provides some other commands useful for development and testing:

- `ips` - list ips of docker containers
- `rmi` - remove all mesos-related images and dangling images
- `rmc` - stop and remove all mesos-related containers
- `nuke` - runs `rmc` and `rmi`
