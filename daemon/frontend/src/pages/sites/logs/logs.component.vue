<style>
	.highlight {
		margin: 1rem -1rem;
		background-color: #f7f7f9;
	}

	.highlight {
		padding: 1.5rem;
		margin-right: 0;
		margin-left: 0;
	}

	.line {
		display: block;
	}
</style>
<template>
	<div>
		<h2 class="row" id="cnc">
						<span class="col-md-8">
							Centre de Contrôle
						</span>
			<ul class="btn-toolbar pull-right" role="toolbar"
				aria-label="Toolbar with button groups">
				<li class="btn-group" role="group" aria-label="Actions publiques">
					<button title="Status" role="button"
							class="btn btn-info btn-sm btn-action hide-btn-content hint--top"
							aria-label="Lister les canaux"
							@click="getPrinters()"
					>
						<i class="fa fa-print"> </i>
					</button>
					<button title="Status" role="button"
							class="btn btn-warning btn-sm btn-action hide-btn-content hint--top"
							aria-label="Lister les boitiers"
							@click="getSites()"
					>
						<i class="fa fa-cube"> </i>
					</button>
				</li>
				<li class="btn-group" role="group" aria-label="Actions publiques">
					<button title="Status" role="button"
							class="btn btn-default btn-sm btn-action hide-btn-content hint--top-left"
							aria-label="Nettoyer le log"
							@click="stdout=[]"
					>
						<i class="fa fa-trash-o"> </i>
					</button>
				</li>
			</ul>
		</h2>
		<div class="row">
			<div class="col-xs-12 highlight">
				<pre class="stdout"><samp v-for="line in stdout" class="line">{{line | json }}</samp></pre>
			</div>
		</div>
	</div>
</template>

<script type="text/ecmascript-6">
	import logging from 'services/logging.service';
	import http from 'services/http.service';

	const sites = http('sites', localStorage);
	const printers = http('printers', localStorage);

	export default {
		data() {
			return {
				data: {
					'data': [],
					'success': false
				},
				stdout: {}
			};
		},
		methods: {
			getSites(){
				sites.all().then((response)=> {
					this.data = response.data;
					this.stdout = response.data.results;
				}).catch(err => {
					console.error(err)
				});
			},
			getPrinters(){
				printers.all().then((response)=> {
					this.data = response.data;
					this.stdout = response.data.results;
				}).catch(err => {
					console.error(err)
				});
			},
		},
		events: {
			'log-response': function (response) {
				if (!Array.isArray(response.results)) {
					response.results = [response.results];
				}
				this.stdout = response.results;
			}
		}
	}
</script>
