sap.ui.define([
	"sap/ui/core/sample/RoutingNestedComponent/base/BaseController",
	"sap/base/Log"
], function(Controller, Log) {
	"use strict";

	return Controller.extend("sap.ui.core.sample.RoutingNestedComponent.reuse.categories.controller.List", {


		onInit: function () {

			this.initSampleDataModel()

		},

		initSampleDataModel: function () {

		},



		onRenderAjaxBar:function(){
			var dataJSON={}
			return $.ajax({
				type:"GET",
				url:"http://www.localhost:5000/bar",
				success: function (oData) {
					console.log("I got the json");
					console.log(oData);
					dataJSON=oData;
					//console.log( Object.values(dataJSON));
					return dataJSON
				},
				error: function (err) {
					Log.error("failed to load json");
				}
			})
		},

		onRender: function () {			
			this.onRenderAjaxBar().then( (dataJSON)=>{
			const ctx = document.getElementById('myChart').getContext('2d');
			const myChart = new Chart(ctx, {
				type: 'bar',
				data: {
					labels: Object.keys(dataJSON),
					datasets: [{
						label: 'Number of places of worship according to religion',
						data: Object.values(dataJSON),
						backgroundColor: [
							'rgba(255, 99, 132, 0.2)',
							'rgba(54, 162, 235, 0.2)',
							'rgba(255, 206, 86, 0.2)',
							'rgba(75, 192, 192, 0.2)',
							'rgba(153, 102, 255, 0.2)',
							'rgba(255, 159, 64, 0.2)'
						],
						borderColor: [
							'rgba(255, 99, 132, 1)',
							'rgba(54, 162, 235, 1)',
							'rgba(255, 206, 86, 1)',
							'rgba(75, 192, 192, 1)',
							'rgba(153, 102, 255, 1)',
							'rgba(255, 159, 64, 1)'
						],
						borderWidth: 1
					}]
				},
				options: {
					scales: {
						y: {
							beginAtZero: true
						}
					}
				}
			});
		
		
		
		
		
		
		})

		},


	
	});
});
