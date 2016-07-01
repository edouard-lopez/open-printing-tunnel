<style scoped>
    .card-block {
        min-height: 97vh;
    }

    tr {
        cursor: pointer;
    }

    th {
        text-transform: uppercase;
        font-size: .9em;
    }

    input[type=checkbox] {
        vertical-align: middle;
        position: relative;
        bottom: 1px;
    }
</style>
<template>
    <div id="incidents-page">
        <div class="row">
            <div class="col-lg-12">
                <div class="card card-block">
                    <div class="row">
                        <div class="col-md-12">
                            <h3>Incidents</h3>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-4">
                            <div id="searchIncidents">
                                <div class="input-group">
                                    <span class="input-group-addon" id="search-addon">
                                        <i class="fa fa-search" aria-hidden="true"></i>
                                    </span>
                                    <input type="text" class="form-control" placeholder="search"
                                           v-model="search" aria-describedby="search-addon"
                                           @keyup="filterEntry(search) | debounce 500">
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <form class="form-inline" id="changeStatusForm" v-on:submit.prevent="confirmUpdateSelected">
                                <div class="form-group">
                                    <label class="sr-only" for="status">Status</label>
                                    <div class="input-group">
                                        <div class="input-group-addon">Change Status</div>
                                        <select class="form-control" id="status" v-model="newStatus">
                                            <option value="1">In progress</option>
                                            <option value="2">Solved</option>
                                            <option value="3">Closed</option>
                                        </select>
                                    </div>
                                </div>
                                <button type="submit" class="btn btn-primary"
                                        :disabled="selected.length==0 || !this.newStatus">update
                                </button>
                            </form>
                        </div>
                        <div class="col-md-4 text-xs-right">
                            <h2>

                                <span class="label label-danger">
                                    <span v-if="selected.length>0"> {{selected.length}} / </span> {{count}} incident<span
                                        v-if="incidents.length>1">s</span>
                                </span>
                            </h2>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-lg-12">
                            <table class="table table-hover table-sm">
                                <thead class="thead-inverse">
                                <tr>
                                    <th>
                                        <input type="checkbox" @click="toggleAll" v-model="selectAll">
                                    </th>
                                    <!--<th>-->
                                    <!--Driver version-->
                                    <!--</th>-->
                                    <th @click="sort('error_code')">
                                        Last error code
                                        <ordering-arrow column="error_code" :sorting="sorting" :ordering="ordering">
                                        </ordering-arrow>
                                    </th>
                                    <th @click="sort('error_message')">
                                        Last error message
                                        <ordering-arrow column="error_message" :sorting="sorting"
                                                        :ordering="ordering">
                                        </ordering-arrow>
                                    </th>
                                    <th @click="sort('equipment')" class="text-xs-center">
                                        Equipment
                                        <ordering-arrow column="equipment" :sorting="sorting" :ordering="ordering">
                                        </ordering-arrow>
                                    </th>
                                    <th @click="sort('created')" class="text-xs-center">
                                        Last error date
                                        <ordering-arrow column="created" :sorting="sorting" :ordering="ordering">
                                        </ordering-arrow>
                                    </th>
                                    <th class="text-xs-right">
                                        Status
                                    </th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr v-show="!incidents.length">
                                    <td colspan="6">
                                        {{ no_incident_message }}
                                    </td>
                                </tr>
                                <tr v-for="incident in incidents"
                                    v-bind:class="{ 'table-danger': incident.status==0,  'table-warning': incident.status==1,'table-success': incident.status==2 || incident.status==3,  }">
                                    <td>
                                        <input type="checkbox" value="{{incident.id}}" v-model="selected">
                                    </td>
                                    <!--<td>{{ incident.driver_version }}</td>-->
                                    <td @click="openIncident(incident.id)">
                                        {{ incident.error_code }}
                                    </td>
                                    <td @click="openIncident(incident.id)">{{ incident.error_message }}</td>
                                    <td @click="openIncident(incident.id)" class="text-xs-center">{{ incident.equipment
                                        }}
                                    </td>
                                    <td @click="openIncident(incident.id)" class="text-xs-center">{{ incident.created |
                                        moment }}
                                    </td>
                                    <td @click="openIncident(incident.id)" class="text-xs-right">{{ incident.status |
                                        displayStatus }}
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
                                        @click="getNextIncidents()">
                                    previous
                                </button>
                            </div>
                            <div class="col-xs-4 text-xs-center" v-if="numberPages > 1">
                                {{ currentPage }} / {{ numberPages }}
                            </div>
                            <div class="col-xs-4 text-xs-right">
                                <button class="btn btn-primary btn-sm" v-if="count > limit"
                                        :disabled="(currentPage*limit >= count)"
                                        @click="getPreviousIncidents()">
                                    next
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal -->
        <div class="modal fade" id="confirmModal" tabindex="-1" role="dialog" aria-labelledby="confirmModalLabel"
             aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                        <h4 class="modal-title" id="confirmModalLabel">Confirm status change</h4>
                    </div>
                    <div class="modal-body">
                        Are you sure you want to change the status of the <span v-if="selected.length>1">{{ selected.length}}</span>
                        selected incident<span v-if="selected.length>1">s</span>?
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" @click="updateSelected">Change status</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script type="text/ecmascript-6">
    import 'bootstrap/dist/js/umd/modal';
    import Incidents from '../services/incidents';
    import OrderingArrow from '../components/ordering-arrow';
    import moment from 'moment';
    import logging from '../services/logging';

    Incidents.localStorage = localStorage;
    export default {
        data() {
            return {
                limit: 100,
                offset: 0,
                currentPage: 1,
                incidents: [],
                selectedEntry: null,
                numberPages: 1,
                count: 0,
                clicks: 0,
                sorting: 'asc',
                ordering: '-created',
                search: '',
                no_incident_message: 'loading....',
                selectAll: false,
                selected: [],
                newStatus: null
            };
        },
        ready(){
            this.getIncidents().then(()=> {
                if (this.count == 0) {
                    this.no_incident_message = 'there is no incident'
                }
            });
        },
        components: {
            OrderingArrow
        },
        methods: {
            moment: function (date) {
                return moment(date);
            },
            getIncidents(limit = this.limit, offset = this.offset, search = this.search, ordering = this.ordering){
                return Incidents.all(limit, offset, search, ordering).then(response => {
                    this.incidents = response.data.results;
                    this.count = response.data.count;
                    this.numberPages = Math.ceil(this.count / this.limit);
                })
            },
            getPreviousIncidents() {
                this.currentPage += 1;
                this.offset = (this.currentPage - 1) * this.limit;
                this.getIncidents();
            },
            getNextIncidents() {
                this.currentPage -= 1;
                this.offset = (this.currentPage - 1) * this.limit;
                this.getIncidents();
            },
            filterEntry(query){
                this.currentPage = 1;
                this.offset = 0;
                this.getIncidents(this.limit, this.offset, query).then(()=> {
                    if (this.count == 0) {
                        this.no_incident_message = 'there is no incident matching your search'
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
                this.getIncidents();
            },
            toggleAll(){
                this.selectAll = !this.selectAll;
                this.selected = [];
                if (this.selectAll) {
                    this.incidents.forEach(incident => {
                        this.selected.push(`${incident.id}`)
                    });
                }
            },
            confirmUpdateSelected(){
                $('#confirmModal').modal('show');
            },
            updateSelected(){
                const ids = this.selected.map(incidentId => {
                    return parseInt(incidentId)
                });
                Incidents.changeStatus(ids, this.newStatus)
                        .then(updatedIncidents => {
                            logging.success('Selected items have been updated');
                        })
                        .catch(() => {
                            logging.error('Cannot update selected elements, try again in a moment');
                        });
                $('#confirmModal').modal('hide');
            },
            openIncident(id){
                this.$router.go(`/incidents/${id}/`);
            }
        },
        filters: {
            moment: function (date) {
                return moment(date).format('MMMM Do YYYY, h:mm');
            },
            displayStatus: function (statusId) {
                const status = {
                    0: 'New',
                    1: 'In progress',
                    2: 'Solved',
                    3: 'Closed'
                };
                return status[statusId];
            }
        }
    };
</script>

