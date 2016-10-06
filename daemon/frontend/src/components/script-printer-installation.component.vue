<template>
	<button aria-label="script d'installation d'imprimante"
			role="button"
			class="btn btn-sm btn-link hide-btn-content hint--top-left"
			@click="getScript(site, printer)"
	>
		<i class="fa fa-file-code-o"> </i>
	</button>
</template>
<script type="text/ecmascript-6">
	import actions from 'vuex/actions';

	export default {
		props: {
			printer: {type: Object, required: true},
			site: {type: Object, required: true}
		},
		methods: {
			getScript(site, printer) {
				this.getPrinterScript(site, printer)
						.then(response => {
							this.saveFile(response);
						})
						.catch(err => {
							console.error('Échec du téléchargement du script.', err);
						})
			}
		},
		vuex: {
			actions: {
				getPrinterScript: actions.getPrinterScript,
				saveFile: actions.saveFile
			}
		}


	}
</script>
