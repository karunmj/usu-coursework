"""Transitland Schedule API: create GeoJSON map of transit frequency."""
import json
import urllib
import urllib2
import datetime
import math
import os

##########################################################
##### Transitland Datastore Interface                #####
##########################################################

class Datastore(object):
  """A simple interface to the Transitland Datastore."""
  def __init__(self, host):
    self.host = host

  def _request(self, uri):
    print uri
    req = urllib2.Request(uri)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req)
    return json.loads(response.read())

  def request(self, endpoint, **data):
    """Request with JSON response."""
    return self._request(
      '%s%s?%s'%(self.host, endpoint, urllib.urlencode(data or {}))
    )

  def paginated(self, endpoint, key, **data):
    """Request with paginated JSON response. Returns generator."""
    response = self.request(endpoint, **data)
    while response:
      meta = response['meta']
      print '%s: %s -> %s'%(
        key,
        meta['offset'],
        meta['offset']+meta['per_page']
      )
      for entity in response[key]:
        yield entity
      if meta.get('next'):
        response = self._request(meta.get('next'))
      else:
        response = None

  def schedule_stop_pairs(self, **data):
    """Request Schedule Stop Pairs."""
    return self.paginated(
      '/api/v1/schedule_stop_pairs',
      'schedule_stop_pairs',
      **data
    )

  def stops(self, **data):
    """Request Stops"""
    return self.paginated(
      '/api/v1/stops',
      'stops',
      **data
    )

  def stop(self, onestop_id):
    """Request a Stop by Onestop ID."""
    return self.request('/api/v1/stops/%s'%onestop_id)

def duration(t1, t2):
  """Return the time between two HH:MM:SS times, in seconds."""
  fmt = '%H:%M:%S'
  t1 = datetime.datetime.strptime(t1, fmt)
  t2 = datetime.datetime.strptime(t2, fmt)
  return (t2 - t1).seconds

##########################################################
##### Count trips between stops, output GeoJSON      #####
##########################################################

HOST = 'http://transit.land'
PER_PAGE = 500
# BBOX = [
#   -122.554,
#   37.668,
#   -122.085,
#   37.912
# ]

# 41.4427
# -112.4890

# 42.3220
# -111.1047

BBOX = [
  -112.489,
  41.443,
  -111.105,
  42.322
]
DATE = '2016-10-20'
BETWEEN = [
  '07:00:00',
  '09:00:00'
]
HOURS = duration(BETWEEN[0], BETWEEN[1]) / 3600.0
# Minimum vehicles per hour
# http://colorbrewer2.org/
COLORMAP = {
  0: '#fef0d9',
  3: '#fdcc8a',
  6: '#fc8d59',
  10: '#d7301f'
}
OUTFILE = 'output.geojson'
if os.path.exists(OUTFILE):
  raise Exception("File exists: %s"%OUTFILE)

# Transitland Datastore API
ds = Datastore(HOST)

# Group SSPs by (origin, destination) and count
edges = {}
ssps = ds.schedule_stop_pairs(
  bbox=','.join(map(str, BBOX)),
  origin_departure_between=','.join(BETWEEN),
  date=DATE,
  per_page=PER_PAGE
)
for ssp in ssps:
  key = ssp['origin_onestop_id'], ssp['destination_onestop_id']
  if key not in edges:
    edges[key] = 0
  edges[key] += 1

# Get Stop geometries
stops = {}
for stop in ds.stops(per_page=PER_PAGE, bbox=','.join(map(str, BBOX))):
  stops[stop['onestop_id']] = stop

# Create GeoJSON Features
colorkeys = sorted(COLORMAP.keys())
features = []
edges_sorted = sorted(edges.items(), key=lambda x:x[1])
for (origin_onestop_id,destination_onestop_id),trips in edges_sorted:
  # Origin and destination geometries
  origin = stops.get(origin_onestop_id)
  destination = stops.get(destination_onestop_id)
  if not (origin and destination):
    # Outside bounding box
    continue
  # Frequency is in trips per hour
  frequency = trips / HOURS
  frequency_class = [i for i in colorkeys if frequency >= i][-1]
  print "Origin: %s Destination: %s Trips: %s Frequency: %s Freq. class: %s"%(
    origin_onestop_id,
    destination_onestop_id,
    trips,
    frequency,
    frequency_class
  )
  # Create the GeoJSON Feature
  features.append({
    "type": "Feature",
    "name": "%s -> %s"%(origin['name'], destination['name']),
    "properties": {
      "origin_onestop_id": origin_onestop_id,
      "destination_onestop_id": destination_onestop_id,
      "trips": trips,
      "frequency": frequency,
      "frequency_class": frequency_class,
      "stroke": COLORMAP[frequency_class],
      "stroke-width": frequency_class+1,
      "stroke-opacity": 1.0
    },
    "geometry": {
      "type": "LineString",
      "coordinates": [
        origin['geometry']['coordinates'],
        destination['geometry']['coordinates']
      ]
    }
  })

# Create the GeoJSON Feature Collection
fc = {
  "type": "FeatureCollection",
  "features": features
}
with open(OUTFILE, 'wb') as f:
  json.dump(fc, f)