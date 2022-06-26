

app.config(['$routeProvider', '$locationProvider', '$logProvider', '$httpProvider',
  function($routeProvider, $locationProvider, $logProvider, $httpProvider) {

    $routeProvider.
      when('/', { redirectTo: '/services' }).
      when('/services', { templateUrl: 'html/services.html', controller: 'ServicesController' }).
      when('/collos', { templateUrl: 'html/collos.html', controller: 'CollosController' }).
      when('/stats', { templateUrl: 'html/stats.html', controller: 'StatsController' }).
      otherwise({ redirectTo: '/services' });

    $locationProvider.html5Mode(true);
    $logProvider.debugEnabled(true);
  }
]);

