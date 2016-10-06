<template>
	<button v-show="has_printers" aria-label="script de configuration des ports"
			role="button"
			class="hidden-sm-down btn btn-link btn-sm hide-btn-content hint--top"
			@click="getPortsScript(site)"
	>
		<i class="fa fa-file-code-o text-danger"> </i>
	</button>
</template>
<script type="text/ecmascript-6">
	import actions from 'vuex/actions';

	export default {
		props: {
			has_printers: {type: Boolean, required: true},
			site: {type: Object, required: true}
		},
		methods: {
			getPortsScript(site) {
				this.getConfigurePortsScript(site).then(response => {
					this.saveFile(response);
				}).catch(err => {
					console.error('Échec du téléchargement du script.', err);
				})
			}
		},
		vuex: {
			actions: {
				getConfigurePortsScript: actions.getConfigurePortsScript,
				saveFile: actions.saveFile
			}
		}
	}
</script>
