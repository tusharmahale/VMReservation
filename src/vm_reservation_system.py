import sqlite3
import threading
import random
import string
import paramiko

class VMReservationSystem:
    def __init__(self, db_file):
        self.db_file = db_file
        self.lock = threading.Lock()
        self._initialize_database()

    def checkout(self, user_id):
        with self.lock:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM vms WHERE checked_out = 0 LIMIT 1")
            result = c.fetchone()
            if result is None:
                conn.close()
                return None
            vm = dict(result)
            c.execute("UPDATE vms SET checked_out = 1, checkedout_by_user_id = ? WHERE id = ?", (user_id, vm["id"],))
            conn.commit()
            conn.close()
            return vm["ip_address"]

    def checkin(self, user_id, ip_address):
        with self.lock:
            conn = sqlite3.connect(self.db_file)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM vms WHERE ip_address = ?", (ip_address,))
            result = c.fetchone()
            if result is None:
                conn.close()
                return False
            vm = dict(result)
            if vm["checkedout_by_user_id"] != user_id or not vm["checked_out"] or vm["ip_address"] != ip_address:
                print(vm)
                conn.close()
                return False
            c.execute("UPDATE vms SET checked_out = 0, checkedout_by_user_id = 0 WHERE id = ?", (vm["id"],))
            conn.commit()
            conn.close()
            # self._cleanup_vm(vm)
            return True

    def _cleanup_vm(self, vm):
        key = paramiko.RSAKey.from_private_key_file('/path/to/private/key')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(vm["ip_address"], username="root", pkey=key)
        stdin, stdout, stderr = ssh.exec_command("rm -rf /tmp/*")
        ssh.close()

    def _initialize_database(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        conn.row_factory = sqlite3.Row
        c.execute("CREATE TABLE IF NOT EXISTS vms (id INTEGER PRIMARY KEY, ip_address TEXT, checked_out INTEGER, checkedout_by_user_id INTEGER)")
        # c.execute("SELECT COUNT(*) FROM vms")
        # result = c.fetchone()
        # count = result[0]
        # Add entries to DB
        # c.execute("INSERT INTO vms ('ip_address', checked_out, checkedout_by_user_id) VALUES (?, 0)", ('10.20.0.11',,))
        conn.commit()
        conn.close()

