<template>
	<div id="containers-page">
		<div class="row">
			<div class="col-lg-12">
				<div class="card card-block">
					<div class="row">
						<div class="col-md-12">
							<h3>Conteneurs</h3>
						</div>
					</div>
					<div class="row">
						<div class="col-md-4">
							<div id="searchContainers">
								<div class="input-group">
                                    <span class="input-group-addon" id="search-addon">
                                        <i class="fa fa-search" aria-hidden="true"></i>
                                    </span>
									<input type="text" class="form-control" placeholder="search"
										   v-model="search" aria-describedby="search-addon"
										   @keyup="filter(search) | debounce 500">
								</div>
							</div>
						</div>
						<div class="col-md-4">
							<h2>
                                <span class="label label-info">
                                    <span v-if="selected.length>0"> {{selected.length}} / </span> {{count}} conteneur<span
										v-if="containers.length>1">s</span>
                                </span>
							</h2>
						</div>
						<div class="col-md-4 text-xs-right">
							<add-container-button></add-container-button>
						</div>
					</div>
					<div class="row">
						<div class="col-lg-12">
							<table class="table table-hover table-sm">
								<thead class="thead-inverse">
								<tr>
									<th @click="sort('name')">
										Nom
										<ordering-arrow column="name" :sorting="sorting" :ordering="ordering">
										</ordering-arrow>
									</th>
									<th @click="sort('adresse')">
										Adresse
										<ordering-arrow column="adresse" :sorting="sorting"
														:ordering="ordering">
										</ordering-arrow>
									</th>
									<th @click="sort('status')">
										Status
										<ordering-arrow column="status" :sorting="sorting"
														:ordering="ordering">
										</ordering-arrow>
									</th>
									<th @click="sort('company')">
										Société
										<ordering-arrow column="company" :sorting="sorting"
														:ordering="ordering">
										</ordering-arrow>
									</th>
									<th @click="sort('description')">
										Description
										<ordering-arrow column="description" :sorting="sorting"
														:ordering="ordering">
										</ordering-arrow>
									</th>
									<th>
										Actions
									</th>
								</tr>
								</thead>
								<tbody>
								<tr v-show="!containers.length">
									<td colspan="6">
										{{ no_container_message }}
									</td>
								</tr>
								<tr v-for="container in containers">
									<td>
										<a @click="openContainer(container.id)">
											{{ container.infos.name }}
										</a>
									</td>
									<td>
										<a @click="openContainer(container.id)">
											{{ container.infos.ipAddress }}
										</a>
									</td>
									<td>
										<span class="label"
											  v-bind:class="{
											  'label-danger': container.infos.status=='exited' || container.infos.status=='dead',
											  'label-warning': container.infos.status=='paused' || container.infos.status=='restarting',
											  'label-success': container.infos.status=='running' || container.infos.status=='created', }">
											{{ container.infos.status }}
										</span>

									</td>
									<td>
										{{ container.company }}
									</td>
									<td>
										{{ container.description }}
									</td>
									<td>
										<span class="btn btn-sm btn-danger" title="delete"
											  @click="deleteContainer(container)">
											<i class="fa fa-trash"></i>
										</span>
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
										@click="getNextContainers()">
									previous
								</button>
							</div>
							<div class="col-xs-4 text-xs-center" v-if="numberPages > 1">
								{{ currentPage }} / {{ numberPages }}
							</div>
							<div class="col-xs-4 text-xs-right">
								<button class="btn btn-primary btn-sm" v-if="count > limit"
										:disabled="(currentPage*limit >= count)"
										@click="getPreviousContainers()">
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
	import 'bootstrap/dist/js/umd/modal';
	import Containers from '../../services/containers';
	import AddContainerButton from '../../components/add-container-button';
	import OrderingArrow from '../../components/ordering-arrow';
	import logging from '../../services/logging';

	Containers.localStorage = localStorage;
	export default {
		data() {
			return {
				limit: 100,
				offset: 0,
				currentPage: 1,
				containers: [],
				selectedEntry: null,
				numberPages: 1,
				count: 0,
				sorting: 'asc',
				ordering: '-created',
				search: '',
				no_container_message: 'There is no container.',
				selectAll: false,
				selected: [],
			};
		},
		events: {
			containerCreated() {
				this.getContainers();
			}
		},
		ready(){
			this.getContainers();
		},
		components: {
			OrderingArrow,
			'add-container-button': AddContainerButton
		},
		methods: {
			getContainers(limit = this.limit, offset = this.offset, search = this.search, ordering = this.ordering){
				return Containers.all(limit, offset, search, ordering).then(response => {
					this.containers = response.data.results;
					this.count = response.data.count;
					this.numberPages = Math.ceil(this.count / this.limit);
				})
			},
			getPreviousContainers() {
				this.currentPage += 1;
				this.offset = (this.currentPage - 1) * this.limit;
				this.getContainers();
			},
			getNextContainers() {
				this.currentPage -= 1;
				this.offset = (this.currentPage - 1) * this.limit;
				this.getContainers();
			},
			filter(query){
				this.currentPage = 1;
				this.offset = 0;
				this.getContainers(this.limit, this.offset, query).then(()=> {
					if (this.count == 0) {
						this.no_container_message = 'there is no container matching your search'
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
				this.getContainers();
			},
			openContainer(id){
				this.$router.go(`/containers/${id}/`);
			},
			deleteContainer(container){
				Containers.delete(container)
						.then(() => {
							logging.success(this.$t('containers.delete.succeed'));
							this.getContainers();
						})
						.catch(() => {
							logging.error(this.$t('containers.delete.failed'))
						});
			}
		}
	};
</script>
