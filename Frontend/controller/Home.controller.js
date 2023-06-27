sap.ui.define([
	"sap/ui/core/sample/RoutingNestedComponent/base/BaseController",
	"sap/base/Log",
	"sap/ui/model/json/JSONModel"
], function(Controller, Log, JSONModel) {
	"use strict";
	return Controller.extend("sap.ui.core.sample.RoutingNestedComponent.controller.Home", {
		onInit: function() {
			Log.info(this.getView().getControllerName(), "onInit");

			// HTML string bound to the formatted text control
			var oModel = new JSONModel({
				HTML: "<p>Our Analysis of OSM Dataset</p>"
			});

			this.getView().setModel(oModel);
		}
	});
});
