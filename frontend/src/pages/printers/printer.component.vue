<style>
	.btn-toolbar .btn-group {
		float: right;
	}
</style>
<template>
		<div class="row btn-toolbar" id="{{ optbox.name }}-{{ printer.hostnane }}"
			 role="toolbar" aria-label="Toolbar with button groups">
			<div class="col-md-8" role="group" aria-label="Actions publiques">
				<a href="http://{{printer.hostname}}">{{ printer.hostname }}</a>
				<span>on port <span class="port">{{ printer.port }}</span></span>
				<span class="description text-muted">{{ printer.description }}</span>
				<i class="text-muted">{{ printer.forward }}</i>
			</div>
			<div class="col-md-4">
				<ul class="btn-toolbar">
					<li class="btn-group" role="group" aria-label="Actions non-réversibles">
						<button aria-label="Supprimer cette *imprimante*"
								role="button"
								class="btn btn-link btn-sm btn-action hide-btn-content hint--top-left"
								@click="remove(printer.id)"
						>
							<i class="fa fa-trash-o text-danger"> </i>
						</button>
					</li>
					<li class="btn-group" role="group" aria-label="Actions d'administrations">
						<button aria-label="script d'installation d'imprimante"
								role="button"
								class="btn btn-default btn-sm btn-action hide-btn-content hint--top"
								@click="link(optbox.name)"
						>
							<i class="fa fa-comment"> </i>
						</button>
					</li>
				</ul>			</div>
		</div>
</template>
<script type="text/ecmascript-6">
	import logging from '../../services/logging';
	import resource from 'pilou';

	const printer = resource('printers', {
				get: '/daemon/${resource}/${optbox}',
				delete: '/daemon/${resource}/${optbox}'
			}
	);

	export default {
		data() {
			return {
			};
		},
		props: {
			printer: {type: Object, required: true},
			optbox: {type: Object, required: true}
		},
		methods: {
			remove(channel_id) {
				printer.delete({'optbox': optbox.name}, {'id': channel_id}).then((response) => {
					console.log(this.printer.channels[channel_id])
				})
			}
		}
	}
</script>
