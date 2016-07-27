<template xmlns:v-on="http://www.w3.org/1999/xhtml">
	<div id="newOptbox">
		<button type="button" class="btn btn-success" data-toggle="modal"
				data-target="#newOptboxModal">
			<i class="fa fa-plus-circle"></i>
			Ajouter un boitier
		</button>
		<div class="modal fade" id="newOptboxModal" tabindex="-1" role="dialog" aria-labelledby="action-label"
			 aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content text-xs-left">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
						<h4 class="modal-title" id="action-label">Créer un boitier</h4>
					</div>
					<div class="modal-body">
						<form @submit="createOptbox()">
							<fieldset class="form-group">
								<label for="name">Nom du boitier <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="name"
									   placeholder="ex. client-un" v-model="Optbox.name"/>
							</fieldset>
							<fieldset class="form-group">
								<label for="hostname">Hôte distant <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="hostname"
									   placeholder="ex. 10.0.254.1" v-model="Optbox.hostname"/>
							</fieldset>
						</form>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Annuler</button>
						<button type="button" class="btn btn-primary" v-on:click.stop.prevent="createOptbox"
								:disabled="!formIsValid">
							<span v-if="!formSubmitted">Créer</span>
							<span v-else><i class="fa fa-spinner fa-pulse fa-fw"></i> Création en cours</span>
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	import 'bootstrap/dist/js/umd/modal';
	import Optboxes from '../services/optboxes';
	import logging from '../services/logging';

	Optboxes.localStorage = localStorage;
	export default {
		data() {
			return {
				Optbox: {
					name: '',
					hostname: ''
				},
				formSubmitted: false
			};
		},
		methods: {
			createOptbox(){
				this.formSubmitted = true;

				Optboxes.create(this.Optbox)
						.then(() => {
							$('#newOptboxModal').modal('hide');
							this.formSubmitted = false;
							this.$dispatch('OptboxCreated');
						})
						.catch(() => {
							this.formSubmitted = false;
							logging.error('Impossible d\'ajouter le boitier');
						});
			}
		},
		computed: {
			formIsValid(){
				return !!(this.Optbox.name && this.Optbox.hostname && !this.formSubmitted);
			}
		}
	};
</script>

