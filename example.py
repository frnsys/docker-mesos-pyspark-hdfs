import sys
import pyspark

leader_ip = sys.argv[1]
hadoop_ip = sys.argv[2]

src = 'hdfs://{}:8020/sample.txt'.format(hadoop_ip)
conf = pyspark.SparkConf()
conf.setMaster('mesos://zk://{}:2181/mesos'.format(leader_ip))
conf.setAppName('my_test_app')

# this must be a _prebuilt_ spark archive, i.e. a spark binary package
# you can build it and host it yourself if you like.
conf.set('spark.executor.uri', 'http://d3kbcqa49mib13.cloudfront.net/spark-1.5.0-bin-hadoop2.6.tgz')

sc = pyspark.SparkContext(conf=conf)

lines = sc.textFile(src)
words = lines.flatMap(lambda x: x.split(' '))
word_count = (words.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x+y))
print(word_count.collect())
