<template>
	<div id="printers-page">
		<div class="row">
			<div class="col-lg-12">
				<div class="card card-block">
					<h2 class="row">
						<span class="col-md-8">
							<span>Printers</span>
						</span>
						<span class="col-md-4 text-xs-right">
							<span class="label label-info">
								<span v-if="printers.length>0"> {{printers.length}} / </span> {{count}} printer<span
									v-if="printers.length>1">s</span>
							</span>
						</span>
					</h2>
					<div class="row">
						<div class="col-md-4">
							<h2>
								<button class="btn btn-success" @click="createPrinter()">
									<i class="fa fa-plus-circle"></i>
									Ajouter un hôte
								</button>
							</h2>
						</div>
					</div>
					<div class="row">
						<div id="accordion" role="tablist" aria-multiselectable="true">
							<div v-for="printer in printers" class="panel panel-default">
								<div class="panel-heading" role="tab" id="heading-host-{{printer.location}}">
									<h5 class="panel-title"
										data-toggle="collapse"
										data-parent="#accordion"
										href="#host-{{printer.location}}"
										aria-expanded="false"
										aria-controls="host-{{printer.location}}"
									>
										<div class="row">
											<span class="col-md-6">
												<span class="hint--top-right" aria-label="Tooltip on top">
													<i class="tunnel-status fa fa-check text-muted"> </i>
												</span>
												<span class="tunnel-name">
													<b>{{printer.location}}</b>
												</span>
												<span class="divider"> – </span>
												<span class="tunnel-fqdn text-muted">{{printer.address}}</span>
											</span>

											<div class="col-md-6">
												<ul class="btn-toolbar pull-right" role="toolbar"
													aria-label="Toolbar with button groups">
													<li class="btn-group" role="group" aria-label="Actions publiques">
														<button title="Status" role="button"
																class="btn btn-info btn-sm btn-action hide-btn-content hint--top"
																data-name="{printer.location}}"
																data-action="status"
																data-redirect="false"
																data-href="./"
																data-target="#modal-status"
																data-placement="left"
																data-toggle="tooltip"
																data-html="true"
																aria-label="Status"
														>
															<i class="fa fa-info"> </i>
														</button>
														<button
																role="button"
																class="btn btn-success btn-sm btn-action hide-btn-content hint--top"
																data-name="{printer.location}}"
																data-action="add-channel"
																data-redirect="false"
																data-href="./"
																data-target="#modal-add-channel"
																data-placement="left"
																data-toggle="tooltip"
																data-html="true"
																aria-label="Ajouter un *canal*"
														>
															<i class="fa fa-plus-circle"> </i>
														</button>
														<button
																role="button"
																class="btn btn-primary btn-sm btn-action hide-btn-content hint--top"
																data-name="{printer.location}}"
																data-action="add-bulk-channels"
																data-redirect="false"
																data-href="./"
																data-target="#modal-add-bulk-channels"
																data-placement="left"
																data-toggle="tooltip"
																data-html="true"
																aria-label="Ajouter des *canaux* par lot"
														>
															<i class="fa fa-print"> </i>
														</button>
														<button
																role="button"
																class="btn btn-default btn-sm btn-action hide-btn-content hint--top"
																data-name="{printer.location}}"
																data-action="link"
																data-redirect="true"
																data-href="./home/getScript/PORTS/eyJyZW1vdGVIb3N0IjoiMTcyLjE4LjAuMSIsInJlbW90ZVBvcnQiOjIyLCJjaGFubmVscyI6W3sibG9jYWxIb3N0IjoiKiIsImxvY2FsUG9ydCI6IjkxMDIiLCJyZW1vdGVIb3N0IjoiMS4yLjMuNCIsInJlbW90ZVBvcnQiOiI5MTAwIiwiY29tbWVudCI6ImFrZW1hIn1dLCJzaXRlIjoiYWxiYW4taG9tZSJ9"
																data-target="#modal-link"
																data-placement="left"
																data-toggle="tooltip"
																data-html="true"
																aria-label="script d'installation d'imprimante"
														>
															<i class="fa fa-comment"> </i>
														</button>
													</li>
													<li class="btn-group" role="group"
														aria-label="Actions d'administration">
														<button
																role="button"
																class="btn btn-warning btn-sm btn-action restart hide-btn-content hint--top"
																data-name="{printer.location}}"
																data-action="restart"
																data-redirect="false"
																data-href="./"
																data-target="#modal-restart"
																data-placement="left"
																data-toggle="tooltip"
																data-html="true"
																aria-label="Redémarrer"
														>
															<i class="fa fa-refresh"> </i>
														</button>
														<button
																role="button"
																class="btn btn-success btn-sm btn-action hide-btn-content hint--top"
																data-name="{printer.location}}"
																data-action="start"
																data-redirect="false"
																data-href="./"
																data-target="#modal-start"
																data-placement="left"
																data-toggle="tooltip"
																data-html="true"
																aria-label="Démarrer"
														>
															<i class="fa fa-play"> </i>
														</button>
														<button
																role="button"
																class="btn btn-danger btn-sm btn-action hide-btn-content hint--top"
																data-name="{printer.location}}"
																data-action="stop"
																data-redirect="false"
																data-href="./"
																data-target="#modal-stop"
																data-placement="left"
																data-toggle="tooltip"
																data-html="true"
																aria-label="Arrêter"
														>
															<i class="fa fa-stop"> </i>
														</button>
													</li>
													<li class="btn-group" role="group"
														aria-label="Actions non-réversibles">
														<button
																role="button"
																class="btn btn-link btn-sm btn-action hide-btn-content hint--top-left"
																data-name="{printer.location}}"
																data-action="remove-host"
																data-redirect="false"
																data-href="./"
																data-target="#modal-remove-host"
																data-placement="left"
																data-toggle="tooltip"
																data-html="true"
																aria-label="Supprimer cet *hôte*"
														>
															<i class="fa fa-trash text-danger"> </i>
														</button>
													</li>
												</ul>

											</div>
										</div>
									</h5>
								</div>
								<div id="host-{{printer.location}}" class="panel-collapse collapse" role="tabpanel"
									 aria-labelledby="heading-host-{{printer.location}}">
									Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry
									richardson ad squid. 3 wolf moon officia aute, non cupidatat skateboard dolor
									brunch. Food truck quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor, sunt
									aliqua put a bird on it squid single-origin coffee nulla assumenda shoreditch et.
									Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente
									ea proident. Ad vegan excepteur butcher vice lomo. Leggings occaecat craft beer
									farm-to-table, raw denim aesthetic synth nesciunt you probably haven't heard of them
									accusamus labore sustainable VHS.
								</div>
							</div>
						</div>
					</div>
					<div class="row m-t-1">
						<div class="paginate">
							<div class="col-xs-4 text-xs-left">
								<button class="btn btn-primary btn-sm" v-if="count > limit"
										:disabled="(currentPage===1)"
										@click="getNextPrinters()">
									previous
								</button>
							</div>
							<div class="col-xs-4 text-xs-center" v-if="numberPages > 1">
								{{ currentPage }} / {{ numberPages }}
							</div>
							<div class="col-xs-4 text-xs-right">
								<button class="btn btn-primary btn-sm" v-if="count > limit"
										:disabled="(currentPage*limit >= count)"
										@click="getPreviousPrinters()">
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
	import Printers from '../services/printers';
	import OrderingArrow from '../components/ordering-arrow';
	import moment from 'moment';
	import logging from '../services/logging';
	import 'bootstrap/dist/js/umd/collapse.js';

	Printers.localStorage = localStorage;
	export default {
		data() {
			return {
				count: 1,
				ordering: '-created',
				sorting: 'asc',
				no_container_message: 'loading…',
				printers: [
					{
						id: 1,
						location: 'salle de réunion (Cenon)',
						opt_box: '049fed91-6880-4c08-8cb2-21e8579d4543',
						address: '10.1.4.1'
					},
				]
			};
		},
		ready(){
			// this.getPrinters().then(()=> {
			// 	if (this.count == 0) {
			// 		this.no_printer_message = 'there is no printer'
			// 	}
			// });
		},
		components: {
			OrderingArrow
		},
		methods: {
			moment: function (date) {
				return moment(date);
			},
			getPrinters(ordering = this.ordering){
				return Printers.all(ordering).then(response => {
					this.printers = response.data.results;
					this.count = response.data.count;
					this.numberPages = Math.ceil(this.count / this.limit);
				})
			},
			sort(field){
				if (this.sorting == 'asc') {
					this.sorting = 'desc';
					this.ordering = field;
				} else {
					this.sorting = 'asc';
					this.ordering = `-${field}`;
				}
				this.getPrinters();
			},
			openPrinter(id){
				this.$router.go(`/printers/${id}/`);
			},
			createPrinter(printer){
				this.$router.go(`/printers/create/`);
			},
			deletePrinter(printer){
				Printers.delete(printer)
						.then(() => {
							logging.success(this.$t('printers.delete.succeed'));
							this.getPrinters();
						})
						.catch(() => {
							logging.error(this.$t('printers.delete.failed'))
						});
			}
		}
	}
</script>
