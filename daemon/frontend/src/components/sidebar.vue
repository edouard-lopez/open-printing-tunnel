<style scoped>
	.sidebar {
		z-index: 10;
		position: fixed;
		width: 100%;
		background-color: #424242;
		display: flex;
		justify-content: space-between;
		overflow: auto;
	}

	.sidebar-menu {
		list-style: none;
		padding: 0;
		margin: 0;
		display: flex;
	}

	.sidebar-item a {
		display: block;
		height: 64px;
		line-height: 64px;
		text-align: left;
		font-size: 32px;
		color: white;
		padding: 0 16px;
		text-decoration: none;
	}

	.sidebar-item span {
		display: none;
	}

	.sidebar-item.active,
	.sidebar-item:hover {
		background-color: #025aa5;
	}

	@media (min-width: 48em) {
		.sidebar {
			height: 100%;
			width: auto;
			flex-direction: column;
		}

		.sidebar-menu:first-child {
			margin-top: 1em;
		}

		.sidebar-menu:last-child {
			margin-bottom: 1em;
		}

		.sidebar-menu {
			display: block;
		}
	}
</style>
<template>
	<div class="sidebar">
		<ul class="sidebar-menu main">
			<li class="sidebar-item" v-link-active>
				<a v-link="{ path: '/sites/', activeClass: 'active' }" class="sidebar-link" title="Sites">
					<i class="fa fa-map-marker" aria-hidden="true"></i>
					<span class="sr-only">Sites</span>
				</a>
			</li>
		</ul>
		<ul class="sidebar-menu settings">
			<li class="sidebar-item" v-link-active>
				<a v-link="{ path: '/settings/', activeClass: 'active' }" class="sidebar-link" title="Settings">
					<i class="fa fa-cog"></i>
					<span class="sr-only">Settings</span>
				</a>
			</li>
			<li class="sidebar-item" v-link-active>
				<a v-link="{ path: '/logout/' }" class="sidebar-link" @click.stop.prevent="logout()" title="Sign-out">
					<i class="fa fa-sign-out"></i>
					<span class="sr-only">Signout</span>
				</a>
			</li>
		</ul>
	</div>
</template>
<script type="text/ecmascript-6">
	import auth from 'services/auth.service';
	import logging from 'services/logging.service';

	export default {
		methods: {
			logout(){
				auth.logout();
				logging.success(this.$t('login.logoutMessage'));
				this.$router.go('/');
			}
		}
	}
</script>
