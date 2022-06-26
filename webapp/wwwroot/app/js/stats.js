
app.controller('StatsController', function ($rootScope, $scope, $log, $interval, Alerts, Services) {


  // GUI content ready trigger
  $rootScope.ContentLoaded = false;
  // Polls settings
  var Polls = {
    Stats: { Checker: null, Timer: 10000 }
  };
  // Stats data
	$scope.Stats = {};

  var NimbleAPIDeepStats = 'https://api.wmspanel.com/v1/deep';
  var client_id = '8efc5a51-70d5-4856-bdf3-87761976ebf3';
  var api_key = 'e3209909392aff33c975f85daca77968';
  var data_slice_full = '544e65977d5c004d8e00001d';
  var data_slice_dvr = '5f525e6d45475e67d77cb797';
  var d = new Date();
  var days_stats = 30;
  d.setDate(d.getDate() - days_stats);
  var date_from = dateToYMD(d);
  var date_to = dateToYMD(new Date());
  var sort_by = 'Most';
  var elements = '100';
  var kind = 'Unique';
  var APIReq = '?client_id=' + client_id + '&api_key=' + api_key + '&data_slice=' + data_slice_full + '&from=' + date_from + '&to=' + date_to + '&sort=' + sort_by + '&top=' + elements + '&kind=' + kind;

  $log.debug('StatsController: APIReq ', APIReq);


  function dateToYMD(date) {
    var d = date.getDate();
    var m = date.getMonth() + 1;
    var y = date.getFullYear();
    return '' + y + '-' + (m<=9 ? '0' + m : m) + '-' + (d <= 9 ? '0' + d : d);
  }


  // Server list request. Hash is optional.
  $scope.StatsGet = function() {
    Services.Get(NimbleAPIDeepStats, APIReq)
    .then(
      function(success) {
//        $scope.Stats.List = success.items;
        $log.debug('StatsGet: success: ', success);
//        $log.debug('StatsGet: success: ', $scope.Stats.List);
      },
      function(error) {
        $scope.Stats.List = {};
        $log.error('StatsGet: error: ', error);
      	//Alerts.Add('Stats', 'danger', 'Stats: ' + error.statusText);
      }
    );
  }

  // Start poll(s)
  $scope.StartPolls = function() {
    $scope.StopPolls();
    Polls.Stats.Checker = $interval(function() {
        $scope.StatsGet();
    }, Polls.Stats.Timer);
    $log.debug('Stats poll started');
  }


  // Stop poll(s)
  $scope.StopPolls = function() {
    $interval.cancel(Polls.Stats.Checker);
    $log.debug('Stats poll terminated');
  }


  // Reset controller on view change
  $scope.$on('$destroy', function() {
    $scope.StopPolls();
	  $rootScope.ContentLoaded = false;
  });


  // First load controller init
  $scope.ControllerInit = function() {
    Services.Get(NimbleAPIDeepStats, APIReq)
    .then(
      function(success) {
//        $scope.Stats.List = success.items;
//        $scope.tableParams.settings({ dataset: $scope.Stats.List });
//        $scope.tableParams.parameters({ count: 25 });
        $log.debug('StatsGet: success: ', success);
//        $log.debug('StatsGet: success: ', $scope.Stats.List);
      },
      function(error) {
        $scope.Stats.List = {};
        //Alerts.Add('Stats', 'danger', 'Stats: ' + error.statusText);
      }
    );
    $log.debug('StatsController is ready');
  }

  $scope.ControllerInit();
//  $scope.StartPolls();

});
