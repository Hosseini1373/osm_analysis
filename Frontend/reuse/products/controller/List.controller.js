var $ctr={};
var markerDummy=new Array();
var map=undefined;
sap.ui.define([
	"sap/ui/core/sample/RoutingNestedComponent/base/BaseController",
	"sap/m/ColumnListItem",
	"sap/m/Text",
	"sap/base/Log",
	"sap/ui/model/type/Currency",
	'sap/ui/model/json/JSONModel'
], function(Controller,	ColumnListItem, Text, Log, Currency,JSONModel) {
	"use strict";

	return Controller.extend("sap.ui.core.sample.RoutingNestedComponent.reuse.products.controller.List", {

		onInit: function () {
			$ctr=this;
			this.amenity()
		},
// Request the amenities() function in the backend, requesting a List of all possible amenities
// Input: None
// Output: Ajax Promise, containing the Amenity List.
		amenity: function () {
			var that=this
			var dataJSON={}
			return $.ajax({
				type:"GET",
				url:"http://www.localhost:5000/amenities",
				success: function (oData) {
					Log.info("I got the amenity json");
					console.log(oData);
					dataJSON=oData;
					var oModel = new JSONModel(oData);
					that.getView().setModel(oModel,"amenities");
					//return dataJSON
				},
				error: function (err) {
					Log.error("failed to load the amenity json");
				}
			})
		},

		// Leaflet funktion, drawonmap, draw markers on map given amenity.
		onChange: function (oEvent) {
			for(var i=0;i<markerDummy.length;i++) {
				map.removeLayer(markerDummy[i]);
				} 
			$ctr.onDrawMap();
			},

		onRenderAjaxMap:function(){

			var dataJSON={}
			var selectedText = $ctr.byId("box0").getSelectedKey();
			if (selectedText==="" || selectedText===undefined){
				selectedText="Laboratory";
			}
			console.log("selectedText",selectedText);
			return $.ajax({
				type:"GET",
				url:"http://www.localhost:5000/map/"+selectedText,
				success: function (oData) {
					Log.info("I got the map json");
					console.log(oData);
					dataJSON=oData;
					return dataJSON
				},
				error: function (err) {
					Log.error("failed to load json");
				}
			})
		},
		//Initializes and draws the amenities on the map.
		onDrawMap:function() {
		  this.onRenderAjaxMap().then( (dataJSON)=>{
			console.log("hallo")
			var data=[];
			console.log(data)


			for (var key in dataJSON){
				console.log(dataJSON[key]);
			}
			for (let i = 0; i < dataJSON.coords.length; i++) {
				var values = Object.keys(dataJSON.coords[i]).map(function(key){
					return dataJSON.coords[i][key];
				});
				if (values.length<=2){
					values[2]=""
				}
				data.push(values);
				//data.push([line.lat,line.long,line.name])
			  }
			  Log.info(data)
		  // Define the chart to be drawn.
			  return data;

   
   
			
		}).then((data)=>{
		

		if (map===undefined){
			map = L.map('myMap').setView([46.90, 8.13], 8);
			L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
				maxZoom: 19,
				attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
			}).addTo(map);
		}
		//map.invalidateSize();

		for (let i=0 ;i<data.length;i++){

			var marker = L.marker([data[i][0], data[i][1]]).addTo(map);
			markerDummy.push(marker)
			map.addLayer(markerDummy[i]);
			var popup = L.popup();
			marker.on('click', (e)=>{	popup
				.setLatLng(e.latlng)
				.setContent("The Coordinates are: " + e.latlng.toString()+"\nThe name is: "+data[i][2])
				.openOn(map);});
		}
		})
	},



		});
	});
