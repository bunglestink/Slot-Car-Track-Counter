/**
 * This file contains the controller to manage slot car races.
 */


var RACE_MODE_STOPPED = 0;
var RACE_MODE_STARTED = 1;

var UPDATE_POLL_MILLIS = 1000;


function RaceCtrl($http, $timeout) {
  this.http_ = $http;
  this.timeout_ = $timeout;

  this.isInitialized = false;
  this.raceMode = RACE_MODE_STOPPED;
  this.numberOfLaps = 10;
  this.numberOfTracks = 2;

  this.lapNumbers = [];
  this.trackNumbers = [];

  this.raceStartTime = null;
  this.trackTimes = {};
}


RaceCtrl.prototype.init = function() {
  var self = this;
  this.lapNumbers = this.getLapNumbers();
  this.trackNumbers = this.getTrackNumbers();
  this.http_({method: 'GET', url: 'api/race/isStarted'}).
    success(function(isStarted) {
      self.raceMode = 
          (isStarted == 'true') ? RACE_MODE_STARTED : RACE_MODE_STOPPED;
      self.isInitialized = true;
    }).
    error(function() {
      alert(
          'An error occrred trying to detect the race state.  Please refresh ' +
          'page or reset track counter if issue persists.');
    });
};


RaceCtrl.prototype.startRace = function() {
  var self = this;
  this.lapNumbers = this.getLapNumbers();
  this.trackNumbers = this.getTrackNumbers();
  this.http_({method: 'POST', url: '/api/race/start'}).
    success(function() {
      self.raceMode = RACE_MODE_STARTED;
      self.updateRaceTimes();
    }).
    error(function() {
      alert(
          'An error occrred trying to start the race.  Please refresh ' +
          'page or reset track counter if issue persists.');
    });
};


RaceCtrl.prototype.stopRace = function() {
  var self = this;
  this.http_({method: 'POST', url: '/api/race/stop'}).
    success(function() {
      self.raceMode = RACE_MODE_STOPPED;
    }).
    error(function() {
      alert(
          'An error occrred trying to stop the race.  Please refresh ' +
          'page or reset track counter if issue persists.');
    });
};


RaceCtrl.prototype.updateRaceTimes = function() {
  var self = this;
  this.http_({method: 'GET', url: '/api/race/stats'}).
    success(function(data) {
      self.raceStartTime = self.calculateRaceStartTime_(data);
      self.trackTimes = data;
      if (self.isRaceStarted()) {
        self.timeout_(function() {
          self.updateRaceTimes();
        }, UPDATE_POLL_MILLIS);
      }
    }).
    error(function() {
      if (console && console.log) {
        console.log('An error occurred updating the track counter.');
      }
      if (self.isRaceStarted()) {
        self.timeout_(function() {
          self.updateRaceTimes();
        }, UPDATE_POLL_MILLIS);
      }
    });
};


RaceCtrl.prototype.calculateRaceStartTime_ = function(data) {
  var startingTime = undefined;
  for (var i = 1; i <= this.numberOfTracks; i++) {
    var times = data[i];
    if (!times || !times.length) {
      continue;
    }
    var time = times[0];
    if (!time) {
      continue;
    }
    if (!startingTime || time < startingTime) {
      startingTime = time;
    }
  }
  return startingTime;
};


RaceCtrl.prototype.getTrackTime = function(track, lap) {
  if (typeof track === 'string') {
    track = parseInt(track);
  }
  var times = this.trackTimes[track];
  if (!times) {
    return null;
  }
  var time = times[lap];
  if (typeof time === 'undefined') {
    return null;
  }
  if (lap === 1) {
    return time - this.raceStartTime;
  }
  var previousTime = times[lap - 1];
  return time - previousTime;
};


RaceCtrl.prototype.getLapNumbers = function() {
  return this.enumerateTo_(this.numberOfLaps);
};


RaceCtrl.prototype.getTrackNumbers = function() {
  return this.enumerateTo_(this.numberOfTracks);
};


RaceCtrl.prototype.enumerateTo_ = function(maximum) {
  var result = [];
  if (typeof maximum === 'string') {
    maximum = parseInt(maximum);
  }
  for (var i = 1; i <= maximum; i++) {
    result.push(i);
  }
  return result;
};



RaceCtrl.prototype.isRaceStarted = function() {
  return this.raceMode === RACE_MODE_STARTED;
};

