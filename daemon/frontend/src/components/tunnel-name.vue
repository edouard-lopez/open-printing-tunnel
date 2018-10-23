<template>
	<span class="tunnel-name hint--top"
		  data-toggle="collapse"
		  aria-expanded="false"
		  aria-controls="site-{{site.id}}"
		  data-target="#site-{{site.id}}"
		  aria-label="⇡ {{config.UploadLimit | kb}} | ⇣ {{config.DownloadLimit | kb}}"
	>
		<b class="expandable">{{site.id}}</b>
	</span>
</template>
<script type="text/ecmascript-6">
import tunnelName from './tunnel-name.filter';

import actions from 'vuex/actions';

export default {
  props: {
    site: { type: Object, required: true }
  },
  ready: function() {
    this.getSiteConfig(this.site);
  },
  computed: {
    config() {
      return this.site.config;
    }
  },
  filters: {
    kb: tunnelName.kb
  },
  vuex: {
    actions: {
      getSiteConfig: actions.getSiteConfig
    }
  }
};
</script>
