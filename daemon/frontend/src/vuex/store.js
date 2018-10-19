import Vue from 'vue';
import Vuex from 'vuex';
import mutations from './mutations';

Vue.use(Vuex);
Vue.config.debug = true;

const debug = process.env.NODE_ENV !== 'production';

// eslint-disable-next-line no-unused-vars
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
		],
		config: { }  // dynamicly inserted
    }
	],
	log: [/*
	 {
	 'help': 'service has not been started yet',
	 'id': 'akema',
	 'state': 'off'
	 }
	 */],
	networks: {
		/*
		 'akema': {
		 '1.1.1.1': {'ping': None, 'telnet': None},
		 '1.2.3.4': {'ping': None},
		 'ping': None,
		 'telnet': None,
		 },
		 'coaxis': {
		 '1.1.1.1': {'ping': None, 'telnet': None},
		 '8.8.8.8': {'ping': None, 'telnet': None},
		 'ping': None,
		 '1.2.3.4': {'telnet': None},
		 'telnet': None,
		 }
		 */
	},
	scans: {
		/**/
	}
};

export default new Vuex.Store({
	state,
	mutations,
	strict: debug
});
