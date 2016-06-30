<style scoped>
    i {
        line-height: 1.5;
    }
</style>
<template>
        <i class="fa pull-xs-right"
       v-if="ordering.includes(column)"
       v-bind:class="{ 'fa-sort-asc': this.sorting=='asc', 'fa-sort-desc': this.sorting=='desc' }">
    </i>
</template>
<script type="text/ecmascript-6">
    export default {
        props: ['column', 'ordering', 'sorting']
    }
</script>
