<template>
	<div>
		<button data-e2e="add-site" type="button" class="btn btn-success" data-toggle="modal"
				data-target="#site-modal">
			<i class="fa fa-plus-circle"></i>
			Ajouter un site
		</button>
		<div class="modal fade" id="site-modal" data-e2e="add-site-modal" tabindex="-1" role="dialog" aria-labelledby="action-label"
			 aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content text-xs-left">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
						<h4 class="modal-title" id="action-label">Créer un site</h4>
					</div>
					<div class="modal-body">
						<form @submit="createSite()">
							<fieldset class="form-group">
								<label for="id">Nom du site <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="id"
									   placeholder="ex. client-un" v-model="site.id" data-e2e="add-site:name"/>
							</fieldset>
							<fieldset class="form-group">
								<label for="hostname">Hôte distant <span class="text-danger">*</span></label>

								<input type="text" class="form-control" id="hostname"
									   placeholder="ex. 10.0.254.1" v-model="site.hostname" data-e2e="add-site:hostname"/>
							</fieldset>
						</form>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-dismiss="modal">Annuler</button>
						<button type="button" class="btn btn-primary" v-on:click.stop.prevent="createSite"
								:disabled="!formIsValid" data-e2e="add-site:submit">
							<span v-if="!formSubmitted">Créer</span>
							<span v-else><i class="fa fa-spinner fa-pulse fa-fw"></i> Création en cours</span>
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
import http from 'services/http.service';
import logging from 'services/logging.service';
import actions from 'vuex/actions';
import getters from 'vuex/getters';

const sites = http('sites', localStorage);

export default {
  data() {
    return {
      site: {
        id: '',
        hostname: ''
      },
      formSubmitted: false
    };
  },
  methods: {
    createSite() {
      this.formSubmitted = true;

      sites
        .create(this.site)
        .then(() => {
          $('#site-modal').modal('hide');
          this.formSubmitted = false;
          this.getSites();
        })
        .catch(() => {
          console.error(err);
          this.formSubmitted = false;
          logging.error("Impossible d'ajouter le site");
        });
    }
  },
  computed: {
    formIsValid() {
      return !!(this.site.id && this.site.hostname && !this.formSubmitted);
    }
  },
  vuex: {
    actions: {
      getSites: actions.getSites
    },
    getters: {
      sites: getters.retrieveSites
    }
  }
};
</script>
