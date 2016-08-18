<template>
	<button aria-label="Ajouter des imprimantes"
			role="button"
			class="btn btn-primary btn-action hide-btn-content hint--top {{class}}"
			data-toggle="modal"
			data-target="#printers-modal-{{printers.siteName}}">
		<i class="fa fa-print"></i>
		<span v-if="label">{{label}}</span>
	</button>
	<div class="modal fade" id="printers-modal-{{printers.siteName}}"
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
					<h4 class="modal-title" id="action-label">Ajouter des imprimante</h4>
				</div>
				<form @submit="addBulk()">
					<div class="modal-body">
						<fieldset class="form-group">
							<label for="siteName">Nom du site<span class="text-danger">*</span></label>

							<input type="text" disabled class="form-control" id="siteName" v-model="printers.siteName"/>
						</fieldset>
						<fieldset class="form-group">
							<label for="hostnames">Adresses des imprimantes<span class="text-danger">*</span></label>

							<textarea class="form-control" id="hostnames" v-model="printers.hostnames"
									  rows="8"
									  placeholder="description    10.100.12.21    9105"
							></textarea>
						</fieldset>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Annuler</button>
						<button type="submit" class="btn btn-primary" v-on:click.stop.prevent="addBulk"
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
	import printersService from 'services/printers.service';
	import actions from 'vuex/actions';

	export default {
		data() {
			return {
				printers: {
					siteName: '',
					hostnames: ''
				},
				formSubmitted: false
			};
		},
		created() {
			this.printers.siteName = this.site.id
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
			addBulk(){
				this.formSubmitted = true;
				const printers = printersService.parsePrinters(this.printers.hostnames);
				for (let printer of printers) {
					printer['site'] = this.site.id;
					this.addPrinter(printer).then(response => {
						this.getSites();
						$('#printers-modal-' + response.data.site).modal('hide');
						this.formSubmitted = false;
					}).catch((err) => {
						console.err(err);
						this.formSubmitted = false;
					});
				}
			}
		},
		computed: {
			formIsValid(){
				return !!(
						this.printers.siteName
						&& this.printers.hostnames
						&& !this.formSubmitted
				);
			}
		},
		vuex: {
			actions: {
				addPrinter: actions.addPrinter,
				getSites: actions.getSites
			}
		}
	};
</script>

