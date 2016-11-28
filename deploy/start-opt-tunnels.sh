#!/usr/bin/env bash

### BEGIN INIT INFO
# Provides:          start-tunnel-after-reboot
# Required-Start:    $network $local_fs $remote_fs $syslog
# Required-Stop:     $network $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start OPT tunnels in older containers (≤1.5.11)
# Description:       Start OPT tunnels in older containers (≤1.5.11) after the host reboot
### END INIT INFO

# USAGE
#       ./start-opt-tunnels.sh

sleep 10s
containers=$(docker ps --format "{{.ID}}")

for container in "${containers[@]}"; do
    docker exec "$container" /etc/init.d/mast start
done