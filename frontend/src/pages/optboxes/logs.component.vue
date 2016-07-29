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
							@click="getOptboxes()"
					>
						<i class="fa fa-cube"> </i>
					</button>
				</li>
				<li class="btn-group" role="group" aria-label="Actions publiques">
					<button title="Status" role="button"
							class="btn btn-default btn-sm btn-action hide-btn-content hint--top-left"
							aria-label="Nettoyer le log"
							@click="data=[]"
					>
						<i class="fa fa-trash-o"> </i>
					</button>
				</li>
			</ul>
		</h2>
		<div class="row">
			<div class="col-xs-12 highlight">
				<pre class="stdout">
					<samp v-for="line in data.output" class="line">{{line}}</samp>
				</pre>
			</div>
		</div>
	</div>
</template>

<script type="text/ecmascript-6">
	import Optboxes from '../../services/optboxes';
	import Printers from '../../services/printers';
	import logging from '../../services/logging';

	export default {
		data() {
			return {
				data: {
					'output': [],
					'success': false
				}
			};
		},
		ready(){
			this.getOptboxes().then(()=> {
			});
		},
		methods: {
			getOptboxes(){
				return Optboxes.all().then(response => {
					this.data = response.data;
				}).catch(err => {
					console.error(err)
				});
			},
			getPrinters(){
				return Printers.all().then(response => {
					console.log(response)
					this.data = response.data;
				}).catch(err => {
					console.error(err)
				});
			},
		}
	}
</script>
