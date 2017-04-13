import os
import sys
import logging
from apscheduler.schedulers.background import BlockingScheduler
import redis
import routeros_api


def main():
    try:
        config = {
                'REDIS_URL':  os.environ['REDIS_URL'],
                'ROUTER_HOST': os.environ['ROUTER_HOST'],
                'ROUTER_USER': os.environ['ROUTER_USER'],
                'ROUTER_PASS': os.environ['ROUTER_PASS'],
                'INTERVAL': int(os.environ.get('INTERVAL', 60)),
                'LOGLEVEL': getattr(logging,
                                    os.environ.get('LOGLEVEL', 'WARNING')),
        }
    except KeyError as exc:
        logging.error("Failed to get configuration from the environment: {}"
                      .format(exc))
        sys.exit(1)

    logging.basicConfig(level=config['LOGLEVEL'])
    logging.getLogger("apscheduler").setLevel(logging.WARNING)

    scheduler = BlockingScheduler()

    logging.warning("Checking the ARP table on `{}' every {} seconds."
                    .format(config['ROUTER_HOST'], config['INTERVAL']))

    scheduler.add_job(run, 'interval', [config], seconds=config['INTERVAL'])
    scheduler.start()


def run(config):
    connection = routeros_api.RouterOsApiPool(config['ROUTER_HOST'],
                                              username=config['ROUTER_USER'],
                                              password=config['ROUTER_PASS'])
    api = connection.get_api()

    redis_connection = redis.from_url(config['REDIS_URL'])

    arp_entries = api.get_resource('/ip/arp')
    addresses = set([entry['mac-address'] for entry in arp_entries.get()
                    if 'mac-address' in entry])

    logging.info("Found {} mac addresses in the ARP table: {}"
                 .format(len(addresses), addresses))

    previous_addresses = redis_connection.lrange('mac-addresses', 0, -1) or []
    previous_addresses = set([a.decode() for a in previous_addresses])

    if addresses != previous_addresses:
        logging.info("Address list has changed, replace with new list.")

        transaction = redis_connection.pipeline()
        transaction.delete('mac-addresses')
        transaction.lpush('mac-addresses', *addresses)
        transaction.execute()

        online = addresses - previous_addresses
        offline = previous_addresses - addresses

        for address in online:
            logging.info("{} came online, emitting update.".format(address))
            redis_connection.publish('mac-address-online', address)

        for address in offline:
            logging.info("{} went offline, emitting update.".format(address))
            redis_connection.publish('mac-address-offline', address)


if __name__ == '__main__':
    main()
