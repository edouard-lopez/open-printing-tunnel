<template>
	<div id="newContainer">
		<button type="button" class="btn btn-success" data-toggle="modal"
				data-target="#newClientModal">
			<i class="fa fa-plus-circle"></i>
			Ajouter un client
		</button>
		<div class="modal fade" id="newClientModal" tabindex="-1" role="dialog" aria-labelledby="action-label"
			 aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content text-xs-left">
					<form v-on:submit.prevent="createClient">
						<div class="modal-header">
							<button type="button" class="close" data-dismiss="modal" aria-label="Close">
								<span aria-hidden="true">&times;</span>
							</button>
							<h4 class="modal-title" id="action-label">Créer un client</h4>
						</div>
						<div class="modal-body">
							<fieldset class="form-group">
								<label for="name">Nom <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="name" required
									   placeholder="Nom de l'entreprise" v-model="client.name"/>
							</fieldset>
						</div>
						<div class="modal-footer">
							<button type="button" class="btn btn-secondary" data-dismiss="modal">Annuler</button>
							<button type="submit" class="btn btn-primary" :disabled="!formIsValid">
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
	import HTTP from 'services/http.service';
	import Logging from '../../services/logging.service';

	const ClientsService = HTTP('clients', localStorage);

	export default {
		data() {
			return {
				client: {
					name: ''
				},
				formSubmitted: false
			};
		},
		methods: {
			createClient(){
				this.formSubmitted = true;

				ClientsService.create(this.client)
						.then(() => {
							$('#newClientModal').modal('hide');
							this.formSubmitted = false;
							this.$dispatch('clientCreated');
						})
						.catch(() => {
							this.formSubmitted = false;
							Logging.error('Impossible de créer un client');
						});
			}
		},
		computed: {
			formIsValid(){
				return !!(this.client.name && !this.formSubmitted);
			}
		}
	};
</script>

