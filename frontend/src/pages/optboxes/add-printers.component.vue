<template>
	<button aria-label="Ajouter des imprimantes"
			role="button"
			class="btn btn-primary btn-action hide-btn-content hint--top"
			data-toggle="modal"
			data-target="#printers-modal-{{printers.optboxName}}">
		<i class="fa fa-plus-circle"></i>
		<span v-if="label">{{label}}</span>
	</button>
	<div class="modal fade" id="printers-modal-{{printers.optboxName}}"
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
				<form @submit="addPrinters()">
					<div class="modal-body">
						<fieldset class="form-group">
							<label for="optboxName">Nom du boîtier<span class="text-danger">*</span></label>

							<input type="text" disabled class="form-control" id="optboxName" v-model="printers.optboxName"/>
						</fieldset>
						<fieldset class="form-group">
							<label for="hostnames">Adresses des imprimantes<span class="text-danger">*</span></label>

							<textarea type="text" class="form-control" id="hostnames" v-model="printers.hostnames"></textarea>
						</fieldset>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Annuler</button>
						<button type="submit" class="btn btn-primary" v-on:click.stop.prevent="addPrinters"
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
	import logging from '../../services/logging';
	import resource from 'pilou';
	import printersService from '../../services/printers';

	const printers = resource('printers', {create: '/daemon/${resource}/'});

	export default {
		data() {
			return {
				printers: {
					optboxName: '',
					hostnames: ''
				},
				formSubmitted: false
			};
		},
		created() {
			this.printers.optboxName = this.boitier.id
		},
		props: {
			boitier: {
				type: Object,
				required: true
			},
			label: {}
		},
		methods: {
			addPrinters(){
				this.formSubmitted = true;
				console.log(printersService.parsePrinters(this.printers.hostnames))
				this.formSubmitted = false;
			},
		},
		computed: {
			formIsValid(){
				return !!(
						this.printers.optboxName
						&& this.printers.hostnames
						&& !this.formSubmitted
				);
			}
		},
	};
</script>

