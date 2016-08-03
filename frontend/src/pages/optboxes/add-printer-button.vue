<style>
	.new-printer {
		display: inline-block;
	}
</style>
<template>
	<div class="new-printer">
		<button aria-label="Ajouter une imprimante"
				role="button"
				class="btn btn-success btn-sm btn-action hide-btn-content hint--top"
				data-toggle="modal"
				data-target="#new-printer-modal-{{printer.optbox}}"
		>
			<i class="fa fa-plus-circle"> </i>
		</button>
		<div class="modal fade" id="new-printer-modal-{{printer.optbox}}" tabindex="-1" role="dialog" aria-labelledby="action-label"
			 aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content text-xs-left">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
						<h4 class="modal-title" id="action-label">Ajouter une imprimante</h4>
					</div>
					<form @submit="addPrinter()">
						<div class="modal-body">
							<fieldset class="form-group">
								<label for="optbox">Nom du boîtier<span class="text-danger">*</span></label>

								<input type="text" disabled class="form-control" id="optbox" v-model="printer.optbox" />
							</fieldset>
							<fieldset class="form-group">
								<label for="hostname">Adresse de l'imprimante<span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="hostname"
									   placeholder="ex. 10.0.254.1" v-model="printer.hostname"/>
							</fieldset>
							<fieldset class="form-group">
								<label for="description">Description</label>

								<input type="text" class="form-control" id="description"
									   placeholder="ex. salle de réunion" v-model="printer.description"/>
							</fieldset>
						</div>
						<div class="modal-footer">
							<button type="button" class="btn btn-secondary" data-dismiss="modal">Annuler</button>
							<button type="submit" class="btn btn-primary" v-on:click.stop.prevent="addPrinter"
									:disabled="!formIsValid">
								<span v-if="!formSubmitted">Créer</span>
								<span v-else><i class="fa fa-spinner fa-pulse fa-fw"></i> Création en cours</span>
							</button>
						</div>
					</form>
				</div>
			</div>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	import logging from '../../services/logging';
	import resource from 'pilou';

	const printers = resource('printers', {create: '/daemon/${resource}/'});

	export default {
		data() {
			return {
				printer: {
					optbox: '',
					hostname: ''
				},
				formSubmitted: false
			};
		},
		created() {
			this.printer.optbox = this.boitier.name
		},
		props: {
			boitier: {
				type: Object,
				required: true
			}
		},
		methods: {
			addPrinter(){
				this.formSubmitted = true;

				printers.create(this.printer)
						.then(() => {
							$('#new-printer-modal-'+printer.optbox).modal('hide');
							this.formSubmitted = false;
							this.$dispatch('PrinterCreated');
						})
						.catch(() => {
							this.formSubmitted = false;
							logging.error('Impossible d\'ajouter l\'imprimante');
						});
			},
		},
		computed: {
			formIsValid(){
				return !!(
						this.printer.optbox
						&& this.printer.hostname
						&& !this.formSubmitted
				);
			}
		},
	};
</script>

