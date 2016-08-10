<template>
	<div id="newContainer">
		<button type="button" class="btn btn-success" data-toggle="modal"
				data-target="#newDaemonModal">
			<i class="fa fa-plus-circle"></i>
			Ajouter un daemon
		</button>
		<div class="modal fade" id="newDaemonModal" tabindex="-1" role="dialog" aria-labelledby="action-label"
			 aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content text-xs-left">
					<form v-on:submit.prevent="createDaemon">
						<div class="modal-header">
							<button type="button" class="close" data-dismiss="modal" aria-label="Close">
								<span aria-hidden="true">&times;</span>
							</button>
							<h4 class="modal-title" id="action-label">Créer un daemon</h4>
						</div>
						<div class="modal-body">
							<fieldset class="form-group">
								<label for="client">Client <span class="text-danger">*</span></label>
								<select id="client" class="form-control" v-model="daemon.client_id" required autofocus>
									<option v-for="client in clients" v-bind:value="client.id">
										{{ client.name }}
									</option>
								</select>
							</fieldset>
							<fieldset class="form-group">
								<label for="subnet">Subnet <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="subnet" required
									   placeholder="Subnet (i.e. 10.0.0.0/24)" v-model="daemon.subnet"/>
							</fieldset>
							<fieldset class="form-group">
								<label for="gateway">Gateway <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="gateway" required
									   placeholder="10.0.0.254" v-model="daemon.gateway"/>
							</fieldset>
							<fieldset class="form-group">
								<label for="containerIp">Container IP <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="containerIp" required
									   placeholder="10.0.0.1" v-model="daemon.ip"/>
							</fieldset>
							<fieldset class="form-group">
								<label for="vlanId">VLAN Id <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="vlanId" required
									   placeholder="100" v-model="daemon.vlan"/>
							</fieldset>
							<fieldset class="form-group">
								<label for="hostname">Hostname <span class="text-danger">*</span></label>

								<input type="url" class="form-control" id="hostname"
									   placeholder="Hostname" v-model="daemon.hostname"/>
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
	import Logging from 'services/logging.service';

	const ClientsService = HTTP('clients', localStorage);
	const DaemonService = HTTP('daemons', localStorage);

	export default {
		data() {
			return {
				clients: [],
				daemon: {
					subnet: '',
					gateway: '',
					ip: '',
					hostname: '',
					client_id: null,
					vlan: null
				},
				formSubmitted: false
			};
		},
		ready(){
			this.getClients();
		},
		methods: {
			getClients(){
				return ClientsService.all().then(response => {
					this.clients = response.data.results;
				});
			},
			createDaemon(){
				this.formSubmitted = true;

				DaemonService.create(this.daemon)
						.then(() => {
							$('#newDaemonModal').modal('hide');
							this.formSubmitted = false;
							this.$dispatch('daemonCreated');
						})
						.catch(() => {
							this.formSubmitted = false;
							Logging.error('Impossible de créer un daemon');
						});
			}
		},
		computed: {
			formIsValid(){
				return !!(this.daemon.ip
				&& this.daemon.subnet
				&& this.daemon.gateway
				&& this.daemon.vlan
				&& this.daemon.hostname
				&& this.daemon.client_id
				&& !this.formSubmitted);
			}
		}
	};
</script>
