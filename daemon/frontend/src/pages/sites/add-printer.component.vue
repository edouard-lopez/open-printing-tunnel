<style>
	.modal.in {
		font-weight: normal;
	}
</style>
<template>
	<button aria-label="Ajouter une imprimante"
			role="button"
			class="btn btn-success btn-action hide-btn-content hint--top {{class}}"
			data-toggle="modal"
			data-target="#printer-modal-{{printer.site}}"
	>
		<i class="fa fa-plus-circle"> </i>
		<span v-if="label">{{label}}</span>
	</button>
	<div class="modal fade" id="printer-modal-{{printer.site}}"
		 tabindex="-1"
		 role="dialog"
		 aria-labelledby="action-label"
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
							<label for="site">Nom du boîtier<span class="text-danger">*</span></label>

							<input type="text" disabled class="form-control" id="site" v-model="printer.site"/>
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
</template>
<script type="text/ecmascript-6">
	import http from 'services/http.service';
	import logging from 'services/logging.service';
	import actions from 'vuex/actions';
	import getters from 'vuex/getters';

	const printers = http('printers', localStorage);


	export default {
		data() {
			return {
				printer: {
					site: '',
					hostname: ''
				},
				formSubmitted: false
			};
		},
		created() {
			this.printer.site = this.site.id
		},
		props: {
			site: {
				type: Object,
				required: true
			},
			label: {},
			class: {}
		},
		methods: {
			addPrinter(){
				this.formSubmitted = true;

				printers.create(this.printer).then((response) => {
					this.getSites();
					$('#printer-modal-' + response.data.site).modal('hide');
					this.formSubmitted = false;
				}).catch((err) => {
					console.log(err);
					this.formSubmitted = false;
					logging.error('Impossible d\'ajouter l\'imprimante');
				});
			},
		},
		computed: {
			formIsValid(){
				return !!(
						this.printer.site
						&& this.printer.hostname
						&& !this.formSubmitted
				);
			}
		},
		vuex: {
			actions: {
				getSites: actions.getSites,
			},
		}
	};
</script>

