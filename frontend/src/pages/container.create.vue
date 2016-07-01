<style scoped>
</style>
<template>
	<div id="containers-page">
		<!-- Modal -->
		<div class="modal fade" id="createModal" tabindex="-1" role="dialog" aria-labelledby="createModalLabel"
			 aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
						<h4 class="modal-title" id="createModalLabel">Création d'un conteneur</h4>
					</div>
					<div class="modal-body">
						<form @submit="createContainer()">
							<fieldset class="form-group">
								<label for="description">Description <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="description"
									   placeholder="Description" />
							</fieldset>
						</form>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Annuler</button>
						<button type="button" class="btn btn-primary" @click="createContainer">Créer</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	import 'bootstrap/dist/js/umd/modal';
	import Containers from '../services/containers';
	import logging from '../services/logging';

	Containers.localStorage = localStorage;
	export default {
		data() {
			return {
				container: {
					description: ''
				},
			};
		},
		ready(){
			$('#createModal').modal('show');
		},
		components: {},
		methods: {
			createContainer(){
				Containers.create(this.container)
						.then(createdContainer => {
							logging.success('Container successfully created');
							$('#createModal').modal('hide');
							this.$router.go(`/containers/`);
						})
						.catch(() => {
							logging.error('Cannot create container');
						});
			},
		},
	};
</script>

