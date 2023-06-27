var $ctr = {};
var tile = {};

sap.ui.define([
	"sap/ui/core/sample/RoutingNestedComponent/base/BaseController",
	"sap/base/Log",
	'sap/ui/model/json/JSONModel'
], function(Controller, Log,JSONModel) {
	"use strict";
	return Controller.extend("sap.ui.core.sample.RoutingNestedComponent.reuse.suppliers.controller.List", {
		onInit:function(){
			$ctr=this;
			var dist_amen = {'dist': 'loading'};
			this.cityAmen();
			tile={
				"TileCollection" : [
					{
						"icon" : "sap-icon://hint",
						"type" : "Monitor",
						"number" : "Zürich",
						"info" : "Number of ATMs",
						'title' : 'loading'
					},
					{
						"icon" : "sap-icon://hint",
						"number" : "Zurich",
						'title' : 'loading',
						"info" : "Number of toilets",
					},
					{
						"icon" : "sap-icon://hint",
						"number" : "Zurich",
						'title': 'loading',
						"info" : "Number of Places of Worship",

					},
					{
						"icon" : "sap-icon://hint",
						"number" : "Zurich",
						'title': 'loading',
						"info" : "Number of Post Offices",

					},
					{
						"icon" : "sap-icon://hint",
						'number':'Zurich',
						"title" : "loading",
						"info" : "Number of kindergarten",
					},
					{ // for the dist
						"icon" : "sap-icon://hint",
						'number':'loading',
						"title" : "Maximum Distance between Amenities of the same type",
					},

	
				]
			}
			this.distanceAmen();
			// set mock model
			var oModel = new JSONModel(tile);

			this.getView().setModel(oModel);
			this.amenity()
		},

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
				},
				error: function (err) {
					Log.error("failed to load the amenity json");
				}
			})
		},


		onChange: function (oEvent) {
			$ctr.distanceAmen();
			},



		cityAmen:function(){

			var dataJSON={};
			var that = this;
			var selectedText = $ctr.byId("box1").getSelectedKey();
			if (selectedText==="" || selectedText===undefined){
				selectedText="Laboratory";
			}
			console.log("selectedText",selectedText);
			return $.ajax({
				type:"GET",
				url:"http://www.localhost:5000/city_amen",
				success: function (oData) {
					Log.info("I got the city_amen json");
					console.log(oData);
					oData = JSON.parse(oData)
					dataJSON=oData;
					that.getView().getModel().setProperty('/TileCollection/0/title', oData['Zurich']['atm']);
					console.log(that.getView().getModel().getProperty('/TileCollection/0/title'));
					that.getView().getModel().setProperty('/TileCollection/1/title', oData['Zurich']['toilets']);
					console.log(that.getView().getModel().getProperty('/TileCollection/1/title'));
					that.getView().getModel().setProperty('/TileCollection/2/title', oData['Zurich']['place_of_worship']);
					console.log(that.getView().getModel().getProperty('/TileCollection/2/title'));
					that.getView().getModel().setProperty('/TileCollection/3/title', oData['Zurich']['post_office']);
					console.log(that.getView().getModel().getProperty('/TileCollection/3/title'));
					that.getView().getModel().setProperty('/TileCollection/4/title', oData['Zurich']['kindergarten']);
					console.log(that.getView().getModel().getProperty('/TileCollection/4/title'));


					return dataJSON
				},
				error: function (err) {
					Log.error("failed to load json");
				}
			})
		},

		distanceAmen:function(){

			var dataJSON={};
			var that = this;
			var selectedText = $ctr.byId("box1").getSelectedKey();
			if (selectedText==="" || selectedText===undefined){
				selectedText="Laboratory";
			}
			console.log("selectedText",selectedText);
			return $.ajax({
				type:"GET",
				url:"http://www.localhost:5000/distance/"+selectedText,
				success: function (oData) {
					Log.info("I got the distance json");
					console.log(oData);
					dataJSON=oData;
					that.getView().getModel().setProperty('/TileCollection/5/number', oData['distance']+ ' km');
					console.log(that.getView().getModel().getProperty('/TileCollection/5/title'));
					return dataJSON
				},
				error: function (err) {
					Log.error("failed to load the distance json");
				}
			})
		},

		onPressListItem: function(oEvent) {
		}
	});
});
