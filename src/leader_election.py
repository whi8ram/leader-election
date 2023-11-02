import logging
import time
from logging import INFO

from kazoo.client import EventType, KazooClient, WatchedEvent
from kazoo.security import OPEN_ACL_UNSAFE

logger = logging.getLogger(__name__)
logger.setLevel(INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class LeaderElection:
    election_namespace = "/election"
    session_timeout = 3000

    def __init__(self, zookeeper_address: str):
        self.zookeeper_address = zookeeper_address
        self._connect()
        if not self.client.exists(self.election_namespace):
            self.client.create(
                path=self.election_namespace,
                value=b"",
                acl=OPEN_ACL_UNSAFE,
            )
    
    def __del__(self):
        self.client.stop()
        self.client.close()

    def run(self):
        self.client.ChildrenWatch(
            path=self.election_namespace,
            func=self._watcher,
            send_event=True,
        )
        self._volunteer_for_leadership()
        while True:
            time.sleep(100)

    def _volunteer_for_leadership(self):
        znode_prefix = self.election_namespace + "/c_"
        znode_full_path = self.client.create(
            path=znode_prefix,
            value=b"",
            acl=OPEN_ACL_UNSAFE,
            ephemeral=True,
            sequence=True,
        )
        logger.info(f"create znode! {znode_full_path}")
        self.current_znode_name = znode_full_path.replace(
            self.election_namespace + "/", ""
        )

    def _elect_leader(self):
        children = self.client.get_children(self.election_namespace)
        children.sort()
        smallest_child = children[0]

        if smallest_child == self.current_znode_name:
            logger.info("I am the leader!")
        else:
            logger.info("I am not the leader.")

    def _get_root_znode_status(self):
        stat = self.client.exists(self.election_namespace)
        if stat is not None:
            data, _ = self.client.get(self.election_namespace)
            children = self.client.get_children(self.election_namespace)
            logger.info(f"Data: {data}\tChildren: {children}")

    def _watcher(self, children, event: WatchedEvent | None):
        if event is None:
            logger.info("Successfully connected to zookeeper!")
        elif event.type == EventType.CHILD:
            logger.info(f"'{self.election_namespace}' children changed!")
            self._elect_leader()

        self._get_root_znode_status()

    def _connect(self):
        self.client = KazooClient(
            hosts="localhost:2181",
            timeout=self.session_timeout,
        )
        self.client.start()
