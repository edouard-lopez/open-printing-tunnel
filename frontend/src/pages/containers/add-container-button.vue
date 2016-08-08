<template>
	<div id="newContainer">
		<button type="button" class="btn btn-success" data-toggle="modal"
				data-target="#newContainerModal">
			<i class="fa fa-plus-circle"></i>
			Ajouter un conteneur
		</button>
		<div class="modal fade" id="newContainerModal" tabindex="-1" role="dialog" aria-labelledby="action-label"
			 aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content text-xs-left">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
						<h4 class="modal-title" id="action-label">Créer un conteneur</h4>
					</div>
					<div class="modal-body">
						<form @submit="createContainer()">
							<fieldset class="form-group">
								<label for="subnet">Subnet <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="subnet"
									   placeholder="Subnet (i.e. 10.0.0.0/24)" v-model="container.subnet"/>
							</fieldset>
							<fieldset class="form-group">
								<label for="subnet">Gateway <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="gateway"
									   placeholder="10.0.0.254" v-model="container.gateway"/>
							</fieldset>
							<fieldset class="form-group">
								<label for="subnet">Container IP <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="containerIp"
									   placeholder="10.0.0.2" v-model="container.ip"/>
							</fieldset>
							<fieldset class="form-group">
								<label for="description">Client <span class="text-danger">*</span></label>
								<select class="form-control" v-model="container.company_id">
									<option v-for="company in companies" v-bind:value="company.id">
										{{ company.name }}
									</option>
								</select>
							</fieldset>
							<fieldset class="form-group">
								<label for="description">Description</label>

								<input type="text" class="form-control" id="description"
									   placeholder="Description" v-model="container.description"/>
							</fieldset>
						</form>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Annuler</button>
						<button type="button" class="btn btn-primary" v-on:click.stop.prevent="createContainer"
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
	import Containers from '../../services/containers.service';

	import logging from '../../services/logging.service';

	Containers.localStorage = localStorage;
	export default {
		data() {
			return {
				companies: [],
				container: {
					subnet: '',
					gateway: '',
					ip: '',
					description: '',
					company_id: null
				},
				formSubmitted: false
			};
		},
		props: {
			companies: {}
		},
		methods: {
			createContainer(){
				this.formSubmitted = true;

				Containers.create(this.container)
						.then(() => {
							$('#newContainerModal').modal('hide');
							this.formSubmitted = false;
							this.$dispatch('containerCreated');
						})
						.catch(() => {
							this.formSubmitted = false;
							logging.error('Impossible de créer un conteneur');
						});
			}
		},
		computed: {
			formIsValid(){
				return !!(this.container.subnet && this.container.description && !this.formSubmitted);
			}
		}
	};
</script>

