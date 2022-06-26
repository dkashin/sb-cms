
app.controller('CollosController', function ($rootScope, $scope, $log, $interval, Alerts, Services) {


  // GUI content ready trigger
  $rootScope.ContentLoaded = false;
  // Polls settings
  var Polls = {
    Collos: { Checker: null, Timer: 2000 }
  };
  // Collos data
	$scope.Collos = {};

  // Server list request. Hash is optional.
  $scope.CollosListGet = function() {
    Services.Get($rootScope.StaboxAPIURL, 'colos')
    .then(
      function(success) {
        $scope.Collos.List = success.items;
        $log.debug('CollosListGet: success: ', $scope.Collos.List);
      },
      function(error) {
        $scope.Collos.List = {};
      	//Alerts.Add('Collos', 'danger', 'Collos: ' + error.statusText);
      }
    );
  }

  // Start poll(s)
  $scope.StartPolls = function() {
    $scope.StopPolls();
    Polls.Collos.Checker = $interval(function() {
        $scope.CollosListGet();
    }, Polls.Collos.Timer);
    $log.debug('Collos poll started');
  }


  // Stop poll(s)
  $scope.StopPolls = function() {
    $interval.cancel(Polls.Collos.Checker);
    $log.debug('Collos poll terminated');
  }


  // Reset controller on view change
  $scope.$on('$destroy', function() {
    $scope.StopPolls();
	  $rootScope.ContentLoaded = false;
  });


  // First load controller init
  $scope.ControllerInit = function() {
    Services.Get($rootScope.StaboxAPIURL, 'colos')
    .then(
      function(success) {
        $scope.Collos.List = success.items;
        $scope.tableParams.settings({ dataset: $scope.Collos.List });
        $scope.tableParams.parameters({ count: 25 });
        $log.debug('CollosListGet: success: ', $scope.Collos.List);
      },
      function(error) {
        $scope.Collos.List = {};
        //Alerts.Add('Collos', 'danger', 'Collos: ' + error.statusText);
      }
    );
    $log.debug('CollosController is ready');
  }

  $scope.ControllerInit();
  $scope.StartPolls();

});
