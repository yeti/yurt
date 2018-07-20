
def get_export_config_json (home):
    return """{{
    "ConfigVersion": 3,
    "Driver": {{
        "IPAddress": "11.22.33.44",
        "MachineName": "test-host",
        "SSHUser": "root",
        "SSHPort": 22,
        "SSHKeyPath": "{home}/.docker/machine/machines/test-host/testkey.pem",
        "StorePath": "{home}/.docker/machine",
        "SwarmMaster": false,
        "SwarmHost": "",
        "SwarmDiscovery": "",
        "EnginePort": 2376,
        "SSHKey": "{home}/.ssh/testkey.pem"
    }},
    "DriverName": "generic",
    "HostOptions": {{
        "Driver": "",
        "Memory": 0,
        "Disk": 0,
        "EngineOptions": {{
            "ArbitraryFlags": [],
            "Dns": null,
            "GraphDir": "",
            "Env": [],
            "Ipv6": false,
            "InsecureRegistry": [],
            "Labels": [],
            "LogLevel": "",
            "StorageDriver": "",
            "SelinuxEnabled": false,
            "TlsVerify": true,
            "RegistryMirror": [],
            "InstallURL": "https://get.docker.com"
        }},
        "SwarmOptions": {{
            "IsSwarm": false,
            "Address": "",
            "Discovery": "",
            "Agent": false,
            "Master": false,
            "Host": "tcp://0.0.0.0:3376",
            "Image": "swarm:latest",
            "Strategy": "spread",
            "Heartbeat": 0,
            "Overcommit": 0,
            "ArbitraryFlags": [],
            "ArbitraryJoinFlags": [],
            "Env": null,
            "IsExperimental": false
        }},
        "AuthOptions": {{
            "CertDir": "{home}/.docker/machine/certs",
            "CaCertPath": "{home}/.docker/machine/certs/ca.pem",
            "CaPrivateKeyPath": "{home}/.docker/machine/certs/ca-key.pem",
            "CaCertRemotePath": "",
            "ServerCertPath": "{home}/.docker/machine/machines/test-host/server.pem",
            "ServerKeyPath": "{home}/.docker/machine/machines/test-host/server-key.pem",
            "ClientKeyPath": "{home}/.docker/machine/certs/key.pem",
            "ServerCertRemotePath": "",
            "ServerKeyRemotePath": "",
            "ClientCertPath": "{home}/.docker/machine/certs/cert.pem",
            "ServerCertSANs": [],
            "StorePath": "{home}/.docker/machine/machines/test-host"
        }}
    }},
    "Name": "test-host"
}}
""".format(home=home)


def get_export_aws_config_json(home):
    return """{{
    "ConfigVersion": 3,
    "Driver": {{
        "IPAddress": "11.22.33.44",
        "MachineName": "test-host2",
        "SSHUser": "ubuntu",
        "SSHPort": 22,
        "SSHKeyPath": "{home}/.docker/machine/machines/test-host2/id_rsa",
        "StorePath": "{home}/.docker/machine",
        "SwarmMaster": false,
        "SwarmHost": "tcp://0.0.0.0:3376",
        "SwarmDiscovery": "",
        "Id": "1df29f6605f746dea1217e8412a59dd5",
        "AccessKey": "testaccesskey",
        "SecretKey": "test+secretkey",
        "SessionToken": "",
        "Region": "us-east-1",
        "AMI": "ami-sdadasd",
        "SSHKeyID": 0,
        "ExistingKey": false,
        "KeyName": "test-host2",
        "InstanceId": "i-34204820349820",
        "InstanceType": "t2.micro",
        "PrivateIPAddress": "1.2.3.4",
        "SecurityGroupId": "",
        "SecurityGroupIds": [
            "sg-8adf0bc0"
        ],
        "SecurityGroupName": "",
        "SecurityGroupNames": [
            "docker-machine"
        ],
        "OpenPorts": null,
        "Tags": "",
        "ReservationId": "",
        "DeviceName": "/dev/sda1",
        "RootSize": 16,
        "VolumeType": "gp2",
        "IamInstanceProfile": "",
        "VpcId": "vpc-blah",
        "SubnetId": "subnet-bleh",
        "Zone": "a",
        "RequestSpotInstance": false,
        "SpotPrice": "0.50",
        "BlockDurationMinutes": 0,
        "PrivateIPOnly": false,
        "UsePrivateIP": false,
        "UseEbsOptimizedInstance": false,
        "Monitoring": false,
        "SSHPrivateKeyPath": "",
        "RetryCount": 5,
        "Endpoint": "",
        "DisableSSL": false,
        "UserDataFile": ""
    }},
    "DriverName": "amazonec2",
    "HostOptions": {{
        "Driver": "",
        "Memory": 0,
        "Disk": 0,
        "EngineOptions": {{
            "ArbitraryFlags": [],
            "Dns": null,
            "GraphDir": "",
            "Env": [],
            "Ipv6": false,
            "InsecureRegistry": [],
            "Labels": [],
            "LogLevel": "",
            "StorageDriver": "",
            "SelinuxEnabled": false,
            "TlsVerify": true,
            "RegistryMirror": [],
            "InstallURL": "https://get.docker.com"
        }},
        "SwarmOptions": {{
            "IsSwarm": false,
            "Address": "",
            "Discovery": "",
            "Agent": false,
            "Master": false,
            "Host": "tcp://0.0.0.0:3376",
            "Image": "swarm:latest",
            "Strategy": "spread",
            "Heartbeat": 0,
            "Overcommit": 0,
            "ArbitraryFlags": [],
            "ArbitraryJoinFlags": [],
            "Env": null,
            "IsExperimental": false
        }},
        "AuthOptions": {{
            "CertDir": "{home}/.docker/machine/certs",
            "CaCertPath": "{home}/.docker/machine/certs/ca.pem",
            "CaPrivateKeyPath": "{home}/.docker/machine/certs/ca-key.pem",
            "CaCertRemotePath": "",
            "ServerCertPath": "{home}/.docker/machine/machines/test-host2/server.pem",
            "ServerKeyPath": "{home}/.docker/machine/machines/test-host2/server-key.pem",
            "ClientKeyPath": "{home}/.docker/machine/certs/key.pem",
            "ServerCertRemotePath": "",
            "ServerKeyRemotePath": "",
            "ClientCertPath": "{home}/.docker/machine/certs/cert.pem",
            "ServerCertSANs": [],
            "StorePath": "{home}/.docker/machine/machines/test-host2"
        }}
    }},
    "Name": "test-host2"
}}
""".format(home=home)
