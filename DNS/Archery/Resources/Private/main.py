# Loosely based on https://gist.github.com/xero/65fc61e0bd8a4d4f267861cc3785e95b

from datetime import datetime, timedelta

# The correct flag
FLAG="csc{Th3T1m3T0L1v3i5n0w}"

# When to show correct flag
from pytz import timezone
TZ = timezone("Europe/Brussels")
WINDOWS=[
    (TZ.localize(datetime(year=2024, month=3, day=8, hour=11, minute=34)), TZ.localize(datetime(year=2024, month=3, day=8, hour=11, minute=35))),
    (TZ.localize(datetime(year=2024, month=3, day=8, hour=13, minute=21)), TZ.localize(datetime(year=2024, month=3, day=8, hour=13, minute=22))),
    (TZ.localize(datetime(year=2024, month=3, day=8, hour=16, minute=50)), TZ.localize(datetime(year=2024, month=3, day=8, hour=16, minute=51))),
    (TZ.localize(datetime(year=2024, month=3, day=9, hour=9, minute=54)), TZ.localize(datetime(year=2024, month=3, day=9, hour=9, minute=55))),
    (TZ.localize(datetime(year=2024, month=3, day=9, hour=15, minute=59)), TZ.localize(datetime(year=2024, month=3, day=9, hour=16, minute=0))),
    (TZ.localize(datetime(year=2024, month=3, day=9, hour=16, minute=11)), TZ.localize(datetime(year=2024, month=3, day=9, hour=16, minute=12))),
    (TZ.localize(datetime(year=2024, month=3, day=9, hour=17, minute=44)), TZ.localize(datetime(year=2024, month=3, day=9, hour=17, minute=45))),
]

# Nameserver configuration
DOMAIN = "knightsofthebinarytable.be"
NS1_IP = "3.250.27.124"
NS2_IP = "34.242.152.175"

# Ensure the windows are sorted
WINDOWS = sorted(WINDOWS, key=lambda item: item)
# Ensure the end is after the start
for window in WINDOWS:
    assert window[0] < window[1]

IDX = 0

IP="0.0.{}.{}"

from dnslib import DNSLabel, QTYPE, RD, RR, RCODE
from dnslib import A, AAAA, CNAME, MX, NS, SOA, TXT
from dnslib.server import DNSServer
from time import sleep

TYPE_LOOKUP = {
    A: QTYPE.A,
    AAAA: QTYPE.AAAA,
    CNAME: QTYPE.CNAME,
    MX: QTYPE.MX,
    NS: QTYPE.NS,
    SOA: QTYPE.SOA,
    TXT: QTYPE.TXT,
}
SERIAL = 1


class Record:
    def __init__(self, rdata_type, *args, rtype=None, rname=None, ttl=None, **kwargs):
        if isinstance(rdata_type, RD):
            # actually an instance, not a type
            self._rtype = TYPE_LOOKUP[rdata_type.__class__]
            rdata = rdata_type
        else:
            self._rtype = TYPE_LOOKUP[rdata_type]
            if rdata_type == SOA and len(args) == 2:
                # add sensible times to SOA
                args += ((
                    SERIAL,  # serial number
                    60 * 60 * 1,  # refresh
                    60 * 60 * 3,  # retry
                    60 * 60 * 24,  # expire
                    60 * 60 * 1,  # minimum
                ),)
            rdata = rdata_type(*args)

        if rtype:
            self._rtype = rtype
        self._rname = rname
        self.kwargs = dict(
            rdata=rdata,
            ttl=self.sensible_ttl() if ttl is None else ttl,
            **kwargs
        )

    def try_rr(self, q):
        if q.qtype == QTYPE.ANY or q.qtype == self._rtype:
            return self.as_rr(q.qname)

    def as_rr(self, alt_rname):
        return RR(rname=self._rname or alt_rname, rtype=self._rtype, **self.kwargs)

    def sensible_ttl(self):
        if self._rtype in (QTYPE.NS, QTYPE.SOA):
            return 60 * 60 * 24
        else:
            return 60 * 60

    @property
    def is_soa(self):
        return self._rtype == QTYPE.SOA

    def __str__(self):
        return '{} {}'.format(QTYPE[self._rtype], self.kwargs)

