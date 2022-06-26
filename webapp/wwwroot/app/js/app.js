

var app = angular.module('STABox', [ 'ngRoute', 'ngTable' ]);


app.run(function ($rootScope, $log) {
});


app.controller('AppController', function ($rootScope, $scope, $log, $location, Alerts, NgTableParams) {

  // GUI content ready trigger
  $rootScope.ContentLoaded = false;
  // API URL
  $rootScope.StaboxAPIURL = 'http://stabox2.newru.tv/api/v1/';
  // Create ngTable
  $scope.tableParams = new NgTableParams();

  $scope.NavBarActive = function(page) {
    var currentRoute = $location.path().substring(1) || 'services';
    return page === currentRoute ? 'active' : '';
  }


});
