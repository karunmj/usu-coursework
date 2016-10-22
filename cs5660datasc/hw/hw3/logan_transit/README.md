# Transitland Frequency Visualization

Accompanies blog post: [Transit dimensions: Transitland Schedule API](http://mapzen.com/blog/the-transit-dimension-transit-land-schedule-api)

The frequency.py script:
 * Fetches all trips on a given date, between a start time and end time, inside of a bounding box
 * Calculates the number of connections between every stop
 * Uses a colormap and line width to show more frequent service
 * Outputs a GeoJSON map as output.geojson

An [example GeoJSON output](https://gist.github.com/irees/f9a4d9d27e202309e9de)

The script defines all the query parameters as constants; feel free to use it as a jumping off point. The example interface is an excerpt from a more fully featured client library in the works.

Please check out the [Transitland Datastore Github Repository](https://github.com/transitland/transitland-datastore) for the full [schedule API documentation](https://github.com/transitland/transitland-datastore/blob/master/doc/schedule_api.md).

Note that your results may vary slightly from the image used in the blog post.