<style scoped>
	.table thead th, .table td, .table th {
		border: none;
	}
</style>
<template>
	<div id="container-page">
		<div class="row">
			<div class="col-md-8">
				<div class="card">
					<h5 class="card-header">
						<i class="fa fa-map-marker" aria-hidden="true"></i> Sites
					</h5>
					<div class="card-block">
						<table class="table table-hover table-sm">
							<thead class="thead-inverse">
							</thead>
							<tbody>
							<tr v-for="site in client.sites">
								<td>
									<a v-link="{ name: 'sites', params: { id: client.id }}">
										{{ site.id }}
									</a>
								</td>
								<td>
									{{ site.hostname }}
								</td>
								<td class="text-xs-right">
									<span class="btn btn-sm btn-danger" title="delete">
										<i class="fa fa-trash"></i>
									</span>
								</td>
							</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>
			<div class="col-md-4">
				<div class="card">
					<h5 class="card-header">
						Status des services
					</h5>
					<div class="card-block">
						<h3>
							<span class="tag tag-lg"
								  v-bind:class="{ 'tag-danger': client.container_info.State.Status=='exited', 'tag-warning': client.container_info.State.Status=='paused', 'tag-success': client.container_info.State.Status=='running'}">
                                {{client.container_info.State.Status }}
							</span>
						</h3>
					</div>
				</div>
				<div class="card">
					<h5 class="card-header">
						<i class="fa fa-home" aria-hidden="true"></i>
						Société
					</h5>
					<div class="card-block">
						<p class="card-text">
							{{ client.company.name }}
						</p>
					</div>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="col-xs-12">
				<div class="card">
					<h6 class="card-header">
						<i class="fa fa-info-circle" aria-hidden="true"></i> Client id : {{client.id}}
						<span class="pull-xs-right">{{ client.created | moment }}</span>
					</h6>
					<div class="card-block">
						<p class="card-text">
							{{client.error_message}}
						<pre>{{client | json 4 }}</pre>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	import ClientsService from '../../services/containers.service';

	import logging from '../../services/logging.service';
	import moment from 'moment';

	ClientsService.localStorage = localStorage;
	export default {
		data() {
			return {
				client: null
			};
		},
		ready(){
			ClientsService.get(this.$route.params.id).then(client => {
				this.client = client;
			});
		},
		filters: {
			moment: function (date) {
				return moment(date).format('MMMM Do YYYY, h:mm:ss');
			},
		}
	};
</script>

