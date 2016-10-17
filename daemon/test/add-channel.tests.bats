#!/usr/bin/env bats

setup() {
    export NO_ERROR=0
    export MAKEFILE_ERROR=2
    export status
    export lines
    cp --preserve /etc/mast/{template,bats.test}
}

teardown() {
    unset NO_ERROR
    unset MAKEFILE_ERROR
    rm  --force --recursive /tmp/ports /tmp/mast.busy /etc/mast/bats.test
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
    old_channels_count=$(source /etc/mast/bats.test; echo ${#ForwardPort[@]})

    run mast-utils add-channel NAME=bats.test PRINTER=my-printer

    new_channels_count=$(source /etc/mast/bats.test; echo ${#ForwardPort[@]})

    [[ "$status" == $NO_ERROR ]]
    (( $new_channels_count == $old_channels_count + 1 ))
    rm /etc/mast/bats.test
}

@test "should belong to 'mast' user" {
    chown nobody /etc/mast/bats.test

    run mast-utils add-channel NAME=bats.test PRINTER=my-printer
    owner_user=$(stat -c "%U" /etc/mast/bats.test)

    [[ "$status" == $NO_ERROR ]]
    [[ $owner_user == 'mast' ]]
}

@test "should set read/write/execute permissions for user and group" {
    chmod u=,g=,o= /etc/mast/bats.test

    run mast-utils add-channel NAME=bats.test PRINTER=my-printer
    permissions=$(stat -c "%A" /etc/mast/bats.test)

    [[ "$status" == $NO_ERROR ]]
    [[ $permissions == '-rwxrwx---' ]]
}

@test "should support concurrent addition" {
    {
        for ((i=0; $i < 10; i++)); do
            mast-utils add-channel NAME=bats.test PRINTER=parallel1-$i;
        done
    } & pid_bulk1=$!
    {
        for ((i=0; $i < 10; i++)); do
            mast-utils add-channel NAME=bats.test PRINTER=parallel2-$i;
        done
    } & pid_bulk2=$!

    wait $pid_bulk1 $pid_bulk2
    channels_count=$(source /etc/mast/bats.test; echo ${#ForwardPort[@]})

#    [[ "$status" == "$NO_ERROR" ]]  # fixme: missing $status
    (( $channels_count == 20 ))
}
