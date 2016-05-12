import angular from 'angular';
import './App.scss';

let app = () => {
  return {
    template: require('./App.html'),
    controller: 'AppCtrl',
    controllerAs: 'vm'
  }
};

class AppCtrl {
  constructor() {
    this.url = 'https://github.com/preboot/angular-webpack';
  }
}

const MODULE_NAME = 'app';

angular.module(MODULE_NAME, [])
  .directive('app', app)
  .controller('AppCtrl', AppCtrl);

export default MODULE_NAME;