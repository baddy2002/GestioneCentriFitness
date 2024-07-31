#!/bin/bash

# Attendi che Kafka sia completamente avviato
sleep 20

# Crea il topic "employee-invitation"
kafka-topics --create --topic employee-invitation --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

echo "Topic 'employee-invitation' creato"


# Crea il topic "email-tasks"
kafka-topics --create --topic email-tasks --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

echo "Topic 'email-tasks' creato"