import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('weather ETL').getOrCreate()

assert sys.version_info >= (3, 4) # make sure we have Python 3.4+
assert spark.version >= '2.1' # make sure we have Spark 2.1+

observation_schema = types.StructType([
    types.StructField('station', types.StringType(), False),
    types.StructField('date', types.StringType(), False),
    types.StructField('observation', types.StringType(), False),
    types.StructField('value', types.IntegerType(), False),
    types.StructField('mflag', types.StringType(), False),
    types.StructField('qflag', types.StringType(), False),
    types.StructField('sflag', types.StringType(), False),
    types.StructField('obstime', types.StringType(), False),
])


def main(in_directory, out_directory):
    weather = spark.read.csv(in_directory, schema=observation_schema)

    #weather.filter(weather.qflag.isNull()).collect()
    #weather.filter(weather.station.startswith('CA')).collect()

    weather = weather.filter(weather.qflag.isNull())
    weather = weather.filter(weather.station.startswith('CA'))
    weather = weather.filter(weather.observation.startswith('TMAX'))

    cleaned_data = weather.select(
        weather['station'],
        weather['date'],
        (weather['value'] / 10).alias('tmax')
    )

    #weather['value'] = weather['value'] / 10.0


    # TODO: finish here.

    #cleaned_data = weather

    cleaned_data.write.json(out_directory, compression='gzip', mode='overwrite')


if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
