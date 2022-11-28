# App Data Scanner Service

## Description

The **AppScannerService** is a Python-based Flask service providing the interface design for the development of data collection operations (i.e., query and scan) and data collection techniques (i.e., web scraping and API consumption) for each of these operations. This adaptive design facilitates the process of adding new data sources through the interface-based specification of a given operation for a given data source. 

The purpose of this service is to gather and return structured information about apps from multiple, heterogeneous, decentralized data sources. This information includes metadata features (e.g., name, version, category) and natural language documents (e.g., description, summary, changelog, reviews). 

## Architecture

![AppScannerService architecture](https://github.com/gessi-chatbots/app_data_scanner_service/blob/main/app-data-scanner-service(1).png)

## Used technologies

Libraries, frameworks, engines, tools, third-party services...

| Component           | Description                                                           | Version |
|---------------------|-----------------------------------------------------------------------|---------|
| google_play_scraper | Open source scraper that retrieves information from Google Play Store | 1.0.4   |
  | serpapi             | API from SerpApi to extract information from different search engines | 

## How to install

1. Clone project

## How to use

1. Run "Controller.py" to start the flask server.
2. Send a POST request to the flask server with an "app_list" parameter including a json array of app package names.
3. Receive info about the package names in a structured way.

The information provided has the following formatting:
  ```json  
{
      "app_name":"OsmAnd — Maps & GPS Offline",
      "description":"OsmAnd is an offline world map application based on OpenStreetMap (OSM), which allows you to navigate taking into account the preferred roads and vehicle dimensions. Plan routes based on inclines and record GPX tracks without an internet connection.\r\nOsmAnd is an open source app. We do not collect user data and you decide what data the app will have access to.\r\n\r\nMain features:\r\n\r\nMap view\r\n• Choice of places to be displayed on the map: attractions, food, health and more;\r\n• Search for places by address, name, coordinates, or category;\r\n• Map styles for the convenience of different activities: touring view, nautical map, winter and ski, topographic, desert, off-road, and others;\r\n• Shading relief and plug-in contour lines;\r\n• Ability to overlay different sources of maps on top of each other;\r\n\r\nGPS Navigation\r\n• Plotting a route to a place without an Internet connection;\r\n• Customizable navigation profiles for different vehicles: cars, motorcycles, bicycles, 4x4, pedestrians, boats, public transport, and more;\r\n• Change the constructed route, taking into account the exclusion of certain roads or road surfaces;\r\n• Customizable information widgets about the route: distance, speed, remaining travel time, distance to turn, and more;\r\n\r\nRoute Planning and Recording\r\n• Plotting a route point by point using one or multiple navigation profiles;\r\n• Route recording using GPX tracks;\r\n• Manage GPX tracks: displaying your own or imported GPX tracks on the map, navigating through them;\r\n• Visual data about the route - descents/ascents, distances;\r\n• Ability to share GPX track in OpenStreetMap;\r\n\r\nCreation of points with different functionality\r\n• Favourites;\r\n• Markers;\r\n• Audio/video notes;\r\n\r\nOpenStreetMap\r\n• Making edits to OSM;\r\n• Updating maps with a frequency of up to one hour;\r\n\r\nAdditional features\r\n• Android Auto support;\r\n• Compass and radius ruler;\r\n• Mapillary interface;\r\n• Night theme;\r\n• Wikipedia;\r\n• Large community of users around the world, documentation, and support;\r\n\r\nPaid features:\r\n\r\nMaps+ (in-app or subscription)\r\n• Unlimited map downloads;\r\n• Topo data (Contour lines and Terrain);\r\n• Nautical depths;\r\n• Offline Wikipedia;\r\n• Offline Wikivoyage - Travel guides;\r\n\r\nOsmAnd Pro (subscription)\r\n• All Maps+ features;\r\n• OsmAnd Cloud (backup and restore);\r\n• Pro features;\r\n• Hourly map updates.",
      "summary":"Navigation on hikes is no longer a problem. Download the map, put notes and go!",
      "category":"Travel & Local",
      "categoryId":"TRAVEL_AND_LOCAL",
      "in_app_purchases":true,
      "android_version":"6.0",
      "developer":"OsmAnd",
      "developer_site":"https://osmand.net",
      "release_date":"Aug 16, 2010",
      "current_version_release_date":"None",
      "version":"4.1.11",
      "changelog":"• Added initial support for Android Auto\r\n• User interface update for UTM coordinate search\r\n• GPS Filter for GPX Tracks\r\n• Elevation Widget (Pro)\r\n• Favorites: added ability to view recently used icons\r\n• Route planning: will use the selected profile after launch\r\n• Fixed Mapillary layer, the plugin is now disabled by default\r\n• Added screen to manage all history in the app\r\n• Map orientation is not reset after restarting the app\r\n• Improved SRTM height marker rendering\r\n• Fixed Arabic map captions",
      "reviews":[
         {
            "review":"great app",
            "reply":"None"
         },
         {
            "review":"nice",
            "reply":"None"
         },
         {
            "review":"i really want to like this app, but it just does not work. when compared to google maps, i can simply look up a town and it will show up, on osmand it does not. navigation and just going through the UI in general is a bad experience.",
            "reply":"Hello! Thank you for the feedback.\nCould you please provide more details about the issue?\nYou can contact us at support@osmand.net."
         }
      ],
      "similar_apps":"None",
      "package_name":"net.osmand",
      "other_apps":"None",
      "play_store_link":"https://play.google.com/store/apps/details?id=net.osmand&hl=en&gl=us"
```
## Notes for developers

Branch 'develop' for new feature integration

## License

Free use of this software is granted under the terms of the GNU General Public License v3.0: https://www.gnu.org/licenses/gpl.html
