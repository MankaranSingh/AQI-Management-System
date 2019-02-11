from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import aqi
import pandas as pd



SECRET_KEY = 'Radiant32'

app = Flask(__name__)

df = pd.read_csv('Dummy_AQI.txt', names = ['timestamp','lat','lon','state','city','area','AQI','humidity', 'temp', 'CO','NO2','O3','PM10','PM25','SO2'])


base_dir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

class AQIData(db.Model):

    __tablename__ = 'aqi_data'
    
    id = db.Column(db.Integer, primary_key=True)
    
    lat = db.Column(db.Float, unique=False, nullable=True)
    lon = db.Column(db.Float, unique=False, nullable=True)
    state = db.Column(db.String(120), unique=False, nullable=True)
    city = db.Column(db.String(120), unique=False, nullable=True)
    area = db.Column(db.String(80), unique=False, nullable=True)
    aqi = db.Column(db.Float, unique=False, nullable=True)
    humidity = db.Column(db.Float, unique=False, nullable=True)
    temperature = db.Column(db.Float, unique=False, nullable=True)
    CO = db.Column(db.Float, unique=False, nullable=True)
    NO2 = db.Column(db.Float, unique=False, nullable=True)
    O3 = db.Column(db.Float, unique=False, nullable=True)
    PM10 = db.Column(db.Float, unique=False, nullable=True)
    PM25 = db.Column(db.Float, unique=False, nullable=True)
    SO2 = db.Column(db.Float, unique=False, nullable=True)

@app.route('/<raw_str>/<secret>', methods = ['GET','POST'])
def update_table(raw_str,secret):

    if SECRET_KEY == secret:
        
        lat,lon,state,city,area,AQI,humidity,temp = raw_str.split('-')
        CO = aqi.to_cc(aqi.POLLUTANT_CO_8H, float(AQI))
        NO2 = aqi.to_cc(aqi.POLLUTANT_NO2_1H, float(AQI))
        O3 = aqi.to_cc(aqi.POLLUTANT_O3_1H, float(AQI))
        PM10 = aqi.to_cc(aqi.POLLUTANT_PM10, float(AQI))
        PM25 = aqi.to_cc(aqi.POLLUTANT_PM25, float(AQI))
        SO2 = aqi.to_cc(aqi.POLLUTANT_SO2_1H, float(AQI))
        
        row = AQIData(lat = lat,lon=lon, state=state,city=city,area=area,aqi=AQI,humidity=humidity,temperature=temp, CO=float(CO),NO2=float(NO2),O3=float(O3),PM10=float(PM10),PM25=float(PM25),SO2=float(SO2))
        db.session.add(row)
        db.session.commit()
        
        return 'DB changes made successfully'
    return 'Forbidden'


@app.route('/check', methods = ['GET'])
def check():
    return 'Welcome To AQI management server'

@app.route('/', methods = ['GET','POST'])
def index():

    means = df.groupby('area',as_index=False).mean()
    max1 = means.iloc[means.AQI.idxmax()]
    min1 = means.iloc[means.AQI.idxmin()]
    waqi = max1[3]
    warea = max1.area
    baqi = min1[3]
    barea = min1.area
    count = len(df.area.unique())
    means = df.groupby('area').mean().sort_values(by='AQI')
    return render_template('index.html', barea = barea, baqi=baqi, waqi=waqi, warea= warea, count = count, means = means.to_html(classes='table-responsive data') )

@app.route('/map', methods = ['GET','POST'])
def map():
    
    return render_template('my_map.html')
    
db.create_all()

if __name__ == '__main__':
    
    app.run(host = '0.0.0.0', port = 5000, debug=True)
    

    
    
