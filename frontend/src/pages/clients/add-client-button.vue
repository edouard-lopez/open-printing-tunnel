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
								<label for="description">Client <span class="text-danger">*</span></label>
								<select class="form-control" v-model="client.company_id" required>
									<option v-for="company in companies" v-bind:value="company.id">
										{{ company.name }}
									</option>
								</select>
							</fieldset>
							<fieldset class="form-group">
								<label for="subnet">Subnet <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="subnet" required
									   placeholder="Subnet (i.e. 10.0.0.0/24)" v-model="client.subnet"/>
							</fieldset>
							<fieldset class="form-group">
								<label for="subnet">Gateway <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="gateway" required
									   placeholder="10.0.0.254" v-model="client.gateway"/>
							</fieldset>
							<fieldset class="form-group">
								<label for="subnet">Container IP <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="containerIp" required
									   placeholder="10.0.0.1" v-model="client.ip"/>
							</fieldset>
							<fieldset class="form-group">
								<label for="subnet">VLAN Id <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="vlanId" required
									   placeholder="100" v-model="client.vlan_id"/>
							</fieldset>
							<fieldset class="form-group">
								<label for="description">Description</label>

								<input type="text" class="form-control" id="description"
									   placeholder="Description" v-model="client.description"/>
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
	import ClientService from '../../services/containers.service';

	import logging from '../../services/logging.service';

	ClientService.localStorage = localStorage;
	export default {
		data() {
			return {
				client: {
					subnet: '',
					gateway: '',
					ip: '',
					description: '',
					company_id: null,
					vlan_id: null
				},
				formSubmitted: false
			};
		},
		props: {
			companies: {}
		},
		methods: {
			createClient(){
				this.formSubmitted = true;

				ClientService.create(this.client)
						.then(() => {
							$('#newClientModal').modal('hide');
							this.formSubmitted = false;
							this.$dispatch('clientCreated');
						})
						.catch(() => {
							this.formSubmitted = false;
							logging.error('Impossible de créer un client');
						});
			}
		},
		computed: {
			formIsValid(){
				return !!(this.client.subnet
				&& this.client.company_id
				&& this.client.subnet
				&& this.client.gateway
				&& this.client.ip
				&& this.client.vlan_id
				&& !this.formSubmitted);
			}
		}
	};
</script>

