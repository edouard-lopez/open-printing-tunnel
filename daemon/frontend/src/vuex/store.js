import Vue from 'vue';
import Vuex from 'vuex';
import createLogger from '../middlewares/logger';
import mutations from './mutations';

Vue.use(Vuex);
Vue.config.debug = true;

const debug = process.env.NODE_ENV !== 'production';

const state = {
	sites: [
		/** {
        hostname: '192.168.2.23',
        id: 'akema',
        printers: [
            {
                description: 'bureau',
                id: 0,
				hostname: '1.2.3.4',
                ports: {
					forward: 'remote',
					listen: 9102
                	send: 9100,
                }
            }
        ]
    } */
	],
	log: [/*
	 {
	 'help': 'service has not been started yet',
	 'id': 'akema',
	 'state': 'off'
	 }
	 */],
	pings: {
		/*
		 'akema': {
		 '1.1.1.1': { 'ping': null },
		 '1.2.3.4': { 'ping': null },
		 'ping': null,
		 }
		 */
	},
	telnets: {
		/**
		 'akema': {
			 '1.1.1.1': {'telnet': null},
			 '1.2.3.4': {'telnet': },
			 'telnet': 0.00013
		 }
		 */
	}
};

export default new Vuex.Store({
	state,
	mutations,
	strict: debug,
	middlewares: debug ? [createLogger()] : []
});
