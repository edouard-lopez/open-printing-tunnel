#!/usr/bin/env bats

setup() {
    alias mast-utils="$BATS_TEST_DIRNAME/../makefile"
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
