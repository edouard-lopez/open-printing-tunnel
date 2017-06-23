<template>
	<div id="daemons-page">
		<div class="row">
			<div class="col-lg-12">
				<div class="card card-block">
					<div class="row">
						<div class="col-md-12">
							<h3>Daemons</h3>
						</div>
					</div>
					<div class="row">
						<div class="col-md-4">
							<div id="searchDaemons">
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
                                    <span v-if="selected.length>0"> {{selected.length}} / </span> {{count}} daemon<span
										v-if="daemons.length>1">s</span>
                                </span>
							</h2>
						</div>
						<div class="col-md-4 text-xs-right">
							<add-daemon-button></add-daemon-button>
						</div>
					</div>
					<div class="row">
						<div class="col-lg-12">
							<table class="table table-hover table-sm">
								<thead class="thead-inverse">
								<tr>
									<th>
										ID
									</th>
									<th>
										IP
									</th>
									<th>
										Subnet
									</th>
									<th>
										Gateway
									</th>
									<th>
										Vlan
									</th>
									<th>
										Hostname
									</th>
									<th>
										Client
									</th>
									<th class="text-xs-right">
										Actions
									</th>
								</tr>
								</thead>
								<tbody>
								<tr v-show="!daemons.length">
									<td colspan="6">
										{{ no_daemon_message }}
									</td>
								</tr>
								<tr v-for="daemon in daemons">
									<td>
										<a v-link="{ name: 'daemons', params: { id: daemon.id }}">
											{{ daemon.id }}
										</a>
									</td>
									<td>
										{{ daemon.ip }}
									</td>
									<td>
										{{ daemon.subnet }}
									</td>
									<td>
										{{ daemon.gateway }}
									</td>
									<td>
										{{ daemon.vlan }}
									</td>
									<td>
										<a v-bind:href="daemon.hostname" target="_blank">{{ daemon.hostname }}</a>
									</td>
									<td>
										{{ daemon.client.name }}
									</td>
									<td class="text-xs-right">
										<delete :promise="deleteDaemon" :object="daemon" class="btn-sm">
											<span slot="title">Supprimer le daemon</span>
											<span slot="body">Confirmer la suppression du daemon et des tunnels associés.</span>
											<span slot="in-progress">Suppression en cours</span>
											<span slot="action">Supprimer le daemon</span>
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
	import AddDaemonButton from './add-daemon-button';
	import DeleteButton from 'components/delete-button';
	import HTTP from 'services/http.service';
	import Logging from 'services/logging.service';

	const DaemonsService = HTTP('daemons', localStorage);

	export default {
		data() {
			return {
				limit: 500,
				offset: 0,
				currentPage: 1,
				selectedEntry: null,
				numberPages: 1,
				count: 0,
				sorting: 'asc',
				ordering: '-created',
				search: '',
				no_daemon_message: 'There is no daemon.',
				selectAll: false,
				selected: [],
				daemons: []
			};
		},
		ready(){
			this.getDaemons();
		},
		components: {
			'add-daemon-button': AddDaemonButton,
			'delete': DeleteButton
		},
		events: {
			daemonCreated() {
				this.getDaemons();
			},
			deleteDaemon(daemon) {
				this.deleteDaemon(daemon);
			}
		},
		methods: {
			getDaemons(limit = this.limit, offset = this.offset, search = this.search, ordering = this.ordering){
				const params = {limit, offset, search, ordering};
				return DaemonsService.all(params).then(response => {
					this.daemons = response.data.results;
					this.count = response.data.count;
					this.numberPages = Math.ceil(this.count / this.limit);
				});
			},
			getPrevious() {
				this.currentPage += 1;
				this.offset = (this.currentPage - 1) * this.limit;
				this.getDaemons();
			},
			getNext() {
				this.currentPage -= 1;
				this.offset = (this.currentPage - 1) * this.limit;
				this.getDaemons();
			},
			filter(query){
				this.currentPage = 1;
				this.offset = 0;
				this.getDaemons(this.limit, this.offset, query).then(() => {
					if (this.count == 0) {
						this.no_daemon_message = 'il n\'y a aucun daemon correspondant à votre recherche'
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
				this.getDaemons();
			},
			deleteDaemon(daemon){
				return DaemonsService.delete(daemon).then(() => {
					Logging.success('Daemon supprimé avec succès');
					this.getDaemons();
				}).catch(() => {
					Logging.error('Impossible de supprimer ce daemon pour l\'instant. Retentez dans quelques instants ou contacter un administrateur')
				});
			}
		}
	};
</script>
