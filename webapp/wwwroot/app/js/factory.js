
// Alerts
app.factory('Alerts', function() {

  var Alerts = {};
  var Queue = [];

  Alerts.Queue = Queue;

  Alerts.Add = function (action, type, msg) {
    Queue.push({ 'action': action, 'type': type, 'msg': msg });
  };

  Alerts.Close = function(index) {
    Queue.splice(index, 1);
  };

  return Alerts;
});


// Local storage manager
app.factory('LSM', function($rootScope, $log) {

  var LSM = {};

  LSM.Load = function(Value) {
    var UserLSData = null;
    if ($rootScope.CurrentUser.Name in localStorage) {
      UserLSData = JSON.parse(localStorage[$rootScope.CurrentUser.Name]);
      Value ? UserLSData = UserLSData[Value] : null;
      $log.debug('LSM.Load:', UserLSData);
    } else {
      $log.debug('LSM.Load: User has no saved settings');
    }
    return UserLSData;
  };

  LSM.Save = function(Data) {
    var UserLSData = JSON.parse(localStorage[$rootScope.CurrentUser.Name] || '{}');
    UserLSData = Object.assign({}, UserLSData, Data);
    $log.debug('LSM.Save:', UserLSData);
    localStorage[$rootScope.CurrentUser.Name] = JSON.stringify(UserLSData);
  };

  return LSM;
});


// Filters
app.factory('Filters', function() {

  var Filters = {};
  var FiltersData;
  var Logic = [
    { 'alias': 'AND', 'value': 'and' },
    { 'alias': 'OR', 'value': 'or' }
  ];

  Filters.Default = function() {
    return angular.copy(FiltersData.Default);
  };

  Filters.Init = function(Data) {
    FiltersData = Data;
  };

  Filters.Data = function() {
    return FiltersData;
  };

  Filters.Logic = function() {
    return Logic;
  };

  Filters.Add = function() {
    FiltersData.Active.push(Default());
  };

  Filters.Delete = function(index, active_filter) {
    if (active_filter.value in FiltersData.Quick) {
      FiltersData.Quick[active_filter.value] = !FiltersData.Quick[active_filter.value];
    }
    if (index == 0 && FiltersData.Active.length <= 1) {
      FiltersData.Active = [ Default() ];
    } else {
      FiltersData.Active.splice(index, 1);
    }
  };

  Filters.Change = function() {};

  Filters.Show = function() {
    FiltersData.Show = !FiltersData.Show;
  };

  Filters.Reset = function(active_filter) {
    active_filter.value = null;
  };

  // Apply filter preset (quick filter)
  Filters.Quick = function(field, value, type) {
    FiltersData.Quick[value] = !FiltersData.Quick[value];
    // Add new filter
    if (FiltersData.Quick[value]) {
      if (FiltersData.Active[0].value == null) {
        FiltersData.Active = [ Default() ];
        FiltersData.Quick.forEach(function(value, key) { FiltersData.Quick[key] = false; });
      } else {
        FiltersData.Active.push({ field: field, value: value, type: type });
      }
    } else {
    // Find and remove filter
      for (FA in FiltersData.Active) {
        if (FiltersData.Active[FA].field == field && FiltersData.Active[FA].value == value) {
          if (FiltersData.Active.length == 1) { Add() }
          FiltersData.Active.splice(FA, 1);
        }
      }
    }
  };

  return Filters;
});


// AV presets
app.factory('Services', function($rootScope, $log, $q, $http) {

  var Services = {};

  Services.Get = function(API, service) {
    var deferred = $q.defer();
    $http.get(API + service)
    .then(
      function(success) {
        $log.debug('Services.Get response:', success);
        deferred.resolve(success.data);
      },
      function(error) {
        $log.error('Services.Get response:', error);
        deferred.reject(error);
      }
    );
    return deferred.promise;
  };

  return Services;

});

