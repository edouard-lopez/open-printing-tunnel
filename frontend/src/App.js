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

angular.module(MODULE_NAME, [
    'ngRoute',
    // 'api',
])
    .config(routeConfig)
    .config(httpConfig)
    .directive('app', app)
    .controller('AppCtrl', AppCtrl);

let routeConfig = ($routeProvider) => {
    $routeProvider
        .when('/', {
            redirectTo: '/login/'
        })
        .when('/login/', {
            template: '<login></login>'
        })
        .otherwise({
            redirectTo: '/'
        });
};

let httpConfig = ($http, $translate) => {
    $http.defaults.xsrfCookieName = 'csrftoken';
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
};


export default MODULE_NAME;