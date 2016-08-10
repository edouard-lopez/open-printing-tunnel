<template>
	<div id="clients-page">
		<div class="row">
			<div class="col-lg-12">
				<div class="card card-block">
					<div class="row">
						<div class="col-md-12">
							<h3>Clients</h3>
						</div>
					</div>
					<div class="row">
						<div class="col-md-4">
							<div id="searchClients">
								<div class="input-group">
                                    <span class="input-group-addon" id="search-addon">
                                        <i class="fa fa-search" aria-hidden="true"></i>
                                    </span>
									<input type="text" class="form-control" placeholder="recherche"
										   v-model="search" aria-describedby="search-addon"
										   @keyup="filter(search) | debounce 500">
								</div>
							</div>
						</div>
						<div class="col-md-4">
							<h2>
                                <span class="label label-info">
                                    <span v-if="selected.length>0"> {{selected.length}} / </span> {{count}} client<span
										v-if="clients.length>1">s</span>
                                </span>
							</h2>
						</div>
						<div class="col-md-4 text-xs-right">
							<add-client-button></add-client-button>
						</div>
					</div>
					<div class="row">
						<div class="col-lg-12">
							<table class="table table-hover table-sm">
								<thead class="thead-inverse">
								<tr>
									<th>
										Id
									</th>
									<th>
										Société
									</th>
									<th class="text-xs-right">
										Actions
									</th>
								</tr>
								</thead>
								<tbody>
								<tr v-show="!clients.length">
									<td colspan="6">
										{{ no_client_message }}
									</td>
								</tr>
								<tr v-for="client in clients">
									<td>
										<a v-link="{ name: 'clients', params: { id: client.id }}">
											{{ client.id }}
										</a>
									</td>
									<td>
										{{ client.name }}
									</td>
									<td class="text-xs-right">
										<delete :promise="deleteClient" :object="client" class="btn-sm">
											<span slot="title">Supprimer le client</span>
											<span slot="body">Confirmer la suppression du client et des tunnels associés.</span>
											<span slot="in-progress">Suppression en cours</span>
											<span slot="action">Supprimer le client</span>
										</delete>
									</td>
								</tr>
								</tbody>
							</table>
						</div>
					</div>
					<div class="row m-t-1">
						<div class="paginate">
							<div class="col-xs-4 text-xs-left">
								<button class="btn btn-primary btn-sm" v-if="count > limit"
										:disabled="(currentPage===1)"
										@click="getNext()">
									previous
								</button>
							</div>
							<div class="col-xs-4 text-xs-center" v-if="numberPages > 1">
								{{ currentPage }} / {{ numberPages }}
							</div>
							<div class="col-xs-4 text-xs-right">
								<button class="btn btn-primary btn-sm" v-if="count > limit"
										:disabled="(currentPage*limit >= count)"
										@click="getPrevious()">
									next
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script type="text/ecmascript-6">
	// todo rename services/containers.service
	import AddClientButton from './add-client-button';
	import DeleteButton from '../../components/delete-button';
	import HTTP from 'services/http.service';
	import Logging from '../../services/logging.service';

	const ClientsService = HTTP('clients', localStorage);

	export default {
		data() {
			return {
				limit: 100,
				offset: 0,
				currentPage: 1,
				selectedEntry: null,
				numberPages: 1,
				count: 0,
				sorting: 'asc',
				ordering: '-created',
				search: '',
				no_client_message: 'There is no client.',
				selectAll: false,
				selected: [],
				clients: []
			};
		},
		ready(){
			this.getClients();
		},
		components: {
			'add-client-button': AddClientButton,
			'delete': DeleteButton
		},
		events: {
			clientCreated() {
				this.getClients();
			},
			deleteClient(client) {
				this.deleteClient(client);
			}
		},
		methods: {
			getClients(limit = this.limit, offset = this.offset, search = this.search, ordering = this.ordering){
				const params = {limit, offset, search, ordering};
				return ClientsService.all(params).then(response => {
					this.clients = response.data.results;
					this.count = response.data.count;
					this.numberPages = Math.ceil(this.count / this.limit);
				});
			},
			getPrevious() {
				this.currentPage += 1;
				this.offset = (this.currentPage - 1) * this.limit;
				this.getClients();
			},
			getNext() {
				this.currentPage -= 1;
				this.offset = (this.currentPage - 1) * this.limit;
				this.getClients();
			},
			filter(query){
				this.currentPage = 1;
				this.offset = 0;
				this.getClients(this.limit, this.offset, query).then(()=> {
					if (this.count == 0) {
						this.no_client_message = 'il n\'y a aucun client correspondant à votre recherche'
					}
				});
			},
			sort(field){
				if (this.sorting == 'asc') {
					this.sorting = 'desc';
					this.ordering = field;
				} else {
					this.sorting = 'asc';
					this.ordering = `-${field}`;
				}
				this.getClients();
			},
			deleteClient(client){
				return ClientsService.delete(client).then(() => {
					Logging.success('Client supprimé avec succès');
					this.getClients();
				}).catch(() => {
					Logging.error('Impossible de supprimer ce client pour l\'instant. Retentez dans quelques instants ou contacter un administrateur')
				});
			}
		}
	};
</script>