ZONES = {
    DOMAIN: [
        Record(A, '0.0.0.0'),
        Record(NS, f'ns1.{DOMAIN}.'),
        Record(NS, f'ns2.{DOMAIN}.'),
        Record(TXT, "Check again in this IPv4 amount of time and we'll give you the flag."),
        Record(TXT, "We're sorry it Takes This Long"),
        Record(TXT, "You'll have one minute to find the flag")
    ],
}

TYPE_LOOKUP = {
    A: QTYPE.A,
    AAAA: QTYPE.AAAA,
    CNAME: QTYPE.CNAME,
    MX: QTYPE.MX,
    NS: QTYPE.NS,
    SOA: QTYPE.SOA,
    TXT: QTYPE.TXT,
}

def should_lie() -> int | None:
    """
    Returns how long you should lie until the real flag re-appears.
    If 0, we're telling the truth. If None, we won't tell the truth anymore.
    """
    global IDX
    now = datetime.now(tz=TZ)

    # Advance in the windows list
    while len(WINDOWS) > IDX and now > WINDOWS[IDX][1]:
        IDX += 1
    if IDX == len(WINDOWS):
        return None
    if now > WINDOWS[IDX][0] and now < WINDOWS[IDX][1]:
        return 0
    return (WINDOWS[IDX][0] - now).seconds



class Resolver:
    def __init__(self):
        self.zones = {DNSLabel(k): v for k, v in ZONES.items()}

    def resolve(self, request, _):
        reply = request.reply()
        zone = self.zones.get(request.q.qname)
        if zone is not None:
            for zone_records in zone:
                rr = zone_records.try_rr(request.q)
                rr and reply.add_answer(rr)
        return reply

    def _update_zone(self, new_zones):
        self.zones = {DNSLabel(k): v for k, v in new_zones.items()}

    def tick(self):
        """Update the zone"""
        timer_value = should_lie()
        if timer_value is None:
            zones = {
                DOMAIN: [
                    Record(A, '0.0.0.0'),
                    Record(NS, f'ns1.{DOMAIN}.'),
                    Record(NS, f'ns2.{DOMAIN}.'),
                    Record(TXT, "Time's up! You can no longer find the flag")
                ],
                f'ns1.{DOMAIN}': [
                    Record(A, NS1_IP)
                ],
                f'ns2.{DOMAIN}': [
                    Record(A, NS2_IP)
                ]
            }
            self._update_zone(zones)
        elif timer_value == 0:
            zones = {
                DOMAIN: [
                    Record(A, '99.99.99.99'.format(timer_value//60, timer_value % 60)),
                    Record(NS, f'ns1.{DOMAIN}.'),
                    Record(NS, f'ns2.{DOMAIN}.'),
                    Record(TXT, f"Nice! Here's a little gift: {FLAG}")
                ],
                f'ns1.{DOMAIN}': [
                    Record(A, NS1_IP)
                ],
                f'ns2.{DOMAIN}': [
                    Record(A, NS2_IP)
                ]
            }
            self._update_zone(zones)
        else:
            td = timedelta(seconds=timer_value)
            secs = td.seconds % 60
            mins = (td.seconds // 60) % 60
            hours = td.seconds // 3600
            days = td.seconds // 86400
            zones = {
                DOMAIN: [
                    Record(A, f'{days}.{hours}.{mins}.{secs}'),
                    Record(NS, f'ns1.{DOMAIN}.'),
                    Record(NS, f'ns2.{DOMAIN}.'),
                    Record(TXT, "Check again in this IPv4 amount of time and we'll give you the flag."),
                    Record(TXT, "We're sorry it Takes This Long")
                ],
                f'ns1.{DOMAIN}': [
                    Record(A, NS1_IP)
                ],
                f'ns2.{DOMAIN}': [
                    Record(A, NS2_IP)
                ]
            }
            self._update_zone(zones)


resolver = Resolver()
servers= [DNSServer(resolver, port=53, address='0.0.0.0', tcp=False)]

if __name__ == '__main__':
    for s in servers:
        s.start_thread()

    try:
        while 1:
            resolver.tick()
            sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        for s in servers:
            s.stop()
