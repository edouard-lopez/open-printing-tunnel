import Vue from 'vue';
import Vuex from 'vuex';
import createLogger from '../middlewares/logger';
import mutations from './mutations';

Vue.use(Vuex);
Vue.config.debug = true;

const debug = process.env.NODE_ENV !== 'production';

const state = {
	sites: [],
	/**
	 {
        hostname: '192.168.2.23',
        id: 'akema',
        printers: [
            {
                description: 'bureau',
                destination_port: 9100,
                forward: 'normal',
                hostname: '1.2.3.4',
                id: 0,
                listening_port: 9102
            }
        ]
    }
	 */
	daemon: {}
};

export default new Vuex.Store({
	state,
	mutations,
	strict: debug,
	middlewares: debug ? [createLogger()] : []
});
