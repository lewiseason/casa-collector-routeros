`casa-collector-routeros` connects to a RouterOS router (using the
[RouterOS API]) and queries its arp table.  A list of mac addresses is then
stored in the specified [Redis] instance (as a list, using the key
`mac-addresses`).

If an address appears or disappears in between checks, an event will be emitted
on a redis topic (`mac-address-online` and `mac-address-offline` respectively).
The body of this message will be the MAC address.

Throughout, MAC addresses are represented in the usual `xx:xx:xx:xx:xx:xx` format.

## Installation

```shell
pip install casa-collector-routeros
```

## Invocation

Run `casa-collector-routeros` and the collector will start in the foreground.

## Configuration

Is done entirely through environment variables.

| Environment variable                        | Description                                                                                    | Notes                                 |
|---------------------------------------------|------------------------------------------------------------------------------------------------|---------------------------------------|
| `REDIS_URL`                                 | The URL of the Redis instance                                                                  | Example: redis://localhost:6379       |
| `ROUTER_HOST`, `ROUTER_USER`, `ROUTER_PASS` | The host and credentials of the RouterOS device (which must have its API correctly configured) | Using a read-only user is recommended |
| `INTERVAL`                                  | How frequently (in seconds) the router should be queried                                       | Default: 60                           |
| `LOGLEVEL`                                  | Log level. Messages are logged to stdout                                                       | Must be a valid Python [log level]    |


[RouterOS API]: https://wiki.mikrotik.com/wiki/Manual:API
[Redis]: https://redis.io/
[log level]: https://docs.python.org/2/library/logging.html#logging-levels
