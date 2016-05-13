// (function() {
//   'use strict';
//
//   angular
//     .module('oliproject')
//     .config(router);
//
//   function router($stateProvider, $urlRouterProvider) {
//     $urlRouterProvider.otherwise("/");
//
//     $stateProvider
//       .state('dashboard', {
//         url: "/",
//         templateUrl: "dashboard/dashboard.html",
//         controller: 'DashboardController',
//         controllerAs: 'dashboardVM',
//       })
//       .state('jugglers', {
//         url: "/jugglers",
//         templateUrl: "jugglers/jugglers.html",
//         controller: 'JugglersController',
//         controllerAs: 'jugglersVM',
//       });
//   }
// })();