#!/usr/bin/env bats

setup() {
    alias mast-utils="$BATS_TEST_DIRNAME/../makefile"
    export NO_ERROR=0
    export MAKEFILE_ERROR=2
    export status
    export lines
}

teardown() {
    unalias mast-utils
    unset NO_ERROR
    unset MAKEFILE_ERROR
}

remove_ansi() {  # http://superuser.com/a/380778/174465
    echo "$@" | sed -r 's/\x1b\[[^@-~]*[@-~]//g'
}

@test "should raise error without NAME parameter" {
    run mast-utils add-channel

    [[ "$status" == "$MAKEFILE_ERROR" ]]
    [[ $(remove_ansi ${lines[1]}) == "NAME missing (see 'mast-utils list-host')" ]]
}

@test "should raise error with NAME=none" {
    run mast-utils add-channel NAME=none

    [[ "$status" == "$MAKEFILE_ERROR" ]]
    [[ $(remove_ansi ${lines[1]}) == "NAME missing (see 'mast-utils list-host')" ]]
}

@test "should raise error without PRINTER parameter" {
    run mast-utils add-channel NAME=bats.test

    [[ "$status" == "$MAKEFILE_ERROR" ]]
    [[ $(remove_ansi ${lines[1]}) == "PRINTER missing (IP address or hostname)" ]]
}

@test "should raise error with PRINTER=none" {
    run mast-utils add-channel NAME=bats.test PRINTER=none

    [[ "$status" == "$MAKEFILE_ERROR" ]]
    [[ $(remove_ansi ${lines[1]}) == "PRINTER missing (IP address or hostname)" ]]
}

@test "should add a channel rule in ForwardPort array" {
    cp /etc/mast/{template,bats.test}
    old_channels_count=$(source /etc/mast/bats.test; echo ${#ForwardPort[@]})

    run mast-utils add-channel NAME=bats.test PRINTER=my-printer
    new_channels_count=$(source /etc/mast/bats.test; echo ${#ForwardPort[@]})

    [[ "$status" == $NO_ERROR ]]
    (( $new_channels_count == $old_channels_count + 1 ))
    rm /etc/mast/bats.test
}

@test "should belong to 'mast' user" {
    cp /etc/mast/{template,bats.test}
    chown nobody /etc/mast/bats.test

    run mast-utils add-channel NAME=bats.test PRINTER=my-printer
    owner_user=$(stat -c "%U" /etc/mast/bats.test)

    [[ "$status" == $NO_ERROR ]]
    [[ $owner_user == 'mast' ]]
}

@test "should set read/write/execute permissions for user and group" {
    cp /etc/mast/{template,bats.test}
    chmod u=,g=,o= /etc/mast/bats.test

    run mast-utils add-channel NAME=bats.test PRINTER=my-printer
    permissions=$(stat -c "%A" /etc/mast/bats.test)

    [[ "$status" == $NO_ERROR ]]
    [[ $permissions == '-rwxrwx---' ]]
}