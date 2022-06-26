
app.controller('ServicesController', function ($rootScope, $scope, $log, $interval, Alerts, Services) {

  // GUI content ready trigger
  $rootScope.ContentLoaded = false;
  // Polls settings
  var Polls = {
    Service: { Checker: null, Timer: 2000 }
  };
  // Service data
	$scope.Service = {};

  // Server list request. Hash is optional.
  $scope.ServiceListGet = function() {
    Services.Get($rootScope.StaboxAPIURL, 'services')
    .then(
      function(success) {
        $scope.Service.List = success.items;
        $log.debug('ServicesListGet: success: ', $scope.Service.List);
      },
      function(error) {
        $scope.Service.List = {};
      	//Alerts.Add('services', 'danger', 'Services: ' + error.statusText);
      }
    );
  }

  // Start poll(s)
  $scope.StartPolls = function() {
    $scope.StopPolls();
    Polls.Service.Checker = $interval(function() {
        $scope.ServiceListGet();
    }, Polls.Service.Timer);
    $log.debug('Service poll started');
  }


  // Stop poll(s)
  $scope.StopPolls = function() {
    $interval.cancel(Polls.Service.Checker);
    $log.debug('Service poll terminated');
  }


  // Reset controller on view change
  $scope.$on('$destroy', function() {
    $scope.StopPolls();
	  $rootScope.ContentLoaded = false;
  });


  // First load controller init
  $scope.ControllerInit = function() {
    Services.Get($rootScope.StaboxAPIURL, 'services')
    .then(
      function(success) {
        $scope.Service.List = success.items;
        $scope.tableParams.settings({ dataset: $scope.Service.List });
        $scope.tableParams.parameters({ count: 25 });
//        $log.debug('tableParams', $scope.tableParams);
        $log.debug('ServicesListGet: success: ', $scope.Service.List);
      },
      function(error) {
        $scope.Service.List = {};
        //Alerts.Add('services', 'danger', 'Services: ' + error.statusText);
      }
    );
    $log.debug('ServicesController is ready');
  }

  $scope.ControllerInit();
  $scope.StartPolls();

});
