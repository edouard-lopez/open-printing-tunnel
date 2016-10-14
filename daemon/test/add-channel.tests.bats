#!/usr/bin/env bats

setup() {
    alias mast-utils="$BATS_TEST_DIRNAME/../makefile"
    NO_ERROR=0
    MAKEFILE_ERROR=2
}

teardown() {
    unalias mast-utils
}

remove_ansi() {  # http://superuser.com/a/380778/174465
    echo $@ | sed -r 's/\x1b\[[^@-~]*[@-~]//g'
}

@test "should raise error without NAME parameter" {
    run mast-utils add-channel

    [[ "$status" == $MAKEFILE_ERROR ]]
    [[ $(remove_ansi ${lines[1]}) == "NAME missing (see 'mast-utils list-host')" ]]
}

@test "should raise error with NAME=none" {
    run mast-utils add-channel NAME=none

    [[ "$status" == $MAKEFILE_ERROR ]]
    [[ $(remove_ansi ${lines[1]}) == "NAME missing (see 'mast-utils list-host')" ]]
}

@test "should raise error without PRINTER parameter" {
    run mast-utils add-channel NAME=bats.test

    [[ "$status" == $MAKEFILE_ERROR ]]
    [[ $(remove_ansi ${lines[1]}) == "PRINTER missing (IP address or hostname)" ]]
}

@test "should raise error with PRINTER=none" {
    run mast-utils add-channel NAME=bats.test PRINTER=none

    [[ "$status" == $MAKEFILE_ERROR ]]
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