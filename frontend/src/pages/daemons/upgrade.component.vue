<template>
	<div class="row xx-large">
		<div class="col-xs-12">
			<span v-if="!upgrading" class="tag tag-lg tag-info">
				{{currentVersion}}
			</span>
			<span v-if="upgrading">
				<span class="tag tag-warning tag-lg">
					Mise à jour…
					<i class="fa fa-refresh fa-spin fa-fw"></i>
				</span>
			</span>
			<span v-if="!upgrading" @click="toggleVersions()"
				  class="tag tag-lg hint--top text-info"
				  aria-label="Afficher les versions disponibles">
				<i class="fa fa-fw text-muted"
				   v-bind:class="{ 'fa-eye': !showVersions, 'fa-eye-slash': showVersions}"></i>
		</span>

			<ul v-if="showVersions" class="list-inline">
				<li v-for="version in availableVersions" class="list-inline-item">
					<small @click="upgrade(container, version)"
						   aria-label="basculer en version {{version}}"
						   class="version tag tag-warning hint--top">
						{{version}}
					</small>
				</li>
			</ul>
		</div>
	</div>
</template>
<style>
	.version {
		font-size: .9rem;
		font-weight: normal;
		cursor: pointer;
	}
</style>
<script type="text/ecmascript-6">
	import HTTP from 'services/http.service';
	import Logging from 'services/logging.service';
	import actions from 'vuex/actions';
	import getters from 'vuex/getters';

	const VersionsService = HTTP('daemon-versions', localStorage);
	const ContainersService = HTTP('containers', localStorage);

	export default {
		data() {
			return {
				showVersions: false,
				upgrading: false,
				availableVersions: []
			}
		},
		props: {
			container: {
				type: Object, default: {
					id: null, container_info: {
						State: {status: 'paused'},
						Config: {Image: null}
					}
				}
			},
		},
		ready(){
			this.listVersions();
		},
		computed: {
			status: function () {
				return this.container.container_info.State.Status;
			},
			currentVersion: function () {
				let image = this.container.container_info.Config.Image;
				return image.split('/').slice(-1).pop().split(':')[1];
			}
		},
		methods: {
			listVersions() {
				return VersionsService.all().then(response => {
					this.availableVersions = response.data;
				});
			},
			toggleVersions() {
				return this.showVersions = !this.showVersions;
			},
			upgrade(container, version){
				this.toggleVersions();
				this.upgrading = true;
				ContainersService.create({id: container.id, action: 'upgrade', version}).then(response => {
					this.fetchDaemon(response.data.id);
					this.upgrading = false;
					Logging.success('Daemon mise à jour en version `'+ version + '`');
				}).catch(() => {
					Logging.error('Impossible de mettre à jour le daemon.')
				});
			}
		},
		vuex: {
			actions: {
				fetchDaemon: actions.fetchDaemon
			}
		}
	}
</script>
