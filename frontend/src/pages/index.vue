<style>
    #landing-page  {
        height: 100vh;
        margin: 0px;
        padding: 0px;
        display: flex;
        flex-flow: column;
    }

    #login-bar {
        background-color: #424242;
        height: 38px;
        color: #F5F5F5;
    }

    #login-bar .nav-link {
        padding-left: 1em;
        padding-right: 1em;
        color: inherit;
    }

    #login-bar .nav-link {
        line-height: 38px;
    }

    #content {
        flex: 1 1 auto;
        text-align: center;
    }
    #content h1 {
        text-shadow: 2px 2px 0px #fff;
        margin-top: 10%;
    }
    #content img {
        margin: 0 auto;
    }

    #footer {
        color: #424242;
    }
    #footer a {
        color: inherit;
    }

</style>
<template>
    <div id="landing-page">
        <div id="login-bar">
            <div class="container">
                <nav class="nav nav-inline pull-xs-right">
                    <a class="nav-link bg-primary" v-link="{ path: '/clients/' }">
                        {{ $t('index.login') }}
                    </a>
                    <a class="nav-link" v-link="{ path: '/register/' }">
                        {{ $t('index.register') }}
                    </a>
                </nav>
            </div>
        </div>
        <main id="content">
            <div class="container">
                <h1>{{ $t('name') }}</h1>
                <!--<img src="/dist/images/coaxis-logo.png" width="100" height="100">-->
            </div>
        </main>
        <div id="footer">
            <div class="container p-t-1">
                <div class="row">
                    <div class="col-lg-12 text-xs-center">
                        <p>
                            &copy; <a href="http://coaxis-asp.fr/">Coaxis ASP</a>.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
