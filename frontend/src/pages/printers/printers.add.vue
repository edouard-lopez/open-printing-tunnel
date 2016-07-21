<style scoped>
</style>
<template>
	<div id="printers-page">
		<!-- Modal -->
		<div class="modal fade" id="addModal" tabindex="-1" role="dialog" aria-labelledby="addModalLabel"
			 aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
						<h4 class="modal-title" id="addModalLabel">Création d'un conteneur</h4>
					</div>
					<div class="modal-body">
						<form @submit="addPrinter()">
							<fieldset class="form-group">
								<label for="description">Description <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="description"
									   placeholder="Description" />
							</fieldset>
						</form>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Annuler</button>
						<button type="button" class="btn btn-primary" @click="addPrinter">Créer</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	import 'bootstrap/dist/js/umd/modal';
	import Printers from '../../services/printers';
	import logging from '../../services/logging';

	Printers.localStorage = localStorage;
	export default {
		data() {
			return {
				printer: {
					description: ''
				},
			};
		},
		ready(){
			$('#addModal').modal('show');
		},
		components: {},
		methods: {
			addPrinter(){
				Printers.add(this.printer)
						.then(adddPrinter => {
							logging.success('Printer successfully addd');
							$('#addModal').modal('hide');
							this.$router.go(`/printers/`);
						})
						.catch(() => {
							logging.error('Cannot add printer');
						});
			},
		},
	};
</script>

