import Vue from 'vue';

export default {
  setSites(state, sites) {
    state.sites = sites.map(site => ({ config: {}, ...site }));
  },
  clearLog(state) {
    const empty = [];
    state.log = empty;
  },
  logResponse(state, response) {
    state.log.push(response.results);
  },
  setNetworksData(state, data) {
    state.networks = data;
    state.networks = { ...state.networks }; // prevent vuejs reactivity caveats
  },
  setScanClipboard(state, site) {
    state.scans[site.id] = site.scan;
    state.scans = { ...state.scans }; // prevent vuejs reactivity caveats
  },
  setSiteConfig(state, { site, config }) {
    const siteIndex = state.sites.findIndex(item => item.id === site.id);

    if (siteIndex !== -1) {
      Vue.set(state.sites[siteIndex], 'config', config);
    }
  }
};
