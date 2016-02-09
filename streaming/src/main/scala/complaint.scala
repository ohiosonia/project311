import kafka.serializer.StringDecoder
import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka._
import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import org.apache.spark.SparkContext
import org.apache.spark.sql._
import com.datastax.spark.connector._
import com.datastax.spark.connector.streaming._
import com.datastax.spark.connector.cql.{ColumnDef, RegularColumn, TableDef}
import com.datastax.spark.connector.types.IntType
import com.datastax.spark.connector.writer._
import org.apache.cassandra.serializers.TimestampSerializer
import java.util.Date
import org.joda.time.DateTime
import org.joda.time.format.DateTimeFormat
import java.sql.Timestamp

object PriceDataStreaming {
  def main(args: Array[String]) {

    val brokers = "52.71.164.204:9092"
    val topics = "complaints"
    val topicsSet = topics.split(",").toSet

    // Create context with 2 second batch interval
    val sparkConf = new SparkConf().setAppName("complaint_data")
    val ssc = new StreamingContext(sparkConf, Seconds(2))

    // Create direct kafka stream with brokers and topics
    val kafkaParams = Map[String, String]("metadata.broker.list" -> brokers)
    val messages = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](ssc, kafkaParams, topicsSet)

// Get the lines and show results

    messages.print

    messages.foreachRDD { rdd =>

        val sqlContext = SQLContextSingleton.getInstance(rdd.sparkContext)
        import sqlContext.implicits._

        val current_time = TimestampFormatter.format(new Date())
        val lines = rdd.map(_._2)
	println("lines.first =  "   +  lines.first)

	val sparkformat = new java.text.SimpleDateFormat("yyyyMMdd HHmmssZ") 
	val cassandraformat = new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss zzz")
	val ticksDF = lines.map( x => {
                                 val tokens = x.split(";")
				  //Tick(tokens(2).toInt,TimestampFormatter.format( DateTimeFormat.forPattern("yyyyMMdd'T'HHmmss").parseDateTime(tokens(1))))}).toDF()
				//Tick(tokens(2).toInt, tokens(1))}).toDF()
			val mydate = sparkformat.parse(tokens(1))
		Tick(tokens(2).toInt,mydate.getTime)}).toDF()
	//println("%s %s".format(ticksDF(0), ticksDF(1)))
	println("ticksDF  =   " + ticksDF)
	val ticks_per_source_DF = ticksDF.groupBy("zipcode").count().collect()
	var ticks_with_time = ticks_per_source_DF.map(x => (x(0),x(1)))

	//ticks_with_time.foreach(x=> println)

	rdd.sparkContext.parallelize(ticks_with_time).saveToCassandra("playground", "live_complaints2",
                            SomeColumns("zipcode","event_time"),
                            writeConf = WriteConf(ttl = TTLOption.constant(30)))
    }

    // Start the computation
    ssc.start()
    ssc.awaitTermination()
  }
}

case class Tick(zipcode: Int, event_time: Long)

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

object TimestampFormatter {

  private val TimestampPattern = "yyyy-MM-dd HH:mm:ss+0000"
   // def format(date: Date): String =
   // DateTimeFormat.forPattern(TimestampPattern).print(new DateTime(date))
 def format(date: Date): String =
    DateTimeFormat.forPattern(TimestampPattern).print(new DateTime(date.getTime))
}

