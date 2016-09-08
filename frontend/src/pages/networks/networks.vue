<template>
	<div id="networks-page">
		<div class="row">
			<div class="col-lg-12">
				<div class="card card-block">
					<div class="row m-b-1">
						<div class="col-md-8">
							<h3 class="m-b-0">Réseaux</h3>
						</div>
					</div>
					<div class="row">
						<div class="col-lg-12">
							<table class="table table-hover table-sm">
								<thead class="thead-inverse">
								<tr>
									<th>
										Nom
									</th>
									<th class="text-xs-center">
										Subnet
									</th>
									<th class="text-xs-center">
										Gateway
									</th>
									<th class="text-xs-center">
										Interface.Vlan Id
									</th>
									<th class="text-xs-right">
										Actions
									</th>
								</tr>
								</thead>
								<tbody>
								<tr v-show="!networks.length">
									<td colspan="6">
										{{ no_network_message }}
									</td>
								</tr>
								<tr v-for="network in networks">
									<td>
										{{network.Name}}
									</td>
									<td class="text-xs-center">
										{{network.IPAM.Config[0].Subnet}}
									</td>
									<td class="text-xs-center">
										{{network.IPAM.Config[0].Gateway}}
									</td>
									<td class="text-xs-center">
										{{network.Options.parent}}
									</td>
									<td class="text-xs-right">
										<delete :promise="deleteNetwork" :object="network" class="btn-sm"
												v-show="isEmptyNetwork(network)">
											<span slot="title">Supprimer le réseau</span>
											<span slot="body">Confirmer la suppression du réseau.</span>
											<span slot="in-progress">Suppression en cours</span>
											<span slot="action">Supprimer le réseau</span>
										</delete>
									</td>
								</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	import DeleteButton from 'components/delete-button';
	import HTTP from 'services/http.service';
	import Logging from 'services/logging.service';

	const Networks = HTTP('networks', localStorage);

	export default {
		data() {
			return {
				count: 0,
				networks: [],
				no_network_message: 'loading....'
			};
		},
		ready(){
			this.getNetworks();
		},
		events: {
			deleteNetwork(network) {
				this.deleteNetwork(network);
			}
		},
		components: {
			'delete': DeleteButton
		},
		methods: {
			deleteNetwork(network){
				return Networks.delete({id: network.Id}).then(() => {
					Logging.success('Réseau supprimé avec succès');
					this.getNetworks();
				}).catch(() => {
					Logging.error('Impossible de supprimer ce réseau pour l\'instant. Retentez dans quelques instants ou contacter un administrateur')
				});
			},
			getNetworks(){
				return Networks.all().then(response => {
					this.networks = response.data;
					this.count = response.data.length;
					if (this.count == 0) {
						this.no_network_message = 'il n\'y a pas de réseau'
					}
				});
			},
			isEmptyNetwork(network){
				return Object.keys(network.Containers).length === 0
			}
		}
	};
</script>


