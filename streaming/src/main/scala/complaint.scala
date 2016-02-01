import kafka.serializer.StringDecoder
import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka._
import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import org.apache.spark.SparkContext
import org.apache.spark.sql._

object PriceDataStreaming {
  def main(args: Array[String]) {

    val brokers = "52.71.164.204:9092"
    val topics = "complaint"
    val topicsSet = topics.split(",").toSet

    // Create context with 2 second batch interval
    val sparkConf = new SparkConf().setAppName("complaint_data")
//    val sqlContext = new SQLContext()
    val ssc = new StreamingContext(sparkConf, Seconds(2))

    // Create direct kafka stream with brokers and topics
    val kafkaParams = Map[String, String]("metadata.broker.list" -> brokers)
    val messages = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](ssc, kafkaParams, topicsSet)

    // Get the lines and show results
    messages.foreachRDD { rdd =>

        val sqlContext = SQLContextSingleton.getInstance(rdd.sparkContext)
        import sqlContext.implicits._

        val lines = rdd.map(_._2)
        val ticksDF = lines.map( x => {
                                  val tokens = x.split(";")
                                  Tick(tokens(0), tokens(2).toInt, tokens(3))}).toDF()
        // val ticks_per_source_DF = ticksDF.groupBy("source")
        //                         .agg("price" -> "avg", "volume" -> "sum")
        //                         .orderBy("source")

        val ticks_per_source_DF = ticksDF.groupBy("complaint").count().collect()//groupBy("source").agg("zipcode" -> "sum").orderBy("source")
        ticks_per_source_DF.collect()
        var ticks_with_time = ticks_per_source_DF.map(x => (x(0),current_time,x(1)))

        // rdd.sparkContext.parallelize(ticks_with_time).saveToCassandra("art_pin_log", "artwork_count", 
        //                     SomeColumns("art_id","event_time", "pin_count"),
        //                     writeConf = WriteConf(ttl = TTLOption.constant(30)))
    }

    // Start the computation
    ssc.start()
    ssc.awaitTermination()
  }
}

case class Tick(source: String, complaint: String, complaint_type: String)

/** Lazily instantiated singleton instance of SQLContext */
object SQLContextSingleton {

  @transient  private var instance: SQLContext = _

  def getInstance(sparkContext: SparkContext): SQLContext = {
    if (instance == null) {
      instance = new SQLContext(sparkContext)
    }
    instance
  }
}