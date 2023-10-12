from colour import Color
from peewee import *
import simplekml

db = SqliteDatabase(None)

class Device(Model):
    first_time = TimestampField()
    last_time = TimestampField()
    devmac = TextField()
    min_lat = DoubleField()
    max_lat = DoubleField()
    min_lon = DoubleField()
    max_lon = DoubleField()
    avg_lat = DoubleField()
    avg_lon = DoubleField()
    strongest_signal = IntegerField()
    
    class Meta:
        database = db
        table_name = 'devices'
        primary_key = False

class Packet(Model):
    ts_sec = TimestampField()
    ts_usec = TimestampField()
    sourcemac = TextField()
    lat = DoubleField()
    lon = DoubleField()
    signal = IntegerField()
    
    class Meta:
        database = db
        table_name = 'packets'
        primary_key = False

class MainModel:
    def get_packets_from_db(self, input_db):
        db.init(input_db)
        db.connect()
        query = Packet.select().where((Packet.signal < 0) & (Packet.sourcemac != '00:00:00:00:00:00') & (Packet.lon != 0.0) & (Packet.lat != 0.0))
        db.close()
        return query
    
    def get_devices_from_db(self, input_db):
        db.init(input_db)
        db.connect()
        query = Device.select().where((Device.devmac != '00:00:00:00:00:00') & (Device.avg_lon != 0.0) & (Device.avg_lat != 0.0)).order_by(Device.devmac)
        db.close()
        return query
    
    def build_kml(self, packets, devices, heatworm):
        kml = simplekml.Kml()
        folders = dict()
        
        # prepare colour range
        num_of_colors = 11
        red = Color("red")
        white = Color("white")
        kml_red_color = simplekml.Color.hex(red.hex_l[1:])
        
        # Prepare a style for each color, this way points don't generate a new style for each (saves TONS of processing time and reduces KML size)
        if heatworm:
            colors = list(red.range_to(white, num_of_colors))
            styles = list()
            for color in colors:
                style = simplekml.Style()
                style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png'
                style.iconstyle.color = simplekml.Color.hex(color.hex_l[1:]) # convert to a KML hex color code (prepends alpha max opacity)
                styles.append(style)
            
            # Generate heatworm per device
            for packet in packets:
                if packet.sourcemac not in folders:
                    folders[packet.sourcemac] = kml.newfolder(name=packet.sourcemac)
                pnt = folders[packet.sourcemac].newpoint()
                pnt.coords = [(packet.lon, packet.lat)]
                color_index = int(abs(packet.signal) / num_of_colors)
                if color_index > 10:
                    color_index = 10
                pnt.style = styles[color_index]
            
        # Generate average location per device
        style = simplekml.Style()
        style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
        style.iconstyle.color = kml_red_color # convert to a KML hex color code (prepends alpha max opacity)
        
        for device in devices:
            if device.avg_lon == 0.0 and device.avg_lat == 0.0:
                continue
            if device.devmac not in folders:
                folders[device.devmac] = kml.newfolder(name=device.devmac)
            pnt = folders[device.devmac].newpoint()
            pnt.coords = [(device.avg_lon, device.avg_lat)]
            pnt.style = style
        
        return kml        