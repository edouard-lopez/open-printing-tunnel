# Troubleshooting

## Debug _Makefile_
To enable debug mode with the makefile, run the command with the `-d` flag:

    sudo make -d install

## Debug _init.d_ service

To debug the service you will need to export the `DEBUG` variable with a non-empty value and tell `sudo` to preserve environment with `-e` or `--preserve-env` option. So the exported variable is available to `sudo` context.

    export DEBUG="true"
    sudo -E /etc/init.d/mast status
    unset DEBUG # restore normal debug mode

**N.B.:** using `-E` option may have some [security implications](https://stackoverflow.com/questions/8633461/how-to-keep-environment-variables-when-using-sudo#comment10726355_8636711), **never use it in production code!**

## _perl: warning: Setting locale failed._

If you got this perl related warning, the actual issue is with SSH and locale forwarding (see below).

    perl: warning: Setting locale failed.
    perl: warning: Please check that your locale settings:
        LANGUAGE = "en_US:en",
        LC_ALL = (unset),
        LC_PAPER = "fr_FR.UTF-8",
        LC_ADDRESS = "fr_FR.UTF-8",
        LC_MONETARY = "fr_FR.UTF-8",
        LC_NUMERIC = "fr_FR.UTF-8",
        LC_TELEPHONE = "fr_FR.UTF-8",
        LC_IDENTIFICATION = "fr_FR.UTF-8",
        LC_MEASUREMENT = "fr_FR.UTF-8",
        LC_TIME = "fr_FR.UTF-8",
        LC_NAME = "fr_FR.UTF-8",
        LANG = "en_US.UTF-8"
        are supported and installed on your system.
    perl: warning: Falling back to the standard locale ("C").

### Solution
The solution is to modify the server configuration in order to refuse locale forwarding:

> Stop accepting locale on the server. Do not accept the locale environment variable from your local machine to the server. 
> You can comment out the `AcceptEnv LANG LC_*` line in the remote _/etc/ssh/sshd_config_ file.

The file _/etc/ssh/sshd_config_ should then look like:

    # AcceptEnv LANG LC_*

For more information refer to [Locale variables have no effect in remote shell (perl: warning: Setting locale failed.)](http://askubuntu.com/a/144448/22343).