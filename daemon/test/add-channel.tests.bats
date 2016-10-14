#!/usr/bin/env bats

setup() {
    alias mast-utils="$BATS_TEST_DIRNAME/../makefile"
}

teardown() {
    unalias mast-utils
}

remove_ansi() {  # http://superuser.com/a/380778/174465
    echo $@ | sed -r 's/\x1b\[[0-9;]*m//g'
}

@test "should raise error without NAME parameter" {
    run mast-utils add-channel

    [[ "$status" == 2 ]]
    [[ $(remove_ansi ${lines[1]}) == "NAME missing (see 'mast-utils list-host')" ]]
}
