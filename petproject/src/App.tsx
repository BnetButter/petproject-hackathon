

import React, { useEffect, useRef } from 'react';
import { loadModules } from 'esri-loader';
import './App.css';

import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import { Box, Button } from "@mui/material"
import { styled } from '@mui/system';


const Input = styled('input')({
  display: 'none',
});

const UploadBox: React.FC = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '30%',
        border: '2px dashed #ccc',
        borderRadius: '8px',
        padding: '16px',
        backgroundColor: '#f9f9f9',
      }}
    >
      <Typography variant="h6" gutterBottom>
        Upload Inspection Report
      </Typography>
      <label htmlFor="upload-button">
        <Input accept="*" id="upload-button" multiple type="file" />
        <Button variant="contained" component="span">
          Choose File
        </Button>
      </label>
    </Box>
  );
};


const Footer: React.FC = () => {
  return (
    <AppBar position="static" color="primary" sx={{ top: 'auto', bottom: 0 }}>
      <Toolbar>
        <Box display="flex" justifyContent="center" width="100%">
          <Typography variant="body1">
            &copy; {new Date().getFullYear()} Kevin Lai
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};


const Header: React.FC = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6">
          Pet Project Hackathon
        </Typography>
      </Toolbar>
    </AppBar>
  );
};


const featureLayerData = {
  source: [
    {
      geometry: {
        type: 'point',
        longitude: -90.199402,
        latitude: 38.627003
      },
      attributes: {
        ObjectId: 1,
        Name: 'St. Louis'
      }
    },
    {
      geometry: {
        type: 'point',
        longitude: -94.572331,
        latitude: 39.091724
      },
      attributes: {
        ObjectId: 2,
        Name: 'Kansas City'
      }
    },
    {
      geometry: {
        type: 'point',
        longitude: -92.173516,
        latitude: 38.576702
      },
      attributes: {
        ObjectId: 3,
        Name: 'Jefferson City'
      }
    },
    {
      geometry: {
        type: 'point',
        longitude: -91.053516,
        latitude: 38.573702
      },
      attributes: {
        ObjectId: 4,
        Name: 'Jefferson City'
      }
    }
  ],
  objectIdField: 'ObjectId',
  fields: [
    {
      name: 'ObjectId',
      type: 'oid'
    },
    {
      name: 'Name',
      type: 'string'
    }
  ],
  renderer: {
    type: 'simple',
    symbol: {
      type: 'simple-marker',
      color: 'red',
      outline: {
        color: 'white',
        width: 1
      }
    }
  },
  popupTemplate: {
    title: '{Name}',
    content: 'This is {Name}.'
  }
};



const EsriMap: React.FC = () => {
  const mapRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // lazy load the required ArcGIS API for JavaScript modules and CSS
    loadModules([
        'esri/Map', 
        'esri/views/MapView', 
        'esri/layers/FeatureLayer',
    
      ], { css: true })
      .then(([Map, MapView, FeatureLayer, QueryTask, Query, Graphic]) => {
        const map = new Map({
          basemap: 'streets-vector'
        });

        const view = new MapView({
          container: mapRef.current as HTMLDivElement,
          map: map,
          center: [-92.603760, 38.573936], // Longitude, latitude for Missouri
          zoom: 6
        });

        const featureLayer = new FeatureLayer(featureLayerData);
        map.add(featureLayer)

        const congressionLayer = new FeatureLayer({
          url: "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Legislative/MapServer/5"
        })

        console.log(featureLayer)

        map.add(congressionLayer)
        
        return () => {
          if (view) {
            // destroy the map view
            view.destroy();
          }
        };
      })
      .catch(err => {
        console.error(err);
      });
  }, []);

  return <div className="webmap" ref={mapRef} style={{ height: '100vh', width: '100%' }}></div>;
};

function App() {
  return (
    <div className="App">
      <Header/>

      <div className="App-content">
        <div className="upload-container">
          <UploadBox />
        </div>
        <div className="map-container">
          <EsriMap />
        </div>
      </div>
      <Footer/>
    </div>
  );
}

export default App;