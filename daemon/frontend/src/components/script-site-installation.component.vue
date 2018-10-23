<template>
	<button v-show="has_printers" aria-label="script d'installation de site"
			role="button"
			class="hidden-sm-down btn btn-link btn-sm hide-btn-content hint--top"
			@click="getScript(site)"
	>
		<i class="fa fa-file-code-o text-info"> </i>
	</button>

</template>
<script type="text/ecmascript-6">
import actions from 'vuex/actions';

export default {
  props: {
    has_printers: { type: Boolean, required: true },
    site: { type: Object, required: true }
  },
  methods: {
    getScript(site) {
      this.getSiteScript(site)
        .then(response => {
          this.saveFile(response);
        })
        .catch(err => {
          console.error('Échec du téléchargement du script.', err);
        });
    }
  },
  vuex: {
    actions: {
      getSiteScript: actions.getSiteScript,
      saveFile: actions.saveFile
    }
  }
};
</script>
